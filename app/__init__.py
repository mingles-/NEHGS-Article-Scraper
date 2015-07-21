# -*- coding: utf-8 -*-
from datetime import datetime
from os import environ
from flask_bootstrap import Bootstrap
from collections import OrderedDict
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,

)
from lxml import html
import lxml.html
import requests
import string
import pdfkit
import re
import json

app = Flask(__name__)
Bootstrap(app)

app.config['DEBUG'] = True


@app.route('/getLinks')
def getLinks():

    with open('articles.txt', 'w') as outfile:
        json.dump(["hello world"], outfile)

    dictionary = []
    content = ""
    published = ""
    page = requests.get(
        'http://web.archive.org/web/20121201230949/http://www.americanancestors.org/articles-locations/')
    tree = html.fromstring(page.text)
    countries = ['Canada', 'Connecticut', 'England', 'Holland', 'Ireland', 'Maine', 'Massachusetts', 'New Hampshire',
                 'New York', 'Rhode Island', 'Vermont', '']
    links = tree.xpath('//a[@target=""]//@href')
    titles = tree.xpath('//a[@target=""]/text()')

    # print 'countries: ', countries
    # print 'Links: ', links
    # print 'Titles: ', titles

    # dictionary = dict(zip(titles, links))
    country = 11
    for x in xrange(0, 2):#len(links)):

        author = ""
        content = ""

        if titles[x] == "'Where is Home? New Brunswick Communities Past and Present.'":
            country = 0
        elif titles[x] == "An Annotated Table of Contents for Bailey's Early Connecticut Marriages":
            country = 1
        elif titles[x] == "English Origins and Sources I":
            country = 2
        elif titles[x] == "Pilgrim Village Families Sketch: Constant Southworth":
            country = 3
        elif titles[x] == "Catholic Records and their Use in Irish Research":
            country = 4
        elif titles[x] == "Deaths and Funerals at Brooksville, Maine: Recorded in the Nineteenth-Century Diary of Margaret (Lord) Varnum":
            country = 5
        elif titles[x] == "Ancestral History in Massachusetts":
            country = 6
        elif titles[x] == "Cemetery Research in New Hampshire":
            country = 7
        elif titles[x] == "An Easier Way to Obtain New York State Vital Records":
            country = 8
        elif titles[x] == "A Few Basic Tools for Rhode Island Research":
            country = 9
        elif titles[x] == "A Genealogical Guide to Essential Printed Resources for Vermont":
            country = 10

        # print country



        # if titles[x] == "Finding Clues to Immigrant Origins":

        page = requests.get('http://web.archive.org' + links[x])
        tree = html.fromstring(page.text)
        author = tree.xpath('//h4/text()')
        published = tree.xpath('//div[@class="PubDate"]//text()')
        contentTree = tree.xpath('//content/*')

        # test = contentTree
        # for element, attribute, link, pos in test.findall():
        #
        #     new_src = link.replace('foo', 'bar') # or element.get('src').replace('foo', 'bar')
        #     element.set('src', new_src)
        # print lxml.test.tostring(html)

        #link = tree.xpath('//a[@href="/web/"]/*')

        # print link

        if len(published) == 0:
            published = ""
        else:
            published = published[1]

        if len(author) == 0:
            author = ""
        else:
            author = author[0]

        for c in contentTree:
            link = "<a href=" + chr(34) + "/web/"
            newlink = "<a href=" + chr(34) + "http://web.archive.org/web/"
            content = content + lxml.html.tostring(c)
            # if not "http://www.americanancestors.org" in content:
            # content = content.replace(link, newlink)
            content = re.sub('/web/.+?/http', 'http', content)
            content = re.sub('http://www.americanancestors.org',
                             'http://web.archive.org/http://www.americanancestors.org', content)
            # else:
            #     content = re.sub('<[^>]+>', '', content)


        # link = "<a href=" + chr(34) + "/web/"
        # newlink = "<a href=" + chr(34) + "http://web.archive.org/web/"
        #
        # content.replace(link, newlink)
        # print content
        # if link in content:
        #     content.replace(link, newlink)

        # print content

        # print lxml.html.tostring(content[0])


        dictionary.append({
            'title': titles[x],
            'country': countries[country].decode('utf-8'),
            'link': links[x],
            'author': author.decode('utf-8'),
            'published': published.decode('utf-8'),
            'content': "",#content.decode('utf-8'),
            'topic': "",
        })
        # print titles[x]

    getTopics(dictionary)
    # import io
    # with io.open('data.txt', 'w', encoding='utf-8') as f:
    #     f.write(unicode(json.dumps(dictionary, ensure_ascii=False)))
    # print unicode(json.dumps(dictionary, ensure_ascii=False))
    # test = [1,2,3]
    #     with open('articles.txt', 'a') as outfile:
    #         json.dump(dictionary, outfile, indent=2)
        # rendered_template = render_template('vermont.html', dictionary=dictionary)
        # rendered_template = rendered_template
        # dictionary = []
        # pdf = pdfkit.from_string(rendered_template,  "pdfs/" + titles[x] + " - " + author + '.pdf')



    return render_template('vermont.html', dictionary=dictionary)


