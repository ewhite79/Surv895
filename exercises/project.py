from __future__ import unicode_literals

import mechanize
import requests

# try selenium and PhantomJS
from selenium import webdriver

from bs4 import BeautifulSoup

#import projects for working with SQLite
import sqlite3
import six

# declare variables
test_url = ""
http_client = ""
HTTP_REQUESTS = "requests"
HTTP_MECHANIZE = "mechanize"
HTTP_PHANTOM_JS = "phantomJS"
test_html = ""

# declare variables - requests and mechanize
response = None

# declare variables - PhantomJS
phantomjs_bin_path = ""
driver = None

# declare variables - BeautifulSoup
soup = None
mlive_comment_div_bs = None
article_text_bs = None
link_list_bs = None
link_bs = None

#declare variables - for SQL
url = ""
author = ""
article_text = ""

# if PhantomJS, set the path to the phantomjs executable.

phantomjs_bin_path = "C:/Users/Emma/phantomjs-2.0.0-windows/bin/phantomjs.exe"

# example from Windows (must be forward slashes between directories, even though it is Windows):
#phantomjs_bin_path = "C:/Users/jonathanmorgan/AppData/Roaming/npm/node_modules/phantomjs/lib/phantom/phantomjs.exe"
#phantomjs_bin_path = "C:/Users/jonathanmorgan/Downloads/phantomjs-2.0.0-windows/bin/phantomjs.exe"

# set URL you want to test

# MLive page with dynamically loaded comments
test_url = "http://www.mlive.com/lansing-news/index.ssf/2014/06/michigan_senate_approves_histo.html"

# tell it what client you want to try.
http_client = HTTP_PHANTOM_JS

# rerieve html based on request_loader
if ( http_client == HTTP_REQUESTS ):

    # retrieve with requests
    response = requests.get( test_url )
    test_html = response.text
    
elif( http_client == HTTP_MECHANIZE ):

    # retrieve with mechanize
    response = mechanize.urlopen( test_url )
    test_html = response.read()

elif( http_client == HTTP_PHANTOM_JS ):
    
    # retrieve with Phantom JS via selenium
    # get PhantomJS Selenium Driver
    driver = webdriver.PhantomJS( phantomjs_bin_path ) # or add to your PATH
    #driver = webdriver.PhantomJS() # or add to your PATH

    # set up virtual window
    driver.set_window_size(1024, 768) # optional

    # grab page.
    driver.get( test_url )

    # save screenshot.
    driver.save_screenshot('screen.png') # save a screenshot to disk

    # get HTML source
    test_html = driver.page_source

#-- END check to see what request loader we are using. --#
    
# place HTML in BeautifulSoup
soup = BeautifulSoup( test_html, "html5lib" )

#get article author 
article_author_bs = soup.find("span", "author vcard").string

#get article text
article_text_bs = soup.find ("div", "entry-content")
article_text = article_text_bs.get_text()


#try except to connect to database and put article info into table
try: 

    #connect to database 
    connection = sqlite3.connect( "mlivecomments.sqlite" )

    # set row_factory that returns values mapped to column names as well as list
    connection.row_factory = sqlite3.Row

    #make cursors
    cursor = connection.cursor()
    cursor2 = connection.cursor()

    #sql insert statement
    sql_insert_article = '''
        INSERT INTO article_raw (
            url,
            author,
            article_text
            )
        VALUES (?,?,?);
    '''
        
        
    #execute insert statement
    cursor.execute(sql_insert_article,(test_url, article_author_bs, article_text))

    # get ID of each record.
    new_user_id = cursor.lastrowid
    
    # output result
    print("New record inserted with ID = " + str(new_user_id))

    #commit
    connection.commit()

except Exception as e:
    
    print( "exception: " + str( e ) )
    
finally:

   # close cursor
    cursor.close()
    cursor2.close()

    # close connection
    connection.close()

#-- END try-->except-->finally around database access. --#

# get div that contains comments by ID
#mlive_comment_div_bs = test_bs.find( "div", id="rtb-comments")
#print( "- <div id=\"rtb-comments\">: " + str( mlive_comment_div_bs ) )
#print( test_bs )
