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


    def getContent(self, pageurl=None):
        if pageurl is None:
            pageurl = "https://class.coursera.org/" + self.course + "/lecture/index"

        data = self.browser.open(pageurl).read()
        html = BeautifulSoup.BeautifulSoup(data)
        resp = []

        for week in html.findAll('h3', {'class':'list_header'}):
            topic = week.string
            temp  = []

            for lectures in week.parent.nextSibling.findAll('li'):
                lecture = self._strip(lectures.a.contents[0])
                lecurls = []
               
                for links in lectures.findAll('a'):
                    url = links['href']

                    if 'view?' not in url:
                        lecurls.append(url)

                temp.append((lecture,  lecurls))

            resp.append((topic,  temp))

        return resp



    def _strip(self, data):
        return re.sub('(\n|\r|\t)', '', data)




from pprint import pprint as pp
from config import USERNAME, PASSWORD

options = {"user": USERNAME, "pass": PASSWORD, "course": "nlp"}
course = Coursera(options)
course.login()
pp(course.getContent())