def getTopics(dictionary):
    content = ""
    published = ""
    country = ""
    page = requests.get('http://web.archive.org/web/20121201230949/http://www.americanancestors.org/articles-topics/')
    tree = html.fromstring(page.text)

    links = []
    links_raw = tree.xpath('//a[@target=""]//@href')

    titles = []
    titles_raw = tree.xpath('//a[@target=""]/text()')

    topics_raw = []
    topic = 24
    topics = []
    topic_list = ["African American Family History", "Bible Records", "Canadian Family History", "Computer Genealogist",
              "Ethnic Research", "Family Health Histories", "Genealogy and Technology", "Genetics\DNA Research",
              "Getting Started in Genealogy", "Hot Topics", "Mayflower Research", "Military Research", "Passenger Lists",
              "Royal Descents, Notable Kin, and Printed Sources", "NEXUS Archive: Vol I", "NEXUS Archive: Vol II",
              "NEXUS Archive: Vol III", "NEXUS Archive: Vol IV", "NEXUS Archive: Vol V", "NEXUS Archive: Vol VI",
              "NEXUS Archive: Vol VII", "NEXUS Archive: Vol VIII", "NEXUS Archive: Vol IX", "NEXUS Archive: Vol X", ""]

    # get list of titles
    namelist = []
    for d in dictionary:
        namelist.append(d['title'])

    # add topics
    for x in xrange(0, len(titles_raw)):

        if titles_raw[x] == u"African American Family History Resources at NEHGS":
            topic = 0
        elif titles_raw[x] == u'Mrs. Lucy Hearsey’s Book':
            topic = 1
        elif titles_raw[x] == u"'Where is Home? New Brunswick Communities Past and Present.'":
            topic = 2
        elif titles_raw[x] == u"Computer Genealogist: Documenting Electronic Sources":
            topic = 3
        elif titles_raw[x] == u"Ahnentafel: A German and Yankee Heritage":
            topic = 4
        elif titles_raw[x] == u"Family Health and Genealogy: Compiling a Family Health History: A Primer for Genealogists":
            topic = 5
        elif titles_raw[x] == u"Computer Interests - 'What Program Should I Buy?”'":
            topic = 6
        elif titles_raw[x] == u"Confronted With Cancer":
            topic = 7
        elif titles_raw[x] == u"For Teachers and Parents: Children’s Books - A Bibliography for Young People and Families":
            topic = 8
        elif titles_raw[x] == u"Another Look at Deeds":
            topic = 9
        elif titles_raw[x] == u"“Almost-Mayflower” Descendants in the Carolinas":
            topic = 10
        elif titles_raw[x] == u"An Introduction to Revolutionary War Resources in New England":
            topic = 11
        elif titles_raw[x] == u"Passenger Ship Lists for the Eighteenth Century":
            topic = 12
        elif titles_raw[x] == u"#1 Royal Descents, Notable Kin, and Printed Sources: Assorted Introductory Topics with a Journal and Multi-Ancestor Recommendation":
            topic = 13
        elif titles_raw[x] == u"An Underwood Connection":
            topic = 14
        elif titles_raw[x] == u"Answers to Queries - Nexus Vol. II No. 1":
            topic = 15
        elif titles_raw[x] == u"Answers - Nexus Vol. III No. 1":
            topic = 16
        elif titles_raw[x] == u"Answers - Nexus Vol. IV No. 1":
            topic = 17
        elif titles_raw[x] == u"Answers - Nexus Vol. V No. 1":
            topic = 18
        elif titles_raw[x] == u"Answers - Nexus Vol. VI No. 1":
            topic = 19
        elif titles_raw[x] == u"Answers - Nexus Vol. VII No. 1":
            topic = 20
        elif titles_raw[x] == u"Answers - Nexus Vol. VIII No. 1":
            topic = 21
        elif titles_raw[x] == u"Acquisition News - Ontario and the Canadian West":
            topic = 22
        elif titles_raw[x] == u"'Hollywood Gothic' and the Alabama Three":
            topic = 23

        if topic != 24:
            for d in dictionary:
                if titles_raw[x] == (d['title']):
                    d['topic'] = topic_list[topic]

        # print topic_list[topic]
        topics_raw.append(topic_list[topic])

    # find articles not in countries page
    for i in range(0, len(titles_raw)):
        # print titles_raw[i]
        if titles_raw[i] not in namelist:
            titles.append(titles_raw[i])
            links.append(links_raw[i])
            topics.append(topics_raw[i])


    for x in range(0, 2):#len(titles)):
        author = ""
        content = ""
        print titles[x]
        session = requests.Session()
        session.max_redirects = 200
        page = session.get('http://web.archive.org' + links[x])
        tree = html.fromstring(page.text)
        author = tree.xpath('//h4/text()')
        published = tree.xpath('//div[@class="PubDate"]//text()')
        contentTree = tree.xpath('//content/*')

        # if float(x) % 50.0 == 0.0:
            # print "-------------- x == " + str(x)
        if len(published) == 0:
            published = ""
        else:
            published = published[1]

        if len(author) == 0:
            author = ""
        else:
            author = author[0]

        for c in contentTree:
            link = "<a href=" + chr(34) + "/web/"
            newlink = "<a href=" + chr(34) + "http://web.archive.org/web/"
            content = content + lxml.html.tostring(c)
            # if not "http://www.americanancestors.org" in content:
            # content = content.replace(link, newlink)
            content = re.sub('/web/.+?/http', 'http', content)
            content = re.sub('http://www.americanancestors.org',
                             'http://web.archive.org/http://www.americanancestors.org', content)

        dictionary.append({
            'title': titles[x],
            'country': "",
            'link': links[x],
            'author': author.decode('utf-8'),
            'published': published.decode('utf-8'),
            'content': "",#content.decode('utf-8'),
            'topic': topics[x],
        })

    print json.dumps(dictionary, ensure_ascii=False)
    # outfile = open('data.txt', 'w')
    # outfile.write(json.dumps(dictionary, ensure_ascii=False))
    # outfile.close()



if __name__ == '__main__':
    app.run()
