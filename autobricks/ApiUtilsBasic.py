import requests
from requests.exceptions import HTTPError
from typing import Union
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(f"autobricks.ApiUtils")



def api_get(url: str, headers: dict, data: dict = None, query: str = None):


    if query:
        url = f"{url}?{query}"
    response = requests.get(url=url, headers=headers, json=data)

    try:
        response.raise_for_status()

    except HTTPError as e:

        msg = f"{e.response.status_code} error at {url} {e.response.text}"
        logger.error(msg)
        raise e

    return response.json()


def api_post(url: str, headers: dict, data: Union[str,dict]):

    response = requests.post(url=url, headers=headers, json=data)

    try:
        response.raise_for_status()

    except HTTPError as e:

        msg = f"{e.response.status_code} error at {url} {e.response.text}"
        logger.error(msg)
        raise e

    return response.json()

