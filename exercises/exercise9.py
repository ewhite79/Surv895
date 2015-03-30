# import beautiful soup and urlopen function
from bs4 import BeautifulSoup
from urllib2 import urlopen

# set a variable for base domain
BASE_URL = "http://www.chicagoreader.com"

#define a function for creating a Beautiful Soup instance
def make_soup(url):

	#open file
    html = urlopen(url).read()

    #return instance
    return BeautifulSoup(html, "lxml")

######################find category URLS#####################################

#create a beautiful soup instance
soup = make_soup("http://www.chicagoreader.com/chicago/best-of-chicago-2011-food-drink/BestOf?oid=4106228")

#find <dl> element with class "boccat" and store it in a variable
boccat = soup.find ("dl", "boccat")

#define category_links as list
category_links = []

for dd in boccat.findAll("dd"):

    #append the link (concatenated with the base domain)
    category_links.append(BASE_URL + dd.a["href"])

########################make dictionary with winners, etc##############

winnerlist= []

#loop over categorys in list you already made
for category in category_links:

    #create a Beautiful Soup instance
    soup = make_soup(category)

    #find the category title from the h1 headline
    category_title = soup.find("h1","headline").string

    category_winner = ""

    #find the winners ffrom h2, boc1
    for h2 in soup.findAll("h2","boc1"):

        category_winner = [h2.string]

    #find the runners up from h2, boc2    
    for h2 in soup.findAll("h2","boc2"):
        
        runners_up = [h2.string]

    data={"category": category_title,"url": category, "winner": category_winner,"runners_up": runners_up}

    winnerlist.append(data)

#end loop

#print winnerlist
print winnerlist
