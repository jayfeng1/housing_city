# -*- coding: utf-8 -*-
"""
Created on Sun May 31 13:55:06 2015

@author: Jay
"""
import scrapy
import csv

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

abbr_states = {v: k for k, v in states.items()}
global count
count = 0

def get_urls(cities):
        urls = []
        base = 'http://www.numbeo.com/property-investment/city_result.jsp?country=United+States&city='
        for city in cities:
            state = city.split(',')[1].strip(' ')
            abbr = abbr_states[state]
            new_url = city.split(',')[0] + '%2C+' + abbr
            new_url = new_url.replace(' ','+')
            urls.append(base + new_url)
        return urls
            
def listCreator(fileName):
        with open(fileName, 'rU') as f:
            reader = csv.reader(f)
            choices = list(reader)
        return [item for sublist in choices for item in sublist]

class numbeoItem(scrapy.Item):
    city = scrapy.Field(default='null')
    one_bed = scrapy.Field(default='null')
    three_bed = scrapy.Field(default='null')
    one_bed_min = scrapy.Field(default='null')
    three_bed_min = scrapy.Field(default='null')
    central_one = scrapy.Field(default='null')
    central_three = scrapy.Field(default='null')
    central_one_min = scrapy.Field(default='null')
    central_three_min = scrapy.Field(default='null')
    rank = scrapy.Field()

    
class MySpider(scrapy.Spider):
    name = "numbeo"
    allowed_domains = ["numbeo.com"]
    cities = listCreator('/Users/Jay/Dropbox/Coding Projects/housing_city/list_cities.csv')
    start_urls = get_urls(cities)

    def parse(self, response):
        global count
        count += 1
        item = numbeoItem()
        item['rank'] = count
        city = response.xpath('//span[@itemprop="title"]/text()').extract()[3]
        city, state = city.split(',')[0], states[city.split(',')[1].strip()]
        item['city'] = city + ', ' + state
        prices = response.xpath('//tr[@class="tr_highlighted"]/td[@align="right"]/text()').extract()
        central_prices = response.xpath('//tr[@class="tr_standard"]/td[@align="right"]/text()').extract()
        item['central_one'], item['central_three'] = central_prices[0], central_prices[1]
        item['one_bed'],item['three_bed'] = prices[0], prices[1]
        lower_end = response.xpath('//tr[@class="tr_highlighted"]//div[@class="barTextLeft"]/text()').extract()
        central_lower_end = response.xpath('//tr[@class="tr_standard"]//div[@class="barTextLeft"]/text()').extract()
        item['central_one_min'], item['central_three_min'] = central_lower_end[0], central_lower_end[1]
        item['one_bed_min'],item['three_bed_min'] = lower_end[0], lower_end[1]
        yield item
        
        