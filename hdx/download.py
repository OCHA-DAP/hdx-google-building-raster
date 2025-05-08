from pathlib import Path
from urllib.request import urlopen

cwd = Path(__file__).parent
url_path = cwd / "urls"
tif_path = cwd / "tifs"
tif_path.mkdir(exist_ok=True, parents=True)


def main() -> None:
    """Download all URLs from the urls directory."""
    for url_file in sorted(url_path.glob("*.txt")):
        group_path = tif_path / url_file.stem
        group_path.mkdir(exist_ok=True, parents=True)
        with url_file.open() as f_in:
            urls = f_in.read().splitlines()
            for url in urls:
                url_name = url.split("/")[-1]
                download_path = group_path / url_name
                if not download_path.exists():
                    with urlopen(url) as r:
                        data = r.read()
                        with download_path.open("wb") as f_out:
                            f_out.write(data)


if __name__ == "__main__":
    main()
