# -*- coding: UTF-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from scrapy1.items import TaobaoItem
import re
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver

class TaobaoTshirt_Spider(Spider):
	count = 0
	name ='taobao1'
	url = 'https://s.taobao.com/search?q=t%E6%81%A4&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&ntoffset=6&s='
	num =0
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	}
	item = TaobaoItem()
	def start_requests(self):
		url = self.url+str(self.num)
		self.num += 44
		fo = open('taobao1.log','w')
		sys.stdout = fo
		print url
		yield Request(url,headers =self.headers)
	def parse(self,response):
		print '============================='
		datas = response.xpath('//script/text()').extract() 
		if datas:
			print '=============================beginning'
			pattern = re.compile('"raw_title":"(.*?)",.*?"detail_url":"(.*?)",.*?"view_price":"(.*?)",.*?"item_loc":"(.*?)","view_sales":"(.*?)",.*?"nick":"(.*?)",',re.S)
			contents = re.findall(pattern,str(datas))
			for content in contents:
				#import chardet
				#fencoding=chardet.detect(content[4])
				#print fencoding
				print content[5].decode("unicode_escape").encode('utf-8')
				print content[3].decode("unicode_escape").encode('utf-8')
				print content[0].decode("unicode_escape").encode('utf-8')
				print content[2].decode("unicode_escape").encode('utf-8')
				print content[4].decode("unicode_escape").encode('utf-8')
				print '============================='
				detail_url = 'https:'+ content[1].decode('unicode_escape').decode("unicode_escape").encode('utf-8')
				print detail_url
				self.get_nextdetails(detail_url)
				self.item['store_name'] =content[5].decode("unicode_escape").encode('utf-8')
				self.item['store_location'] =content[3].decode("unicode_escape").encode('utf-8')
				self.item['goods_name'] =content[0].decode("unicode_escape").encode('utf-8')
				self.item['price'] =content[2].decode("unicode_escape").encode('utf-8')
				self.item['sales'] =content[4].decode("unicode_escape").encode('utf-8')
				self.count += 1
				print self.count
				if self.count <200:
					yield self.item
					time.sleep(1)
				else:
					break
		if self.count < 200:
			url = self.url+str(self.num)
			self.num += 44
			yield Request(url,headers =self.headers)
		#item = TaobaoItem()
	def get_nextdetails(self,url):
		service_args=[]
		service_args.append('--load-images=no')  ##关闭图片加载
		service_args.append('--disk-cache=yes')  ##开启缓存
		service_args.append('--ignore-ssl-errors=true') ##忽略https错误
		service_args.append('--ssl-protocol=any')
		browser=webdriver.PhantomJS(service_args=service_args)#PhantomJS
		#chrome_options = webdriver.ChromeOptions()
		#prefs = {"profile.managed_default_content_settings.images":2}
		#chrome_options.add_experimental_option("prefs",prefs)
		#browser = webdriver.Chrome(chrome_options=chrome_options)
		browser.get(url)
		time.sleep(3)
		#browser.save_screenshot('E:\\mygit1\\scrapy\\scrapyspider\\1123.png')
		print '=================================6666666666!!!!'
		try:
			results = browser.find_elements_by_xpath("//span[@class='tm-count']")
			print u'month_sales:',results[0].text
			print u'review_num:',results[1].text
			
			self.item['month_sales'] = results[0].text
			self.item['reviews'] = results[1].text
		except:
			results = browser.find_elements_by_xpath("//em[@class='J_ReviewsCount']")
			print u'未知月销量'
			print u'review_num:',results[0].text
			self.item['month_sales'] = u'   未知'
			self.item['reviews'] = results[0].text
			
		else:
			print u'ok=====go on '
			
		scores = browser.find_elements_by_xpath('//*[@class="shopdsr-score-con"]')
		if scores:
			decribe_score = scores[0]
			print 'decribe_score:',decribe_score.text
			attitude_score = scores[1]
			print 'attitude_score:',attitude_score.text
			logistics_score = scores[2]
			print 'logistics_score:',logistics_score.text
			print 'tianmao'
		else:
			scores = browser.find_elements_by_xpath('//*[@class="tb-shop-rate"]//a')
			if scores:
				decribe_score = scores[0]
				print 'decribe_score:',decribe_score.text
				attitude_score = scores[1]
				print 'attitude_score:',attitude_score.text
				logistics_score = scores[2]
				print 'logistics_score:',logistics_score.text
				print 'taobao1'
			else:
				scores = browser.find_elements_by_xpath('//*[@class="rateinfo"]//em')
				decribe_score = scores[0]
				print 'decribe_score:',decribe_score.text
				attitude_score = scores[1]
				print 'attitude_score:',attitude_score.text
				logistics_score = scores[2]
				print 'logistics_score:',logistics_score.text
				print 'taobao2'
		print u'ok=====go on############### '
		self.item['decribe_score'] = decribe_score.text
		self.item['attitude_score'] = attitude_score.text
		self.item['logistics_score'] = logistics_score.text
		#score_urls = browser.find_element_by_xpath('//*[@class="main-info"]//a')
		#if score_urls:
		#	print score_urls.get_attribute("href")
		#else:
		#	score_urls = browser.find_elements_by_xpath('//*[@class="tb-shop-rate"]//a')
		#	print score_urls[0].get_attribute("href")
		browser.quit()
	
		
		

#url = https://s.taobao.com/search?q=t%E6%81%A4&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&ntoffset=6&s=0
#https://s.taobao.com/search?q=t%E6%81%A4&imgfile=&commend
#=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017
#.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc
#&bcoffset=0&p4ppushleft=%2C44&s=44

	
		
		

#url = https://s.taobao.com/search?q=t%E6%81%A4&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&ntoffset=6&s=0
#https://s.taobao.com/search?q=t%E6%81%A4&imgfile=&commend
#=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017
#.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc
#&bcoffset=0&p4ppushleft=%2C44&s=44
