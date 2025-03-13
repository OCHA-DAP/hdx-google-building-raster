from pathlib import Path

import duckdb
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)

cwd = Path(__file__).parent
stac_path = cwd / "data/stac.parquet"
bnda_cty_path = cwd / "data/bnda_cty.parquet"
urls_path = cwd / "data/urls"
urls_path.mkdir(exist_ok=True, parents=True)


def get_iso3() -> list[str]:
    """Get list of ISO-3 codes contained in the country admin boundaries."""
    iso3 = pd.read_parquet(bnda_cty_path, columns=["iso3cd"])
    return iso3["iso3cd"].tolist()


def get_years() -> list[int]:
    """Get list of years contained in the STAC file."""
    years = pd.read_parquet(stac_path, columns=["datetime"])
    return list(set(years["datetime"].dt.year))


def main() -> None:
    """Filters a GeoParquet file using a GeoJSON file for the geometry."""
    iso3_list = get_iso3()
    years = get_years()
    for iso3 in iso3_list:
        for year in years:
            with duckdb.connect() as con:
                con.sql("INSTALL spatial;")
                con.sql("LOAD spatial;")
                query = f"""
                    SELECT stac.assets.data.href
                    FROM '{stac_path}' as stac
                    JOIN '{bnda_cty_path}' as bnda_cty
                    ON ST_Intersects(stac.geometry, bnda_cty.geometry)
                    WHERE bnda_cty.iso3cd = '{iso3}'
                    AND date_part('year', stac.datetime) = {year};
                """
                urls = con.sql(query).to_df()["href"].tolist()
            if len(urls) > 0:
                with (urls_path / f"{iso3}_{year}.txt").open("w") as f:
                    f.write("\n".join(urls))


if __name__ == "__main__":
    main()
