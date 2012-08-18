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

        self.browser            = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) \
                                    Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.browser.set_handle_robots(False)


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
            topic = "%02d - %s" % (i+1, week.string)
            temp  = []

            for j, lectures in enumerate(week.parent.nextSibling.findAll('li')):
                lecture = "%02d %s" % (j+1, self._strip(lectures.a.contents[0]))
                lecurls = []
               
                for links in lectures.findAll('a'):
                    url = links['href'].replace('%2F', '/')
                    if 'view?' not in url:
                        lecurls.append(url)

                temp.append((lecture,  lecurls))

            resp.append((topic,  temp))

        return resp


    def downloadTree(self, course=None):
        if course is None:
            course = self.course

        content = self.getContent(course)

        for topic in content:
            topicName = self._renameFolder(topic[0])
            pathName  = 'nlp' + '/' + topicName + '/'

            print "\n" + ' >> ' + topicName 

            for lecture in topic[1]:
                lectureName = self._renameFolder(lecture[0])
                dlPathName  = pathName + lectureName + '/'

                try:
                    os.makedirs(dlPathName)
                except OSError as e:
                    if e.errno != 17:
                        raise e
                    pass
                    
                print " " * 6 + lectureName

                for link in lecture[1]:
                    fileName = self._renameFile(link, lectureName)
                    filePath = dlPathName + fileName
                    self.downloadFile(link, filePath)


    def downloadFile(self, url, fileName):
        if os.path.exists(fileName):
            print " " * 8 + " - %s (Already Saved)" % fileName.split('/')[-1]
        else:
            print " " * 8 + "- %s" % fileName.split('/')[-1]
            #print "    -  URL: %s" % url

            try:
                self.browser.retrieve(url, fileName, self._progressBar)
            except KeyboardInterrupt:
                if os.path.exists(fileName):
                    os.remove(fileName)
                raise
            except Exception, e:
                if os.path.exists(fileName):
                    os.remove(fileName)
                print "       Error: %s" % e


    def _renameFile(self, url, name):
        allowed = ['ppt', 'pptx', 'doc',  'docx', 'pdf',
                   'srt', 'txt',  'mp3',  'zip',  'mp4',
                   'exe', 'xls',  'xlsx', 'flv',  'wmv']

        fname = None
        name  = re.sub("\([^\(]*$", "", name)
        name  = name.strip().replace(':','-')
        name  = re.sub("[^A-Za-z0-9\.\(\)\_\s\:]", "", name)
        name  = re.sub("_+", "_", name.replace(' ', '_'))

        # file extension
        if url.split('.')[-1] in allowed:
            fname = url.split('/')[-1]

        if url.split('format=')[-1] in allowed:
            fname = name + '.' + url.split('format=')[-1]

        if fname is None:
            ext = re.search("(\w+)(?:\?.*)?$", url).group(1)
            if ext in allowed:
                fname = name + '.' + ext

        return re.sub('_+', '_', fname)


    def _renameFolder(self, name):
        name = re.sub("[^A-Za-z0-9\.\(\)\_\s\-\:]", "", name)
        name = re.sub(" +", " ", name)

        return name


    def _progressBar(self, blocknum, bs, size):
        if size > 0:
            if size % bs != 0:
                blockCount = size/bs + 1
            else:
                blockCount = size/bs

            fraction = float(blocknum)/blockCount
            width    = 50

            stars    = '*' * int(width * fraction)
            spaces   = ' ' * (width - len(stars))
            progress = '    [%s%s] (%s%%)' % (stars, spaces, int(fraction * 100))

            if fraction*100 <= 99:
                sys.stdout.write(progress)

                if blocknum < blockCount:
                    sys.stdout.write('\r')
                else:
                    sys.stdout.write('\n')
            else:
                sys.stdout.write('    ' + '  ' * width + '\r')
                sys.stdout.flush()


    def _strip(self, data):
        return re.sub('(\n|\r|\t)', '', data)




from pprint import pprint as pp
from config import USERNAME, PASSWORD

options = {"user": USERNAME, "pass": PASSWORD, "course": "nlp"}
course = Coursera(options)
course.login()
course.downloadTree()
#course.downloadFile( 'https://class.coursera.org/nlp/lecture/download.mp4?lecture_id=6', course._renameFile('01 Defining Minimum Edit Distance.mp4', True))

