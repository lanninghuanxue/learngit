from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from Crawler.items import ListItem, MetaItem, DownItem
from pymongo import MongoClient
from scrapy import log
from scrapy.http import Request
from bson.objectid import ObjectId

class LiquSpider(BaseSpider):
	name = 'LiquSpider'
	allowed_domains = ['www.liqucn.com']

	modeList = ['list', 'meta', 'down']
	mode = modeList[0]

	inited = False

	def __init__(self, mode, *args, **kwargs):
		super(AnzhiSpider, self).__init__(*args, **kwargs)
		self.start_urls = []

		if mode not in self.modeList:
			mode = self.modeList[0]
		self.mode = mode

		if self.mode == 'list':
			self.start_urls.append('http://www.liqucn.com/rj/c/286/')
		elif self.mode == 'meta':
			client = MongoClient()
			db = client.meta_crawler
			listItems = db.list_items
			for oneItem in listItems.find():
				self.start_urls.append(oneItem['url'])
		elif self.mode == 'down':
			self.start_urls.append('http://www.liqucn.com/rj/c/286/')

	def parse(self,response):
		sel = Selector(response)
		if self.mode == self.modeList[0]:
			nextRetUrl =  ''.join(sel.xpath('//div[@class="page"]/a/@href').extract())
			if nextRetUrl != []:
				yield Request('http://www.liqucn.com/rj/c/286/'+nextRetUrl, callback = self.parse)

			for url in sel.xpath('//a[@class="pic"]/@href').extract():
				listItem = ListItem()
				listItem['mode'] = self.mode
				listItem['market'] = 'liqu'
				listItem['url'] = 'http://www.liqucn.com'+url
				yield listItem

		elif self.mode == 'meta':
			metaItem = MetaItem()
			metaItem['mode'] = self.mode
			metaItem['market'] = 'liqu'
			metaItem['url'] = response.url
			metaItem['title'] = sel.xpath('//div[@class="app_leftinfo"]/h1/text()').extract()
			metaItem['version'] = ''
			metaItem['desc'] = sel.xpath('//div[@class="p_info"]/text()').extract()

			yield metaItem
		elif self.mode == 'down':
			if self.inited == False:
				self.inited = True
				client = MongoClient()
				db = client.meta_crawler
				downItems = db.down_items
				metaItems = db.meta_items
				for oneItem in downItems.find({}, {'liqu':1, '_id':0}):
					for oneId in oneItem['liqu']:
						result = metaItems.find_one({'_id': ObjectId(oneId)}, {'url':1, '_id':0})
						request = Request(result['url'], callback = self.parse)
						request.meta['oid'] = oneId
						yield request
			else:
				downItem = DownItem()
				downItem['mode'] = self.mode
				downItem['url'] = sel.xpath('//li[@class="btn_normal"]/@href').extract()
				downItem['oid'] = response.meta['oid']
				yield downItem


