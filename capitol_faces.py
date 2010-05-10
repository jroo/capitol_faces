# capitol_faces.py
# Updated 05/08/2010, Joshua Ruihley
# grabs images of lawmakers from Yahoo Image Search and saves them locally
#
# Yahoo Image Search API Documentation: http://developer.yahoo.com/search/image/V1/imageSearch.html

from BeautifulSoup import BeautifulStoneSoup
import csv, httplib2, time, urllib, urllib2

LEGISLATOR_SOURCE = "legislators.csv"

#Yahoo API Values
YAHOO_APP_ID = ''  #Your Yahoo Developer Network App ID
YAHOO_SEARCH_URL = 'http://search.yahooapis.com/ImageSearchService/V1/imageSearch' #URL For Yahoo Image Search Requests
MAX_RESULTS = 50 #maximum number of results allowed by Yahoo
TOTAL_RESULTS = 200 #total number of results to return

def grab_images(lawmaker_name, bioguide_id):
    
    http = httplib2.Http()
    start_row = 0
    xml_list = []
    image_id = 0
    
    while (start_row < TOTAL_RESULTS):
        params = urllib.urlencode({
            'query': lawmaker_name,
            'start': start_row,
            'results': MAX_RESULTS,
            'appid': YAHOO_APP_ID,
        })
        
    	url = "%s?%s" % (YAHOO_SEARCH_URL, params)
    	response, content = http.request(url)
    	if response.status == 200:
    	    soup = BeautifulStoneSoup(content)
    	    results = soup.findAll('result')
    	    for result in results:
    	        save_locally(result.url.contents[0], bioguide_id, image_id)
    	        image_id = image_id + 1
                time.sleep(1)
    	
    	start_row = start_row + MAX_RESULTS
        
def format_legislator_name(title, first_name, last_name, nickname):
    if nickname.strip() != "":
        first_name = nickname
    return"%s %s %s" % (title, first_name, last_name)
    
def save_locally(url, bioguide_id, image_id):
    try:
        extension = url.split('/')[len(url.split('/')) - 1]
        file_name = "%s_%s.%s" % (bioguide_id, image_id, extension)
        remote_file = urllib2.urlopen(url)
        local_file = open(file_name, "w")
        local_file.write(remote_file.read())
        local_file.close
        print url
    except:
        pass
	    
#loop through each lawmaker in legislators.csv and save first 200 images
data_reader = csv.reader(open(LEGISLATOR_SOURCE))
for i, row in enumerate(data_reader):
    if i > 0:
        title = row[0]
        first_name = row[1]
        last_name = row[3]
        nickname = row[5]
        
        full_name = format_legislator_name(title, first_name, last_name, nickname)
        bioguide_id = row[17]
        
        grab_images(full_name, bioguide_id)  
