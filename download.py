from os import getenv
from pathlib import Path

import duckdb
from dotenv import load_dotenv
from httpx import stream

load_dotenv(override=True)

GEOJSON = getenv("DOWNLOAD_GEOJSON", "")
YEAR = getenv("DOWNLOAD_YEAR", "")
CHUNK_SIZE = int(getenv("CHUNK_SIZE", "104857600"))

cwd = Path(__file__).parent
stac_path = cwd / "data/stac.parquet"
download_path = cwd / "data/downloads"
download_path.mkdir(exist_ok=True, parents=True)


def main() -> None:
    """Filters a GeoParquet file using a GeoJSON file for the geometry."""
    with duckdb.connect() as con:
        con.sql("INSTALL spatial;")
        con.sql("LOAD spatial;")
        query = f"""
            SELECT assets.data.href FROM '{stac_path}'
            WHERE ST_Intersects(
                ST_GeomFromGeoJSON('{GEOJSON}'),
                geometry
            ) AND date_part('year', datetime) = {YEAR};
        """
        urls = con.sql(query).to_df()["href"].tolist()
    for url in urls:
        file_name = url.split("/")[-1]
        with (download_path / file_name).open("wb") as f, stream("GET", url) as r:
            for data in r.iter_bytes(chunk_size=CHUNK_SIZE):
                f.write(data)


if __name__ == "__main__":
    main()
