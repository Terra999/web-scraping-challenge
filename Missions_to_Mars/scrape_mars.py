from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

# NASA Mars News

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve the parent divs for all paragraphs
    results = soup.find('div', class_='list_text')
    # Scrape the article for titles
    title = results.find('div', class_='content_title').text   
    # Scrape the article paragraph
    paragraph = results.find('div', class_='article_teaser_body').text  

# JPL Mars Space Images - Featured Image

    # URL of the page to be scraped
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    # Retrieve featured image
    results = soup.find('img', class_='headerimage').get('src')
    featured_image_url = f'{url}{results}'


# Mars Facts

    # Identify the url
    url = 'https://galaxyfacts-mars.com/'

    # Use Panda's 'read_html' to parse the url
    tables = pd.read_html(url)
    # Find the correct table
    tables[1]

    # Rename the column headings
    mars_df = tables[1]
    mars_df.columns = ['Feature', 'Measurement']

    # Convert to an html file
    mars_table = mars_df.to_html(classes='table table-striped', index = False)


# Mars Hemispheres

    #URL of the page to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    # Declare an empty list for titles and img_urls
    hemi_image_urls = []

    # Retrieve the parent divs for all images
    results = soup.find_all('div', class_='description')

    # Iterate through the thumb area
    for i in range(len(results)):
        # Create an empty dictionary
        hemi_dict = {}
    
        # Find the href
        image_html = results[i].find(class_='itemLink').get('href')
    
        image_url=f'{url}{image_html}'
        browser.visit(image_url)
    
        # Find the 'Sample' element
        sample_element=browser.find_by_text('Sample').first
    
        # Get the title
        title=browser.find_by_css('h2.title').text
    
        # Add the image href to the dictionary
        hemi_dict['img_url']=sample_element['href']
    
        # Add the image title to the dictionary
        hemi_dict['title']=title
    
        # Append the dictionary to the list 'hemi_image_urls'
        hemi_image_urls.append(hemi_dict)
    
        # Repeat
        browser.back()
    
        # time.sleep(0.5)

    post = {
        'title': title,
        'paragraph': paragraph,
        'image': featured_image_url,
        'mars_facts': mars_table,
        'hemispheres': hemi_image_urls    
        }
    
    browser.quit()
    return post


print("Data Uploaded!")