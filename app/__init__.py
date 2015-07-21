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
    dictionary = []
    content = ""
    published = ""
    page = requests.get('http://web.archive.org/web/20121201230949/http://www.americanancestors.org/articles-locations/')
    tree = html.fromstring(page.text)
    countries = ['Canada', 'Connecticut', 'England', 'Holland', 'Ireland', 'Maine', 'Massachusetts', 'New Hampshire', 'New York', 'Rhode Island', 'Vermont', '']
    links = tree.xpath('//a[@target=""]//@href')
    titles = tree.xpath('//a[@target=""]/text()')

    # print 'countries: ', countries
    # print 'Links: ', links
    # print 'Titles: ', titles

    # dictionary = dict(zip(titles, links))
    country = 11
    id = 0
    for x in xrange(0, len(links)):#len(links)):

        author = ""
        content = ""

        if titles[x] == "'Where is Home? New Brunswick Communities Past and Present.'":
            country = 0
        elif titles[x] == "An Annotated Table of Contents for Bailey's Early Connecticut Marriages":
            country=1
        elif titles[x] == "English Origins and Sources I":
            country=2
        elif titles[x] == "Pilgrim Village Families Sketch: Constant Southworth":
            country=3
        elif titles[x] == "Catholic Records and their Use in Irish Research":
            country=4
        elif titles[x] == "Deaths and Funerals at Brooksville, Maine: Recorded in the Nineteenth-Century Diary of Margaret (Lord) Varnum":
            country=5
        elif titles[x] == "Ancestral History in Massachusetts":
            country=6
        elif titles[x] == "Cemetery Research in New Hampshire":
            country=7
        elif titles[x] == "An Easier Way to Obtain New York State Vital Records":
            country=8
        elif titles[x] == "A Few Basic Tools for Rhode Island Research":
            country=9
        elif titles[x] == "A Genealogical Guide to Essential Printed Resources for Vermont":
            country=10

        # print country



        # if titles[x] == "Finding Clues to Immigrant Origins":

        page = requests.get('http://web.archive.org'+links[x])
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
            content = re.sub('http://www.americanancestors.org', 'http://web.archive.org/http://www.americanancestors.org', content)
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
            'content': content.decode('utf-8'),
            'id': id,
        })
        print author
        id += 1


    # jsonDict = json.dumps(dictionary, ensure_ascii=False)
    # with open('articles.json', 'w') as outfile:
    #     json.dump(dictionary, outfile)
        # dictionary = []

        # rendered_template = render_template('vermont.html', dictionary=dictionary)
        # rendered_template = rendered_template
        # dictionary = []
        # pdf = pdfkit.from_string(rendered_template,  "pdfs/" + titles[x] + " - " + author + '.pdf')


    return render_template('vermont.html', dictionary=dictionary)




if __name__ == '__main__':
    app.run()
