from src.scrapers.base import BaseScraper

scraper = BaseScraper()
response = scraper.fetch("https://httpbin.org/get")

if response:
    print(f"✅ Success! Status: {response.status_code}")
    print(f"Response preview: {response.json()}")
else:
    print("❌ Failed")