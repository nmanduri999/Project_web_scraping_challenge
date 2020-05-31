from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    import os
    if os.name=="nt":
        executable_path = {'executable_path': './chromedriver.exe'}
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    # time.sleep(5)

def nasa_mars_news():
    browser = init_browser()
    nasa_url = 'https://mars.nasa.gov/news'
    browser.visit(nasa_url)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')
    nasa_news  = []
    for slides in soup.find_all('li', class_='slide'):
        news_title = slides.find_all('div', class_='content_title')[0].text
        news_p = slides.find_all('div', class_='article_teaser_body')[0].text
        nasa_news =  [news_title, news_p]
        break
    browser.quit()
    return nasa_news  

def featured_mars_img():
    browser = init_browser()
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')
    image_url = soup.find('article', class_='carousel_item')['style']
    mars_image_url =image_url.replace('background-image: url(', '').replace(');','')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + mars_image_url
    browser.quit()
    return featured_image_url  

def mars_weather_twitter():
    browser = init_browser()
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    mars_weather = soup.find_all('span')
    for tweet in mars_weather:
        if 'InSight sol' in tweet.text:
            mars_weather = tweet.text
            break
    browser.quit()
    return mars_weather 

def mars_facts_table():
    facts_url = 'https://space-facts.com/mars/'
    facts_tables = pd.read_html(facts_url)
    mars_facts = facts_tables[0]
    mars_facts.columns = ["Description", "Value"]
    mars_facts = mars_facts.set_index("Description")
    mars_table = mars_facts.to_html()
    return mars_table

def mars_hems_imgs():
    browser = init_browser()
    hems_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hems_url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='item')
    hem_title_urls  = []
    main_url = 'https://astrogeology.usgs.gov'  
    for result in results:
        title = result.find('h3').text
        image_url = result.find('a', class_='itemLink product-item')['href']
        image_url = main_url+image_url
        browser.visit(image_url)
        time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        result = browser.links.find_by_text('Sample').first
        enhanced_url = result['href']
        hem_title_urls.append({"Title" : title, "Image_URL" : enhanced_url}) 
    browser.quit()  
    return hem_title_urls


def scrape_info():
    
    mars_info = {}
    nasa_news = nasa_mars_news()
    mars_info["title"] = nasa_news[0]
    mars_info["par"] = nasa_news[1]
    mars_info["featured_image_url"] = featured_mars_img()
    mars_info["mars_weather"] = mars_weather_twitter()
    mars_info["mars_table"] = mars_facts_table()
    mars_info["hem_title_urls"] = mars_hems_imgs()

    # Return results
    return mars_info
