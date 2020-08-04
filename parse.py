from selenium import webdriver
from urllib.parse import urlencode
import webbrowser
import sqlite3

options = webdriver.ChromeOptions()

options.add_argument('headless')

browser = webdriver.Chrome(options=options)

conn = sqlite3.connect('gmap.sqlite')

cur = conn.cursor()

cur.executescript('''
    DROP TABLE IF EXISTS gdata;

    CREATE TABLE gdata(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Name TEXT,
    Rating TEXT,
    Detail TEXT,
    Location TEXT,
    Closing_time TEXT,
    Phone TEXT
    )
    ''')

gmapsurl = "https://www.google.com/maps/search/?api=1&"
#url = "https://www.google.com/maps/place/Mall+Of+Mysore/@12.2975437,76.6622001,17z/data=!3m1!4b1!4m5!3m4!1s0x3baf7018a81e0e5d:0x5b736aafd8221b5d!8m2!3d12.2975437!4d76.6643888"
#place = input("Enter the place : ")


search = input("What are u looking for? ")

mydict = {"query": search}

#gmapsurl = f"https://www.google.com/maps/search/{search}+near+{place}/"

url = gmapsurl + urlencode(mydict)
print(url)
global no
no = 1
browser.get(url)

while 1:
    try:
        titles = browser.find_elements_by_class_name("section-result-title")
        ratings = browser.find_elements_by_class_name("section-result-rating")
        details = browser.find_elements_by_class_name("section-result-details")
        locations = browser.find_elements_by_class_name("section-result-location")
        description = browser.find_elements_by_class_name("section-result-descriptions")
        openings = browser.find_elements_by_class_name("section-result-opening-hours")
        phone_nos = browser.find_elements_by_class_name("section-result-phone-number")

        
        for title,rating,detail,location,opening,phone in zip(titles,ratings,details,locations,openings,phone_nos):
            print('\nNo :',no)
            print('Tiltle :',title.text)
            print('Rating :',rating.text)
            print('Detail :',detail.text)
            print('Location :',location.text)
            print('Opens at :',opening.text)
            print('Phone no: ',phone.text)
            no += 1
            cur.execute('''INSERT INTO gdata (Name, Rating, Detail, Location, Closing_time, Phone)
                VALUES (?,?,?,?,?,?)''',(title.text,rating.text,detail.text,location.text,opening.text,phone.text,))
        
        browser.find_element_by_id("n7lv7yjyC35__section-pagination-button-next").click()
        conn.commit()
    
    except:
        print("that's all the results!")
        break







