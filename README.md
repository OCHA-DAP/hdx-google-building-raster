# Google Earth Engine Manifest to STAC GeoParquet

This tool converts Google Earth Engine Manifests to STAC GeoParquet for faster querying.

To use this tool, first make a copy of `.env.example` with the path to the manifest folder you wish to convert.

If running natively ensure you have `uv` and `gsutils` installed. Initialize your environment with `uv sync` followed by `python main.py`.

If running with Docker, install Docker Desktop and run `docker compose up --build`.
