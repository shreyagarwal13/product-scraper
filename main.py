from fastapi import FastAPI

from managers.scraper_manager import ScraperManager
from authenticator import Authenticator

app = FastAPI()

@app.get("/scrape")
async def scrape_products(limit: int, proxy: str = None, token: str = "") -> dict:
    """
    route to scrape and return data
    
    Args:
        limit: no. of pages to be scraped
        proxy: proxy server 

    Returns:
        scraped products dict
    """
    Authenticator.verify_token(token)
    products = ScraperManager(limit=limit, proxy=proxy).scrape_data()
    print(f"Scraping completed! Total {str(len(products))} products scraped and stored.")
    return {"products": products}
