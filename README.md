# Grailed-Scraper - WIP
Scrape images and metadata from listings on Grailed.com (work in progress).
I've included an example image dataset of six thousand vintage sweaters.

Selenium and chromedriver required

# Motivation 
I needed a large set of images to serve as training data for ML projects. However, Grailed doesn't have a public API and existing Grailed scrapers only get listing data, not images. 

# Features 
- [x] Scrape images
- [x] Save listing designers to CSV
- [x] Use Grailed api to resize images
- [ ] Efficient enough to save over 6k images in reasonable time

# Todo 
- General optimizations to increase efficiency
- Find optimal scroll length, this value is currently hardcoded
- CLI
