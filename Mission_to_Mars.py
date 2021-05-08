
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Set executable path and set up the url for scraping
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

### Latest News

#Visit the mars nasa news site 
url = 'https://redplanetscience.com'
browser.visit(url)
# Add a delay for loading the page then search for components with the tag div and attribute list_text
browser.is_element_present_by_css('div.list_text', wait_time=1)

#Set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
#assign slide_elem as the variable to look for the ,div/> tag and it's descendent 
slide_elem = news_soup.select_one('div.list_text')


# Use the parent element, slide_elem to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
#when .get_text() was chained onto the metho .find(), only the text of the element is returned


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


### Featured Images

# to get to the full sized version of the featured image on the webpage
#we'll need to click on the image a few times, this requires splinter

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

#there are three buttons on the page so this needs to specify the 
#full image button as the first one...

# Find and click the full image button, identified by its tag
full_image_elem = browser.find_by_tag('button')[1]
#use splinter to click it
full_image_elem.click()

# Parse the resulting html (new page opened) with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#we want to pull whatever image comes up each time the code runs
#not the same image every time
#tell BeautifulSoup to look inside the <img /> tag for an image with the class "fancybox-image" seen in the
#dev tools and use .get('src') to pull the link to the image

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

#the url pulled above is only the partial url that needs to be 
#added to the url base so we can access the photo so we'll add them together here
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


 ### Mars Facts

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

#use the pandas function, .to_html() to convert the Dataframe back into HTML-ready code
df.to_html()

#end the splinter session
browser.quit()


#jupyter notebook was good to write the code in testable chunks
#but it cannot be run automatically in jupyter notebook so it has
#to be converted into a .py file
#to do so: file>download as> Python(.py)
#if you get a warning click "Keep" to continue downloading

