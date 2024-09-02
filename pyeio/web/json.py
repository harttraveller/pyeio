from pathlib import Path


def crawl(): ...


def get(url: str):
    raise NotImplementedError()


def download(url: str, path: str | Path):
    raise NotImplementedError()


# # todo: get recursive from webpage or online directory
# # webpage: eg - scrape all json links and download to local dir
# # dir: eg - s3 bucket, dl all
