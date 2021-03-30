import requests
import json
from pprint import pprint

# ## CONSTS ## #
API_URL = "https://5ka.ru/api/v2/"


# ## FUNCTIONS ## #
def get_categories():
    raw_categories = requests.get(API_URL + "categories").json()
    categories = {}
    for category in raw_categories:
        categories[category["parent_group_code"]] = category["parent_group_name"]
    return categories


def get_special_offers():
    for code, name in get_categories().items():
        now_page = requests.get(API_URL + "special_offers?categories=" + code).json()
        buffer = now_page["results"]
        while now_page["next"]:
            now_page = requests.get(now_page["next"]).json()
            buffer += now_page["results"]
        with open(code+".json", 'w') as f:
            json.dump({"name": name, "code": code, "products": buffer}, f)


# ## MAIN ## #
if __name__ == "__main__":
    get_special_offers()
