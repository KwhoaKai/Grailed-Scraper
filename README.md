# Grailed-Scraper - WIP
Scrape images from listings on Grailed.com.
I've included an [example image dataset of six thousand images](https://github.com/KwhoaKai/Grailed-Scraper/blob/master/6k-Sweaters.zip) scraped from the search term "vintage sweaters".

[Selenium](https://selenium-python.readthedocs.io/installation.html) and [chromedriver](https://chromedriver.chromium.org/downloads) required

## Motivation 
I needed a large set of images to serve as training data for ML projects. However, Grailed doesn't have a public API (as of Dec. 2019) and existing Grailed scrapers retrieve listing data, but not images.

## Features 
- [x] Scrape images
- [x] Save listing designers to CSV
- [x] Use Grailed api to resize images
- [ ] Efficient enough to save over 6k images in reasonable time

## Todo 
- General optimizations to increase efficiency
- Find optimal scroll length, this value is currently hardcoded
- CLI
