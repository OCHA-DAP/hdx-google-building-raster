# Google Open Building Temporal

source: <https://sites.research.google/gr/open-buildings/temporal/>

The Open Buildings 2.5D Temporal Dataset contains annual data spanning eight years (2016-2023) with building presence, fractional building counts, and building heights covering approximately 58 million square kilometers. It was produced using publicly available, low-resolution imagery from the [Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2) satellite mission, which has approximately 5-day revisit times and world-wide coverage. The resulting dataset has an effective spatial resolution of 4 meters, equivalent to what could be achieved by a high-resolution model using a single frame of 4-meter resolution imagery. The Open Buildings 2.5D Temporal Dataset is available across Africa, South Asia, South-East Asia, Latin America and the Caribbean.

The goal is to support organizations (e.g., governmental, non-profits, commercial) working on projects that benefit society, such as promoting sustainable development, disaster response and improving access to public healthcare, among other things. See the related [Research Blog post](https://research.google/blog/open-buildings-25d-temporal-dataset-tracks-building-changes-across-the-global-south/) to learn more.

## Downloading Data

This folder includes a simple python script which will download all the resources contained in the `urls` folder. Remove any files from this folder you don't want to download. Run the script using:

```shell
python download.py
```

Alternatively, download GeoTIFFs using the `wget` command like so:

```shell
wget --input-file={url_list.txt} --directory-prefix={output_folder}
```
