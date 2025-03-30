# amazon_scraper.py
import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_amazon_soft_toys():
    # URL for searching "soft toys" on Amazon.in
    url = "https://www.amazon.in/s?k=soft+toys"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve page")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    # Find all product containers
    products = soup.find_all("div", {"data-component-type": "s-search-result"})
    results = []

    for product in products:
        # Check for "Sponsored" badge in the product container
        sponsored = product.find("span", text="Sponsored")
        if not sponsored:
            continue

        # Extract Title
        title_elem = product.find("span", class_="a-size-medium")
        title = title_elem.get_text(strip=True) if title_elem else "N/A"

        # Extract Brand (this may vary by page structure)
        brand_elem = product.find("span", class_="a-size-base-plus")
        brand = brand_elem.get_text(strip=True) if brand_elem else "N/A"

        # Extract Reviews
        reviews_elem = product.find("span", class_="a-size-base")
        reviews = reviews_elem.get_text(strip=True) if reviews_elem else "0"

        # Extract Rating (example text: '4.5 out of 5 stars')
        rating_elem = product.find("span", class_="a-icon-alt")
        rating = rating_elem.get_text(strip=True).split(" ")[0] if rating_elem else "0"

        # Extract Selling Price (whole part)
        price_elem = product.find("span", class_="a-price-whole")
        price = price_elem.get_text(strip=True) if price_elem else "N/A"

        # Extract Image URL
        img_elem = product.find("img", class_="s-image")
        image_url = img_elem["src"] if img_elem else "N/A"

        # Extract Product URL
        link_elem = product.find("a", class_="a-link-normal")
        product_url = "https://www.amazon.in" + link_elem["href"] if link_elem and link_elem.get("href") else "N/A"

        results.append({
            "Title": title,
            "Brand": brand,
            "Reviews": reviews,
            "Rating": rating,
            "Selling Price": price,
            "Image URL": image_url,
            "Product URL": product_url
        })
        # Be polite and sleep between requests
        time.sleep(1)
    
    return results

if __name__ == "__main__":
    data = scrape_amazon_soft_toys()
    if data:
        keys = data[0].keys()
        with open("amazon_soft_toys_raw.csv", "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print("Scraping complete. Data saved to amazon_soft_toys_raw.csv")
    else:
        print("No data scraped")
