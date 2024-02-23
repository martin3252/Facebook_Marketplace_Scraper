# facebook-marketplace-scraper


```diff
You use the software provided at your own risk. I cannot be held responsible for any potential consequences, including potential bans from Meta.
```
### Overview
This open-source program uses Python to scrape data from Facebook Marketplace. The program uses Playwright to navigate the Facebook Marketplace website and BeautifulSoup to parse the HTML and extract relevant data. It then displays the results in a Streamlit GUI.

### Customization
This program can be customized to your personal/organizational needs. For more information, please get in touch with me at coldder159@gmail.com
- Streamlit
- Playwright
- BeautifulSoup 
  
### Language: 
- [Python](https://www.python.org/)
  
### Flow diagrams:

### Requirements:
- Python 3.x
- Playwright
- Streamlit
- BeautifulSoup 
  
### Modules:
- Playwright for web crawling
- BeautifulSoup for HTML parsing
- FastAPI for API creation
- JSON for data formatting
- Uvicorn for running the server
 
### API:
- Root: Displays a welcome message
- Data scraping: Parameters include city, query, and max price
- IP information retrieval
  
### Implementation
- Browser automation and data scraping using Playwright
- HTML content parsing with BeautifulSoup
- Data returned in JSON format
- Application server run using Uvicorn

### Features:
- List of supported cities for scraping.
- User inputs for city, search query, and maximum price.
- Submission button to start scraping.
- Display of scraping results including number of results, images, prices, locations, and item URLs.

### How to run:
- python3 app.py
- Streamlit run gui.py

### This repository is based on https://github.com/passivebot/facebook-marketplace-scraper
