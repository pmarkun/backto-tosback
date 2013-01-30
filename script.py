from lxml import etree
from lxml.html import parse
import urllib2, datetime, simplejson
import os, glob
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def retrieveToS(xml):
    site = {}
    site['name'] = xml.xpath('/sitename')[0].get('name')
    site['url'] = xml.xpath('/sitename/docname/url')[0].get('name')
    site['xpath'] = xml.xpath('/sitename/docname/url')[0].get('xpath')

    tos_site = urllib2.urlopen(site['url'])
    tos = parse(tos_site).getroot()

    site['tos'] = tos.xpath(site['xpath'])[0].text_content()
    site['retrieved'] = datetime.datetime.strftime(datetime.datetime.now(), DATETIME_FORMAT)
    return site

for filename in os.listdir("rules"):
    print 'reading ' + filename
    try:
        xml = etree.parse(open('rules/' + filename, 'r')).getroot()
        tos = simplejson.dumps(retrieveToS(xml), sort_keys=True, indent=4 * ' ')
        json = open('json/' + filename[:-4] + '.json', 'w')
        json.write(tos)
        json.close()
    except:
        print "erro reading" + filename
