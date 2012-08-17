import re
import sys
import os
import mechanize
import BeautifulSoup


class Coursera:

    def __init__(self, options):
        self.username = options["user"]
        self.password = options["pass"]
        self.course   = options["course"]

        self.browser  = mechanize.Browser()


    def login(self, course=None):
        if course is None:
            course = self.course

        loginurl  = "https://www.coursera.org/" + course + "/auth/auth_redirector?" + \
                    "type=login&subtype=normal&email="
        homeurl   = "https://class.coursera.org/" + course + "/class/index"

        self.browser.open(loginurl)
        self.browser.select_form(nr=0)
        self.browser.form["email"]    = self.username
        self.browser.form["password"] = self.password
        self.browser.submit()

        main   = self.browser.open(homeurl).read()
        search = re.findall('dropdown_my', main)

        if len(search) == 1:
            return False

        return True


    def getContent(self, course=None):
        if course is None:
            course = self.course

        pageurl = "https://class.coursera.org/" + course + "/lecture/index"
        data    = self.browser.open(pageurl).read()
        html    = BeautifulSoup.BeautifulSoup(data)
        resp    = []

        for i, week in enumerate(html.findAll('h3', {'class':'list_header'})):
            topic = "%02d %s" % (i+1, week.string)
            temp  = []

            for j, lectures in enumerate(week.parent.nextSibling.findAll('li')):
                lecture = "%02d %s" % (j+1, self._strip(lectures.a.contents[0]))
                lecurls = []
               
                for links in lectures.findAll('a'):
                    url = links['href']
                    if 'view?' not in url:
                        lecurls.append(url)

                temp.append((lecture,  lecurls))

            resp.append((topic,  temp))

        return resp


    def _renameFile(self, fname, isFile=True):
        name = re.sub("\([^\(]*$", "", fname)
        name = name.strip().replace(':','-')
        name = re.sub("[^A-Za-z0-9.\(\)\-\_\s]", "", name)

        if isFile:
            name = re.sub("_+", "_", name.replace(' ', '_'))

        return name


    def _strip(self, data):
        return re.sub('(\n|\r|\t)', '', data)




from pprint import pprint as pp
from config import USERNAME, PASSWORD

options = {"user": USERNAME, "pass": PASSWORD, "course": "nlp"}
course = Coursera(options)
course.login()
pp(course.getContent())


