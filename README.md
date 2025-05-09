# Google Earth Engine Manifest to STAC GeoParquet

This tool converts Google Earth Engine Manifests to STAC GeoParquet for faster querying, then creating a list of URL's from that catalog grouping resources by country-year.

For users on macOS / Linux, the code can be run natively using the folowing steps:

1. Ensure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) and [gsutils](https://cloud.google.com/storage/docs/gsutil_install) installed.
2. Download [UN Geodata](https://geoportal.un.org/arcgis/apps/sites/#/geohub/datasets/702b9ed60bde48ba8619d691077ce309/about) from [UN Geo Hub](https://geohub.un.org). Add `BNDA_CTY.*` to the `data` directory in this project.
3. Initialize your environment with `uv sync`.
4. Use `uv run task stac` to generate a STAC GeoParquet from Google's manifest JSON.
5. Use `uv run task urls` to generate a list of URLs for each country-year combination.
6. Zip the `hdx` directory and publish on HDX.

Alternatively, for Windows users or those unable to install the gsutil dependancy, Docker can run the code:

1. Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
2. Download [UN Geodata](https://geoportal.un.org/arcgis/apps/sites/#/geohub/datasets/702b9ed60bde48ba8619d691077ce309/about) from [UN Geo Hub](https://geohub.un.org). Add `BNDA_CTY.*` to the `data` directory in this project.
3. Run the scripts using `docker compose up --build`.
4. Zip the `hdx` directory and publish on HDX.
