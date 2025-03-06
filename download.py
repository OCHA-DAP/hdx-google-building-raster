from os import getenv
from pathlib import Path

import duckdb
from dotenv import load_dotenv
from httpx import Client

load_dotenv(override=True)

GEOJSON = getenv("DOWNLOAD_GEOJSON", "")
YEAR = getenv("DOWNLOAD_YEAR", "")
TIMEOUT = int(getenv("DOWNLOAD_TIMEOUT", "600"))

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
        download_urls = con.sql(query).to_df()["href"].tolist()
    for download_url in download_urls:
        file_name = download_url.split("/")[-1]
        with Client(http2=True, timeout=TIMEOUT) as client:
            response = client.get(download_url)
            response.raise_for_status()
            with (download_path / file_name).open("wb") as f:
                f.write(response.content)


if __name__ == "__main__":
    main()
