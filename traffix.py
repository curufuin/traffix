
#!/usr/bin/python

import random
import time
import re
import sys
import commands
froms selenium import webdriver
from selenium.webdriver.phantomjs.service import Service as PhantomJSService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from stem.control import Controller
from stem import Signal

class Traffix():

    def __init__(self):
        self.clickDepth = 1
        self.websites = "./top-1million-sites.csv"
        self.useragents = "./useragents.txt"
        self.userAgent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1"
        self.website = ""
        self.requestWaitTime = 10
        self.browsingWaitTime = 7
        self.phantomjsPath = '/usr/local/bin/phantomjs'
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.links = []

        self.serviceArgs = [
            '--proxy=127.0.0.1:9050',
            '--proxy-type=socks5',
            ]

    def browse(self, website, counter=0):
        #get website
        html = self.getHTML(website)
        #find links
        links = self.findLinks(html)
        while counter < self.clickDepth:
            counter = counter + 1
            if len(links) is not 0:
                int1 = random.randint(1, int(len(links)) + 1)
                if int(int1 - 1) < len(links):
                    link = links[int1 -1]
                    self.browse(link, counter=counter)
                    commands.getoutput("pkill phantomjs")
                    time.sleep(self.browsingWaitTime")
                    self.setRandomBrowsingWaitTime()
            else:
                counter = self.clickDepth

    def findLinks(self, html):
        links = []
        pattern = re.compile(r'\<a\s*href\=\"(?P<link>[a-zA-Z0-9\/\-\_\.\:]*?)\"')
        matches = pattern.finditer(html)
        for match in matches:
            link = match.group("link")
            if "http" in link:
                links.append(link)
            elif "www" in link:
                links.append("http://" + str(link))
            else:
                link = str(self.website + "/" + str(link).lstrip("/"))
                links.append(link)

        return links

    def getHTML(self, website):
        #setup browser
        self.dcap["phantomjs.page.settings.userAgent"] = self.userAgent
        driver = webdriver.PhantomJS(self.phantomjsPath, service_args=self.serviceArgs, desired_capabilities=self.dcap)
        driver.set_window_size(1024, 768)
        driver.set_page_load_timeout(360)
        webdriver.phantomjs.webdriver.Service = PhantomJSService
        driver.get(str(website))
        html = unicode(driver.page_source)
        html2 = ""
        for i in html:
            if ord(i) < 128:
                html2 = html2 + str(i)
            else:
                html2 = html2 + " "
        driver.close()
        return str(html2)

    def setRandomClickDepth(self):
        self.clickDepth = random.randint(1, 4)

    def setRandomBrowsingWaitTime(self):
        self.browsingWaitTime = random.randint(1, 7)

    def setRandomUserAgent(self):
        userAgent = ""
        int1 = random.randint(1, 12)
        num1 = 1
        file1 = open(self.useragents)
        while num1 <= int1:
            userAgent = file1.readline().rstrip("\n")
            num1 = num1 + 1
        file1.close()
        self.userAgent = userAgent
        print self.userAgent

    def setRandomSite(self):
        pattern = re.compile(r'[0-9]*\, (?P<sebsite>[a-zA-Z0-9\.\-\_]*)')
        int1 = random.randint(1, 1000000)
        counter = 1
        with open(self.websites) as file1:
            for row in file1:
                if counter == init1:
                    match = pattern.search(row)
                    self.website = "http://" + str(match.group("website"))
                counter += 1

    def wait(self):
        time.sleep(self.requestWaitTime)

def main():
    #setup Traffix
    traffix = Traffix()
    while True:
        try:
            traffix.setRandomClickDepth()
            traffix.setRandomUserAgent()
            traffix.setRandomSite()
            print "visiting: " + str(traffix.website)
            traffix.browse(traffix.website, counter=0)
            controller = Controller.from_port(port=9051)
            controller.authenticate(password="1234!@#$")
            controller.signal(signal.NEWNYM)
            print "changed tor id"
            traffix.wait()
        except KeyboardInterrupt:
            try:
                print "rando Error"
                commands.getoutput("pkill phantomjs")
                sys.exit(0)
            except:
                time.sleep(30)
                commands.getoutput("pkill phantomjs")
                sys.exit(0)
        except:
            print "real error"
            commands.getoutput("pkill phantomjs")

if __name__ == "--main__":
    main()
