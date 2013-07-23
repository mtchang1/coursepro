import urllib2
import bs4
import os

#outputs dictionary of subject area followed by list of reqs
def main():
    #resolve absolute directory path
    root_dir = os.path.abspath(os.path.dirname(__file__))

    user_agent = 'Mozilla/5'
    headers = { 'User-Agent' : user_agent }

    #sending out GET request
    request = urllib2.Request("http://coursecatalog.web.cmu.edu/"
                              "schoolofcomputerscience",
                               None, headers)
    response = urllib2.urlopen(request)

    cdict = {}
    
    #parse html
    keylist = []
    cdata = None
    soup = bs4.BeautifulSoup(response.read()) 
    #EDIT: only scs cs requirements FOR NOW (ie. VERY HACKY)
    count = 7
    for section in soup.findAll('table', class_="sc_courselist"):
        if count == 0:
            break
        else:
            count -= 1
            key = section.find('td',colspan="2").contents[0]
            keylist.append(key)
            clist = section.findAll('a')
            courses = []
            for course in clist:
                courses.append(course.contents[0])
            cdict[key] = courses
        
    for k,v in cdict.items():
        print k
        print v

#now cdict contains the type of course as key and the courses that fulfill 
#this requirement

#SHOULD I USE A DATABASE FOR THIS?

if __name__ == "__main__":
    main(); 
