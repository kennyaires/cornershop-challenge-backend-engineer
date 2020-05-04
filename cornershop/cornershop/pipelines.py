import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tools import get_product_info_from_branch
from references import BRANCHES_INFO

import sys
sys.path.append('..')

from models import Product, BranchProduct


class CornershopPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker
        """
        engine = create_engine('sqlite:///../db.sqlite')
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        self.file = open('output.txt', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line =  json.dumps(dict(item)) + '\n'
        self.file.write(line)

        session = self.Session()

        # create Product object
        product = Product(
            store="Walmart",
            barcodes=item['bar_code'],
            sku=item['sku'],
            brand=item['brand'],
            name=item['name'],
            description=item['description'],
            package=item['package'],
            image_urls=item['image_urls'] ,
            category=item['category'],
            product_url=item['product_url']
        )

        # create BranchProduct objects
        branch_one = get_product_info_from_branch(list(BRANCHES_INFO.keys())[0], item['bar_code'])
        branch_two = get_product_info_from_branch(list(BRANCHES_INFO.keys())[1], item['bar_code'])

        branch_product_1 = BranchProduct(
            branch=str(list(BRANCHES_INFO.keys())[0]),
            product=product,
            stock=branch_one.get('availableToSellQty', 0),
            price=branch_one.get('sellPrice', 0),
        )

        branch_product_2 = BranchProduct(
            branch=str(list(BRANCHES_INFO.keys())[1]),
            product=product,
            stock=branch_two.get('availableToSellQty', 0),
            price=branch_two.get('sellPrice', 0),
        )

        session.add(product)
        session.commit()

        return item
