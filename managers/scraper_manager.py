import requests
from bs4 import BeautifulSoup

from decorators import retry
from database.db import DBManager


class ScraperManager:
    # this is a class constant to define the classes in HTML of the host which contain the required product information
    PRODUCT_HTML_CLASS_NAMES = {
        "title" : ".woo-loop-product__title",
        "price" : ".woocommerce-Price-amount",
        "image" : ".attachment-woocommerce_thumbnail",
    }
    BASE_URL = "https://dentalstall.com/shop/page/{page_number}"

    @classmethod
    def __init__(cls, limit: int = 5, proxy=None):
        if not isinstance(limit, int) or limit < 1:
            raise Exception("Invalid limit")
        cls.limit = limit
        cls.proxy = proxy

    # NOTE - This function has a retry to handle cases where the scraping GET request fails due to any reason like website down
    @classmethod
    @retry(max_attempts=3, wait_time=1)
    def get_html(cls, page_number: int) -> bytes:
        """
        This function makes GET request to fetch the HTML from given page number of the host

        Args:
            page_number: current page number

        Returns:
            html content of host
        """
        url = cls.BASE_URL.format(page_number = page_number)
        proxies = {"http": cls.proxy, "https": cls.proxy} if cls.proxy else None
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        return response.content

    @classmethod
    def convert_price_to_float(cls, price:str, title: str):
        """
        This function is used to convert the scraped price from string to int 

        Args:
            price: price of the product
            title: title of the product

        Returns:
            converted price in float/ the price in string if the price is not convertable
        """
        price = price[1:] if price[0] == '₹' else price
        try:
            return float(price)
        except:
            print(f"Failed to convert price to integer for {title}")
        
        return price

    @classmethod
    def store_image(cls, image_url: str, title:str) -> str:
        """
        This function stores the image on local and return the url of path on PC

        Args:
            image_url: url of the image on the web

        Returns:
        the url of image on your local 
        """
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f"product_images/{title}.jpg", "wb") as file: 
                file.write(response.content)
            return f"product_images/{title}.jpg"
        else:
            print(f"Failed to download the image for {title}.")

    @classmethod
    def parse_page_html(cls, page_html, page_number: int) -> list:
        """
        This function parses the page html and extracts the product info 

        Args:
            page_html: bytes of page html that was fetched
        
        Returns:
            final list of dict of scraped product info
        """
        soup = BeautifulSoup(page_html, "html.parser")
        product_cards = soup.select(".product-inner")  
        if not product_cards:
            return []
            
        page_products = []
        for card in product_cards:
            # NOTE - we have to extract name from the link to product page, since the name is unique and complete in that only
            product_anchor_tag = card.select_one(f"h2{cls.PRODUCT_HTML_CLASS_NAMES.get("title")} a")
            title = ""
            if product_anchor_tag:
                product_link = product_anchor_tag.get("href")
                product_name = product_link.split('/')[-2]
                title = product_name.replace('-', ' ').title()
            else:
                continue
            
            price = card.select_one(cls.PRODUCT_HTML_CLASS_NAMES.get("price"))
            if price:
                price = price.get_text(strip=True)
                price =  cls.convert_price_to_float(price, title)
            else:
                price = None
                print(f"Price not available for product: {title} , on page: {page_number}")

            image = card.select_one(cls.PRODUCT_HTML_CLASS_NAMES.get("image"))
            if image:
                image = image.get("data-lazy-src")
                try:
                    image = cls.store_image(image, title)
                except Exception as e:
                    print(f"Unable to save image on PC for {title}. \nError: {e} ")
            else:
                image = ""
                print(f"Image not available for product: {title} , on page: {page_number}")

            if title:
                page_products.append({
                    "product_title":title, 
                    "product_price":price,
                    "path_to_image":image
                })
        return page_products

    @classmethod
    def scrape_data(cls) -> list:
        """
        This function starts the process of scraping and triggers all the functions around it

        Returns:
            list of products that have been scraped
        """
        products = []
        for page_number in range(1, cls.limit + 1):
            page_html = cls.get_html(page_number)
            page_products = cls.parse_page_html(page_html, page_number)
            DBManager.save_update_product_info(page_products)
            products.extend(page_products)
            print(f"Page no. - {str(page_number)} scraped and stored.")
        return products
