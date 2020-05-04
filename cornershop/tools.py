import requests
import json

from references import BRANCHES_INFO, FIND_IN_STORE_BASE_URL


def get_product_info_from_branch(branch_id, bar_code):
    """ Make request to Walmart API in order to get product availability info """

    try:
        request_url = f'{FIND_IN_STORE_BASE_URL}?latitude={BRANCHES_INFO[branch_id]["latitude"]}&longitude={BRANCHES_INFO[branch_id]["longitude"]}&lang=en&upc={bar_code}'
        response = requests.get(request_url)
        response = json.loads(response.text)
        result = [el for el in response['info'] if el['id'] == branch_id]

        return result[0]
    
    except:
        return dict()
