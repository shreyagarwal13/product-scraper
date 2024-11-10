# Data scraper in Python

## Description
Developed a scraping tool using Python FastAPI framework to automate the information scraping process from the target website.

## Setup

1. Clone the repo
```
git clone https://github.com/shreyagarwal13/product-scraper.git

```

2. Initialise Environment
```
pipenv shell
```

3. Start the service for scraping
```
uvicorn main:app
```

4. This project uses Redis for in memory caching. Please setup redis on your system to be able to run the service. Follow the instructions [here](https://redis.io/docs/latest/operate/oss_and_stack/install/) to setup Redis on your system.
Post Redis setup run this command to start a redis-server :
```
redis-server
```


## Scraping
To start the scraping please make use the `/scrape` API. 

cURL request to trigger scraping and storage of data
```
curl -X GET "http://127.0.0.1:8000/scrape?limit=5&token=my_static_token"
```
Here, limit is the number of pages to be scraped.

if you have a proxy please use the below curl 
```
curl -X GET "http://127.0.0.1:8000/scrape?limit=5&token=my_static_token&proxy=http://yourproxy:port"
```

## Features
- Scraped data is stored in a file on your local. 
- If scraping  again data is checked in cache and is updated in the db only if the price has changed.
- Status checks and error logs have been added to keep a track of scraping process and notified when complete.
- Retry mechanism for cases where a page cannot be reached because of a destination site server error.
- Static authentication token validation


