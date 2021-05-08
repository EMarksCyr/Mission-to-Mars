#import flask dependencies, Flask to render a template, redirect to another url and create a UR:
#PyMongo to interact with our mongo database, and scraping to convert from jupyter notebook into python
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection using PyMongo
#We'll connect using a URI (similar to a URL) and can connect to our mars_app mongo database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Define the route for the HTML page.
@app.route("/")
def index():
    #use PyMongo to finds "mars" collection in our database
   mars = mongo.db.mars.find_one()
   #Tells Flask to return an HTML template using an index.html file
   #and use the mars collection in MongoDB
   return render_template("index.html", mars=mars)

#Add a route that will be the 'button' of the web app that scrapes for updated data

@app.route("/scrape")
def scrape():
    #assign a new variable that points to out Mongo Database
   mars = mongo.db.mars
   #Create a new variable to hold the newly scraped data using the scrape_all function in the scraping.py file exported from jupyter notebook
   mars_data = scraping.scrape_all()
   #updated the database using .update() with the data stored in mars_data. upsert=True indicates to Mongo to create a new document if one doesnt already exist
   mars.update({}, mars_data, upsert=True)
   #redirect our page back to / where we can see the updated content
   return redirect('/', code=302)

#Tells Flask to run
if __name__ == "__main__":
   app.run()