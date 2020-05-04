# Cornershop's backend integrations test

## Before you begin

Read this README completely before continuing. There whole content of this document is relevant for the test and there are some important tips and notes in every section.

Before you begin, create a new private repository. Once finished, invite as collaborators to @jeffersonlizar @lbenitez000
and share with your recruiter the link of the project.

## Introduction

This is the technical test for backend integration engineers. It's focused on connecting to remote services, gathering data and storing it in the project's models.

A common task is collecting product information form external sources as websites and files. In this project, you'll have to  build a web crawler that visits a website and extracts product information.

The data models have already been defined for you. The ORM for this project is SQLAlchemy. 

The product information is defined by two models (or tables):

### Product
The Product model contains basic product information:

*Product*

- Store
- Barcodes (a list of UPC/EAN barcodes)
- SKU (the product identifier in the store)
- Brand
- Name
- Description
- Package
- Image URLs (a comma separated list of URLs)
- Category
- Product URL

### BranchProduct
The BranchProduct model contains the attributes of a product that are specific for a store's branch. The same product can be available/unavailable or have different prices at different branches.

*BranchProduct*

- Branch
- Product
- Stock
- Price

## The case

Cornershop is expanding to Canada and we want to provide our customers with the very best stores available in their city. One of them is [Walmart](https://www.walmart.ca/). They offer a very broad selection of products, from breakfast cereals to gym equipment. We need to ingest their product information and store it in our database before we can offer them to our customers.

The product information we need is:

*Product*

- Store `Walmart`
- Barcodes `60538887928`
- SKU `10295446`
- Brand `Great Value`
- Name `Spring Water`
- Description `Convenient and refreshing, Great Value Spring Water is a healthy option...`
- Package `24 x 500ml`
- Image URLs `["https://i5.walmartimages.ca/images/Large/887/928/999999-60538887928.jpg", "https://i5.walmartimages.ca/images/Large/089/6_1/400896_1.jpg", "https://i5.walmartimages.ca/images/Large/88_/nft/605388879288_NFT.jpg"]`
- Category `Grocery|Pantry, Household & Pets|Drinks›Water|Bottled Water`
- Product URL `https://www.walmart.ca/en/ip/great-value-24pk-spring-water/6000143709667`

*BranchProduct*
 - Product `<product_id>`
 - Branch `3124`
 - Stock `426`
 - Price `2.27`

You will have to create a *[Scrapy](https://scrapy.org/)* spider in this project, then use it to crawl Walmart's website and store the collected products in our existing database.

### Constraints

The following constraints apply:
1. The web crawler **must be implemented using [Scrapy](https://scrapy.org/)** only. [Selenium](https://www.selenium.dev/), [Splash](https://github.com/scrapinghub/splash) and similar libraries are not allowed. This test can be completed without using any other library.
2. We only need (and only want) product information from the "Groceries" website.
3. We only need (and only want) information from the following branches: `3124` and `3106`. These branches are located in Toronto, Ontario Province.

### Considerations

In Walmart's website, the information is available per branch.

There is **no need** to create an account or sign-in.

The web crawler **must be implemented using [Scrapy](https://scrapy.org/)**.

You don't need to crawl the whole website, you can just stop when you have collected at least 500 Products with their 
respective BranchProducts for each branch.

The examples provided are just referential. **You are completely free to transform the information collected they way you want** (capitalize, replace text, transform symbols, etc.), but data stored must meet the data types and semantics of the data model. i.e: there must be a brand in the `Brand` field and a list of URLs in the `Image URLs` field, etc. The ORM is SQLAlchemy and it must be used as the only interface with the DB. If there is any piece of information that you think can be improved with some extra processing, please do it, we want high-quality information!

Feel free to **use the Python environment manager of your preference**. We provide a `Pipfile` in case you want to use `Pipenv` and a `requirements.txt` if you prefer to use Python's `pip`. Just remember to commit a file with the list of dependencies. 

**Create and initialize the database** running `python database_setup.py`.

**Commit the sqlite3 database** containing all the data collected.

# Aspects to be evaluated
- Software design
- Programing style
- Crawling strategy
- Data processing strategy
- Quality of the collected data
- GIT repository history
- Appropriate use of the framework

## Aproach and comments
The Scrapy project has one spider - WalmartCA.py -, it has three parses: the first one for crawling the xml site-map for categories urls, the second one for the category page on the groceries site and finally, a product parse.
I ended up using the scrapy-splash library in order to crawl on the groceries website as it its content is generated asynchronously throw javascript. The first parse and the product parse don't use the splash resources. When inquirying the WalmartCA api for product availabily on the store brach, I use the requests library. The splash service can be runned locally inside a docker container:

```
docker pull scrapinghub/splash
docker run -p 8050:8050 -d scrapinghub/splash
```

Starting the spider:
```
scrapy runspider cornershop/spiders/WalmartCA.py
```

The sqlite3 database has a total of 528 products and 1056 product branches.
Item example:
```
{"bar_code": "68113191195", "sku": "10052944", "brand": "Great Value", "name": "Great Value Large Eggs", "description": "Great Value Large Eggs. Great Value has the everyday essentials your family needs with guaranteed, money-back quality. From breakfast to baking, Great Value eggs can\u2019t be beat!", "package": "12 Count", "image_urls": "https://i5.walmartimages.ca/images/Large/924/227/6000197924227.jpg,https://i5.walmartimages.ca/images/Enlarge/924/227/6000197924227.jpg", "category": "Grocery|Dairy & Eggs|Eggs", "product_url": "https://www.walmart.ca/en/ip/great-value-large-eggs/10052944"}
```