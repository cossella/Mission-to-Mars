import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def scraper():
    all_data = {}
    title_p = marsNews()
    all_data["mars_news"] = output[0]
    all_data["mars_paragraph"] = output[1]
    all_data["mars_image"] = marsImage()
    all_data["mars_weather"] = marsWeather()
    all_data["mars_facts"] = marsFacts()
    all_data["mars_hemispheres"] = marsHemispheres()
    return all_data


def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    title_p = [news_title, news_p]
    return title_p


def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    print(featured_image_url)
    return featured_image_url


def marsWeather():
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    twitter = requests.get(weather_url)
    tweet = bs(twitter.text, 'html.parser')
    mars_weather = tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    return mars_weather


def marsFacts():
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)
mars_facts = pd.read_html(facts_url)
mars_facts = pd.DataFrame(mars_facts[0])
mars_facts.columns = ["Description", "Value"]
mars_facts = mars_facts.set_index("Description")
mars_table = mars_facts.to_html(header = False, index = False)
print(mars_table)


def marsHemispheres():
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)
html = browser.html
soup = bs(html, "html.parser")
mars_hemispheres = []

items = soup.find("div", class_ = "result-list" )
hemispheres = items.find_all("div", class_="item")

for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup = bs(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    mars_hemispheres.append({"title": title, "img_url": image_url})
return mars_hemispheres