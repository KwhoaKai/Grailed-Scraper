from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import urllib.request
import pandas as pd
import os
from urllib.error import HTTPError
import argparse

# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument("search", help="Query to find listings on Grailed.com")
parser.add_argument(
    "-w", "--width", help="Set the width of downloaded images", type=int, default=0
)
parser.add_argument(
    "-he", "--height", help="Set the height of downloaded images", type=int, default=0
)
parser.add_argument("-n", "--num", help="Number of images desired", type=int, default=0)
args = parser.parse_args()
search_term = args.search
img_width = args.width if args.width > 0 else None
img_height = args.height if args.height > 0 else None
target = args.num if args.num > 0 else 1000

# Welcome :)
print("Hi there! " + str(target) + " listing images for '" + search_term + "' coming right up <3")

# Scrape images from Grailed query with optional image width/height parameters
def GrailedScraper(search_term, img_width, img_height, target):
    webdriver = "./chromedriver"
    chrome_options = Options()
    driver = Chrome(webdriver, options=chrome_options)
    url = "https://www.grailed.com/"
    driver.get(url)
    input_box = driver.find_element_by_id("globalheader_search")

    # Search Grailed
    input_box.send_keys(search_term)
    input_box.send_keys(Keys.RETURN)

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
        print("No listings showed up after 10 seconds!")

    count = 0
    all_designers = []
    seen = {}
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    height_diff = driver.execute_script("return document.body.scrollHeight")

    while count < target:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, " + str(height_diff) + ");")
        time.sleep(SCROLL_PAUSE_TIME)
        listings = driver.find_elements_by_class_name("feed-item")
        listings.reverse()

        # Download images until we reach a feed-item we've seen before, then scroll down to load more images
        for listing in listings:
            is_loaded = len(listing.find_elements_by_class_name("lazyload-placeholder")) == 0
            still_more = count < target
            if is_loaded & still_more:
                try:
                    img = listing.find_element(By.TAG_NAME, "img")
                    url = img.get_attribute("src")

                    curr_designer = listing.find_element_by_class_name("listing-designer").text
                    curr_date = listing.find_element_by_class_name("date-ago").text
                    curr_title = listing.find_element_by_class_name("listing-title").text

                    if curr_title in seen:
                        if seen[curr_title] == curr_date:
                            break

                    else:
                        seen[curr_title] = curr_date

                        # Use url parameters to download at preferred width
                        idx_width = url.index("width")
                        idx_height = url.index("height")

                        if (img_height == None) & (img_width == None):
                            new_url = url[: idx_width + 6] + "200" + url[idx_height + 10 :]

                        elif (img_height == None) & (img_width != None):
                            new_url = (
                                url[: idx_width + 6] + str(img_width) + url[idx_height + 10 :]
                            )

                        elif (img_height != None) & (img_width == None):
                            new_url = (
                                url[:idx_width]
                                + "height:"
                                + str(img_height)
                                + url[idx_height + 10 :]
                            )

                        elif (img_height != None) & (img_width != None):
                            new_url = (
                                url[: idx_width + 6]
                                + str(img_width)
                                + ","
                                + "height:"
                                + str(img_height)
                                + url[idx_height + 10 :]
                            )

                        try:
                            urllib.request.urlretrieve(new_url, str(count) + ".jpg")
                            all_designers.append(curr_designer)
                            count += 1
                            print("Downloaded: " + str(count) + " Target: " + str(target))
                            #print("downloads: " + str(count) + " feed-items: " + str(len(listings)))

                        except HTTPError as err:
                            print("Listing's image threw an HTTP error when trying to download")

                # Listing was lazy-loaded but still doesn't have an image     
                except:
                    print("Skipping listing: Lazy-loaded but still doesn't have cover-photo URL")

        # Distance to scroll
        height_diff += 1100

    # Save feed-item designer info to csv
    df = pd.DataFrame(all_designers, columns=["Designer"])
    df.to_csv("designers.csv")
    driver.close()

GrailedScraper(search_term, img_width, img_height, target)
