import json
from datetime import UTC, datetime
from os import getenv
from pathlib import Path
from subprocess import run

import pystac
import stac_geoparquet
from dotenv import load_dotenv
from pyproj import Transformer
from pystac.extensions.projection import ProjectionExtension
from shapely.geometry import box

load_dotenv(override=True)

MANIFEST_DIR = getenv("MANIFEST_DIR", "")

cwd = Path(__file__).parent
data_dir = cwd / "data"
manifests_dir = cwd / "data/manifests"
stac_dir = cwd / "data/stac"
stac_dir.mkdir(exist_ok=True, parents=True)


def main() -> None:
    """Create a STAC catalog from the Google Open Data manifests."""
    run(["gsutil", "-m", "cp", "-r", f"gs://{MANIFEST_DIR}", data_dir], check=False)
    for manifest_path in manifests_dir.glob("*.json"):
        with Path.open(manifest_path) as f:
            _, __, epsg, year, month, day = manifest_path.stem.split("_")
            transformer = Transformer.from_crs(
                f"EPSG:{epsg}",
                "EPSG:4326",
                always_xy=True,
            )
            data = json.load(f)
            bands = [
                {"name": x["id"], "nodata": x["missingData"]["values"][0]}
                for x in data["bands"]
            ]
            url_prefix = data["uriPrefix"][5:]
            items = []
            for source in data["tilesets"][0]["sources"]:
                source_id = source["uris"][0]
                at = source["affineTransform"]
                dim = source["dimensions"]
                xmin_utm = at["translateX"]
                ymin_utm = at["translateY"] + dim["height"] * at["scaleY"]
                xmax_utm = at["translateX"] + dim["width"] * at["scaleX"]
                ymax_utm = at["translateY"]
                xmin, ymin = transformer.transform(xmin_utm, ymin_utm)
                xmax, ymax = transformer.transform(xmax_utm, ymax_utm)
                item = pystac.Item(
                    id=f"{url_prefix.split('/')[-1]}{source_id[:-4]}".replace("/", "_"),
                    geometry=box(xmin, ymin, xmax, ymax).__geo_interface__,
                    bbox=[xmin, ymin, xmax, ymax],
                    datetime=datetime(int(year), int(month), int(day), tzinfo=UTC),
                    properties={},
                )
                item.add_link(
                    pystac.Link(
                        rel=pystac.RelType.VIA,
                        target=f"https://console.cloud.google.com/storage/browser/{MANIFEST_DIR}",
                    ),
                )
                proj = ProjectionExtension.ext(item, add_if_missing=True)
                proj.apply(code=f"EPSG:{epsg}")
                asset = pystac.Asset(
                    href=f"https://storage.googleapis.com/{url_prefix}{source_id}",
                    media_type=pystac.MediaType.COG,
                    roles=["data"],
                    extra_fields={"bands": bands},
                )
                item.add_asset(key="data", asset=asset)
                items.append(item)
            record_batch_reader = stac_geoparquet.arrow.parse_stac_items_to_arrow(items)
            stac_geoparquet.arrow.to_parquet(
                record_batch_reader,
                stac_dir / f"{manifest_path.stem}.parquet",
                compression="zstd",
            )


if __name__ == "__main__":
    main()
