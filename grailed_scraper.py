from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import urllib.request
from PIL import Image
import pandas as pd
import os
from urllib.error import HTTPError
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("search", help="Query to find listings on Grailed.com")
parser.add_argument(
    "-w", "--width", help="Set the width of downloaded images", type=int
)
parser.add_argument(
    "-h", "--height", help="Set the height of downloaded images", type=int
)
parser.add_argument("-n", "--num", help="Number of images desired", type=int)


# Scrape images from Grailed query with optional image width/height parameters
webdriver = "chromedriver"
chrome_options = Options()
driver = Chrome(webdriver, options=chrome_options)
url = "https://www.grailed.com/"
driver.get(url)
inputBox = driver.find_element_by_id("globalheader_search")
search_term = "vintage sweaters"

# Search Grailed
inputBox.send_keys(search_term)
inputBox.send_keys(Keys.RETURN)

# Error if search bar not found after 10 seconds
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "shop"))
    )
except TimeoutException:
    print("Loading took too much time!")


# Wait for feed-items to appear
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "listing-cover-photo"))
    )
except TimeoutException:
    print("No photos found this search")

# Target image number
target = 10000
img_width = 200
# lastFeedItem = None
count = 0
all_designers = []
seen = {}
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while count <= target:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")
    time.sleep(SCROLL_PAUSE_TIME)
    listings = driver.find_elements_by_class_name("feed-item")
    listings.reverse()

    # Download images until the we reach a feed-item we've seen before
    for listing in listings:

        if len(listing.find_elements_by_class_name("lazyload-placeholder")) == 0:
            img = listing.find_element_by_tag_name("img")
            url = img.get_attribute("src")

            currDesigner = listing.find_element_by_xpath(
                "//p[contains(@class, 'listing-designer') and contains(@class, 'truncate')]"
            ).text
            currDate = listing.find_element_by_xpath("//span[@class = 'date-ago']").text
            currTitle = listing.find_element_by_class_name("listing-title").text

            if currTitle in seen:
                if seen[currTitle] == currDate:
                    break

            else:
                seen[currTitle] = currDate

                # Use url parameters to download at preferred width
                idx_width = url.index("width")
                idx_height = url.index("height")
                new_url = url[: idx_width + 6] + str(img_width) + url[idx_height + 10 :]

                try:
                    urllib.request.urlretrieve(new_url, str(count) + ".jpg")
                    all_designers.append(currDesigner)
                    count += 1

                except HTTPError as err:
                    print("src threw http error")

    last_height += 1100
    print("downloads: " + str(count) + " feed-items: " + str(len(listings)))


# Save feed-item designer info
df = pd.DataFrame(all_designers, columns=["Designer"])
df.to_csv("designers.csv")
driver.close()
