
"""
Only get products from categories below
"""
ALLOWED_CATEGORIES = ["Pantry, Household & Pets", "Grocery"],


""" 
Branches information

sources:
    https://www.walmart.ca/en/stores-near-me/thunder-bay-supercentre-3124
    https://www.walmart.ca/en/stores-near-me/dufferin-mall-supercentre-3106
"""
BRANCHES_INFO = {
    3124: {
        'branch_name': 'Thunder Bay Supercentre',
        'postal_code': 'P7B 3Z7',
        'latitude': '48.4114837646',
        'longitude': '-89.2452468872',
    },
    3106: {
        'branch_name': 'Dufferin Mall Supercentre',
        'postal_code': 'M6H 4A9',
        'latitude': '43.6560592651',
        'longitude': '-79.434173584',
    },
}


""" 
Walmart CA API URL to check product info per branch 
e.g.  BASE_URL + '?latitude={lat_val}&longitude={long_val}&lang=en&upc={bar_code}'
"""
FIND_IN_STORE_BASE_URL = 'https://www.walmart.ca/api/product-page/find-in-store'
