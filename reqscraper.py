import urllib2
import bs4
import os

def get_prereq(s):
    return get_req(s,"prerequisite")

def get_coreq(s):
    return get_req(s,"corequisite")

#note: reqs can come in the form of:
#1. xx-xxx and xx-xxx
#2. xx-xxx or xx-xxx
#3. (xx-xxx) or (xx-xxx and xx-xxx) [and any variation of this]
def get_req(s,reqtype):
    s = s.lower()
    i = s.find(reqtype)
    # move cursor to start of course number
    while not s[i].isdigit(): i+=1
    course_list = []
    # prereq part ends with <br />
    while s[i] != '<':
        course = ""
        while s[i].isdigit() or s[i] == "-":
            course += s[i]
            i+=1
        if course != "":
            course_list.append(course)
        else:
            i+=1
    return course_list

#takes in list of courses, outputs dictionary of courses + reqs
#def scrape():

def main():
    #resolve absolute directory path
    root_dir = os.path.abspath(os.path.dirname(__file__))

    user_agent = 'Mozilla/5'
    headers = { 'User-Agent' : user_agent }

    #sending out GET request
    request = urllib2.Request("http://coursecatalog.web.cmu.edu"
                              "/ribbit/?page=getcourse.rjs&code=15-150",
                               None, headers)
    response = urllib2.urlopen(request)

    #parse html
    cdata = None
    soup = bs4.BeautifulSoup(response.read())
    for cd in soup.findAll(text=True):
        if isinstance(cd, bs4.CData):
            cdata = cd
    if cdata == None:
        print "Course not found"
        return
    print cdata
    print get_prereq(cdata)
    print get_coreq(cdata)

if __name__ == "__main__":
    main()
