import threading
import requests
import json

# ## CONSTS ## #
API_URL = "https://5ka.ru/api/v2/"


# ## FUNCTIONS ## #
def thread(category):
    now_page = requests.get(
        API_URL + "special_offers?records_per_page=20&categories=" + category["parent_group_code"]).json()
    buffer = now_page["results"]
    while now_page["next"]:
        now_page = requests.get(now_page["next"]).json()
        buffer += now_page["results"]
    with open(category["parent_group_code"] + ".json", 'w') as f:
        json.dump({
            "name": category["parent_group_name"],
            "code": category["parent_group_code"],
            "products": buffer
        }, f)


def get_special_offers():
    threads = []
    for category in requests.get(API_URL + "categories").json():
        threads.append(tr := threading.Thread(target=thread, args=(category,)))
        tr.start()
    for tr in threads:
        tr.join()


# ## MAIN ## #
if __name__ == "__main__":
    get_special_offers()
