#######IMPORTS##############################

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

# if PhantomJS, set the path to the phantomjs executable.

phantomjs_bin_path = "C:/Users/Emma/phantomjs-2.0.0-windows/bin/phantomjs.exe"

# example from Windows (must be forward slashes between directories, even though it is Windows):
#phantomjs_bin_path = "C:/Users/jonathanmorgan/AppData/Roaming/npm/node_modules/phantomjs/lib/phantom/phantomjs.exe"
#phantomjs_bin_path = "C:/Users/jonathanmorgan/Downloads/phantomjs-2.0.0-windows/bin/phantomjs.exe"

# set URL you want to test

# MLive page with dynamically loaded comments
test_url = "http://www.mlive.com/lansing-news/index.ssf/2014/05/union_contribution_a_huge_step.html"

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

############FILL ARTICLE TABLE###################

#load more comments
self.selenium.open("class=fyre-stream-more")
self.selenium.click("class=fyre-stream-more")
self.selenium.wait_for_page_to_load("2000")

# declare variables - BeautifulSoup
soup = None
article_text_bs = None
article_author_bs = None

#Other variables
url = ""
author = ""
article_text = ""

# place HTML in BeautifulSoup instance
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
    new_article_id = cursor.lastrowid
    
    # output result
    print("New article inserted with ID = " + str(new_article_id))

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

#################FILL COIMMENT TABLE###############################

#soup variables
comment_div_bs = None
commenter_name_bs = None
comment_text_bs = None

#other variables
comment_id = ""
commenter_id = ""
commenter_name = ""
commenter_rating = ""
comment_text = ""
comment_date = ""
comment_likes = ""


#div where the comments are
comment_div_bs = soup.find( "div", id="rtb-comments")

#loop over comments - each is in its own "article" tag
for article in comment_div_bs.findAll("article"):

    #there is one article tag with nothing in it. skip that one
    if article.has_attr('data-message-id'):

        #comment id is in the article tag, attribute "data-message-id"
        comment_id = article["data-message-id"]
    
        #commenter id is in the article tag too 
        commenter_id = article["data-author-id"]

        #commenter_name is attribute in div with class "fyre-comment-user'
        commenter_name_bs = article.find("div", "fyre-comment-user")
        commenter_name = commenter_name_bs["data-from"]

        #commenter rating is in span with class = fyre-comment-user-rating
        commenter_rating = article.find("span", "fyre-comment-user-rating").string

        #date of comment is in a "time" tag
        comment_date = article.find("time").string

        #text of comment is in div with class "fyre-comment"
        comment_text_bs = article.find ("div", "fyre-comment")
        comment_text = comment_text_bs.get_text()

        #comment likes are in span with class 'fyre-comment-like-count'
        comment_likes = article.find("span", "fyre-comment-like-count").string

        #try except to connect to database and put comment info into table
        try: 

            #connect to database 
            connection = sqlite3.connect( "mlivecomments.sqlite" )

            # set row_factory that returns values mapped to column names as well as list
            connection.row_factory = sqlite3.Row

            #make cursors
            cursor = connection.cursor()
            cursor2 = connection.cursor()

            #sql insert statement
            sql_insert_comment = '''
                INSERT INTO comment_raw (
                    MLIVE_comment_id,
                    MLIVE_commenter_id,
                    commenter_username,
                    MLIVE_commenter_rating,
                    comment_date,
                    comment_text,
                    comment_like_count,
                    article_id
                    )
                VALUES (?,?,?,?,?,?,?,?);
            '''
            
            #execute insert statement
            cursor2.execute(sql_insert_comment,(comment_id, commenter_id, commenter_name,
                commenter_rating,comment_date,comment_text, comment_likes, new_article_id))

            # get ID of each record.
            new_comment_id = cursor2.lastrowid
    
            # output result
            print("New comment inserted with ID = " + str(new_comment_id))

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
    
    else:

        print "found tag with no comment"

#END loop over comments
