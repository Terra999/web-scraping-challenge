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
    browser = Browser('chrome', **executable_path, headless=False)

    # Define database and collection
    db = client.mars_db
    collection = db.articles

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve the parent divs for all paragraphs
    results = soup.find('div', class_='list_text')
    # Scrape the article for titles
    title = results.find('div', class_='content_title').text   
    # Scrape the article paragraph
    paragraph = results.find('div', class_='article_teaser_body').text
    
    # Dictionary to be inserted into MongoDB
    post = {
        'title': title,
        'paragraph': paragraph,
    }

    # print(post)

    # Insert dictionary into MongoDB as a document
    collection.insert_one(post)

    # Quit the browser
    browser.quit()

# JPL Mars Space Images - Featured Image

    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of the page to be scraped
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    # Declare an empty list for image url
    featured_image_url = []

    # Retrieve the parent div for the image
    results = soup.find_all('div', class_='floating_text_area')

    # Iterate through the floating text area
    for result in results:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        a = result.find('a')
        link = result.find('a')
        href = link['href']
        image_url = ('https://spaceimages-mars.com/' + href)
        print('-----------')
        print(image_url)
        featured_image_url.append(image_url)
    
        time.sleep(0.5)

    # Click the 'FULL IMAGE' button
    try:
     browser.links.find_by_partial_text('FULL IMAGE').click()
          
    except:
        print("Scraping Complete")
    
    # Dictionary to be inserted into MongoDB
    feature_image_url = {
        'image_url': image_url,
    }
    # Insert dictionary into MongoDB as a document
    collection.insert_one(feature_image_url)

    # Quit the browser
    browser.quit()

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
    mars_df.to_html('mars_data.html', classes='table table-striped', index = False)

# Mars Hemispheres

    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #URL of the page to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

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
    
        time.sleep(0.5)
    

        # print article data
        # print('-----------------')
        # print(hemi_image_urls)
   
    
        # Insert dictionary into MongoDB as a document
        collection.insert_one(hemi_dict)


#     # print article data
    # print('-----------------')
    # print(hemi_image_urls)
   
    
    # Insert dictionary into MongoDB as a document
    collection.insert_one(hemi_dict)

    return results

print("Data Uploaded!")