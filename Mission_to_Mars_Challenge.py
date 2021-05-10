#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


#Set executable path and set up the url for scraping
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Latest News

# In[3]:


#Visit the mars nasa news site 
url = 'https://redplanetscience.com'
browser.visit(url)
# Add a delay for loading the page then search for components with the tag div and attribute list_text
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


#Set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
#assign slide_elem as the variable to look for the ,div/> tag and it's descendent 
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Use the parent element, slide_elem to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
#when .get_text() was chained onto the metho .find(), only the text of the element is returned


# In[6]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[7]:


# to get to the full sized version of the featured image on the webpage
#we'll need to click on the image a few times, this requires splinter

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[8]:


#there are three buttons on the page so this needs to specify the 
#full image button as the first one...

# Find and click the full image button, identified by its tag
full_image_elem = browser.find_by_tag('button')[1]
#use splinter to click it
full_image_elem.click()


# In[9]:


# Parse the resulting html (new page opened) with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[10]:


#we want to pull whatever image comes up each time the code runs
#not the same image every time
#tell BeautifulSoup to look inside the <img /> tag for an image with the class "fancybox-image" seen in the
#dev tools and use .get('src') to pull the link to the image

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[11]:


#the url pulled above is only the partial url that needs to be 
#added to the url base so we can access the photo so we'll add them together here
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[12]:


#we want to pull a table of facts from a website and use the same table 
#format in our webpage
#instead of scraping each row, we'll use the .read)html() function to scrape the entire table
#create a new dataframe from the HTML table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
#assing columns to the new DataFrame for clarity
df.columns=['description', 'Mars', 'Earth']
#use set_index() to turn the description column into the index, inplace=True means the updated index will remain in place
df.set_index('description', inplace=True)
df


# In[13]:


#use the pandas function, .to_html() to convert the Dataframe back into HTML-ready code
df.to_html()


# ## D1: Scrape High-Res Mars' Hemisphere Images and Titles

# ### Hemispheres

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the resulting html (new page opened) with soup
html = browser.html
hemi_soup = soup(html, 'html.parser')

#Go into the dom object with all of the images
main_page = hemi_soup.find('div', class_='full-content')

#Within the main_page, get all of the info boxes for the images
description_set = main_page.find_all('div', class_= 'description')

#go into the set of descriptions and pull each title and append them to the list
for i in range(len(description_set)):
    description = description_set[i]
    #pull clickable links to full images
    wde_url = browser.find_by_tag('h3')[i]
    
    title = description.find('h3').get_text()
    
    #Click full image link and grab sample link url
    wde_url.click()
    html = browser.html
    fullimg_soup = soup(html, 'html.parser')
    sample_container = fullimg_soup.find('div', class_='downloads')
    image = sample_container.find('a')
    
    #Add title and image link to dictionary, append dict to list
    a = {'title': title, 'image': f"{url}{image['href']}"}
    hemisphere_image_urls.append(a)
    browser.back()
    


# #### 4. Print the list that holds the dictionary of each image url and title.
# hemisphere_image_urls

# In[17]:


hemisphere_image_urls


# In[18]:


# 5. Quit the browser
browser.quit()

