from selenium import webdriver
from bs4 import BeautifulSoup

import csv
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

chrome_version = '114.0.5735.90'



# Input search query
search_query = input("Enter search query: ")

# Set up the Chrome WebDriver (make sure you have chromedriver installed and its path configured)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Visit the YouTube search results page
search_url = f"https://www.youtube.com/results?search_query={search_query}"
driver.get(search_url)


# Get the current time
#start_time = time.time()
#or time.time() - start_time > 3:  # no more new videos loaded or 3 seconds have passed

# Scroll down to the bottom of the page until no more new videos are loaded or 3 seconds have passed
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)  # wait for the new videos to load
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Get the HTML content after the page has loaded
html_code = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_code, 'html.parser')

# Extracting all video elements
video_elements = soup.find_all('ytd-video-renderer')

# Initialize lists to store video details
titles = []
links = []
views = []
release_dates = []
channel_names = []

# Iterate over video elements
for video_element in video_elements:
    # Extract title
    title_element = video_element.find('a', id='video-title')
    title = title_element.text.strip() if title_element else None
    titles.append(title)
    # Extract link
    link_element = video_element.find('a', id='video-title')
    link = 'https://www.youtube.com' + link_element['href'] if link_element else None
    links.append(link)

    # Extract views
    views_element = video_element.find('span', class_='inline-metadata-item style-scope ytd-video-meta-block')
    view_count = views_element.text.strip() if views_element else None
    views.append(view_count)
    # Extract release date
    release_date_elements = video_element.find_all('span', class_='inline-metadata-item style-scope ytd-video-meta-block')
    release_date = release_date_elements[1].text.strip() if len(release_date_elements) > 1 else None
    release_dates.append(release_date)
    # # Extract views and release date from aria-label
    # aria_label = link_element['aria-label'] if link_element else None
    # if aria_label:
    #     match = re.search(r'by [^ ]+ ([\d,]+ views) ([^ ]+ ago)', aria_label)
    #     if match:
    #         views.append(match.group(1))  # view count is the first group
    #         release_dates.append(match.group(2))  # release date is the second group
    #     else:
    #         views.append(None)
    #         release_dates.append(None)
    # else:
    #     views.append(None)
    #     release_dates.append(None)

    # Extract channel name
    channel_name_element = video_element.find('tp-yt-paper-tooltip', class_='style-scope ytd-channel-name')
    channel_name = channel_name_element.text.strip() if channel_name_element else None
    channel_names.append(channel_name)

# # Print results
# for title, link, view, release_date, channel_name in zip(titles, links, views, release_dates, channel_names):
#     print("Title:", title)
#     print("Link:", link)
#     print("Views:", view)
#     print("Release Date:", release_date)
#     print("Channel Name:", channel_name)

filename = "{}.csv".format(search_query)

# Open a new CSV file with write permission
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Title", "Link", "View Count", "Release Date", "Channel Name"])
    # Write the data
    for title, link, view_count, release_date, channel_name in zip(titles, links, views, release_dates, channel_names):
        writer.writerow([title, link, view_count, release_date, channel_name])