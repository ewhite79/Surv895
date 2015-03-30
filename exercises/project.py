import mechanize
import requests

# try selenium and PhantomJS
from selenium import webdriver

from bs4 import BeautifulSoup

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
test_bs = None
mlive_comment_div_bs = None

# if PhantomJS, set the path to the phantomjs executable.

phantomjs_bin_path = "C:/Users/Emma/node_modules/phantomjs/bin/phantomjs"

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
test_bs = BeautifulSoup( test_html, "html5lib" )

# get div that contains comments by ID
mlive_comment_div_bs = test_bs.find( "div", id="rtb-comments")
print( "- <div id=\"rtb-comments\">: " + str( mlive_comment_div_bs ) )
#print( test_bs )