# Google Earth Engine Manifest to STAC GeoParquet

This tool converts Google Earth Engine Manifests to STAC GeoParquet for faster querying, then creating a list of URL's from that catalog grouping resources by country-year.

1. Ensure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) and [gsutils](https://cloud.google.com/storage/docs/gsutil_install) installed.
2. Initialize your environment with `uv venv && uv sync`.
3. Use `python scripts/stac.py` to generate a STAC GeoParquet from Google's manifest JSON.
4. Download [UN Geodata](https://geoportal.un.org/arcgis/apps/sites/#/geohub/datasets/702b9ed60bde48ba8619d691077ce309/about) from [UN Geo Hub](https://geohub.un.org). Add `BNDA_CTY.*` to the `data` directory in this project.
5. Use `python scripts/urls.py` to generate a list of URLs for each country-year combination.
6. Zip the `hdx` directory and publish on HDX.
