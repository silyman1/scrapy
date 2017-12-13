# -*- coding: UTF-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from scrapy2.items import BilibiliItem
from selenium import webdriver
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')
from selenium.webdriver.common.action_chains import ActionChains
class Bilibili_Spider(Spider):
	name = 'bili'
	url = 'https://www.bilibili.com'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	}
	item = BilibiliItem()
	def start_requests(self):
		fo = open('bilibili.log','w')
		sys.stdout = fo
		print self.url
		print u'开始============================================='
		yield Request(self.url,headers =self.headers)
	def parse(self,response):
		soup = BeautifulSoup(response.body)
		results = soup.find_all('li',attrs={'class':'nav-item'})
		
		for result in results:
			print result
			soup1 = BeautifulSoup(result)
			details = soup.find_all('a')
			print details
			print '\n'
			for detail in details:
				detail_url = detail
				next_url = self.url + detail_url
				print next_url
				self.parse_second(next_url)
				print 'comlete one detail============================================'
			print 'comlete one type++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print 'comlete all types############################################'
	def parse_second(self,url):
		service_args=[]
		service_args.append('--load-images=no')  ##关闭图片加载
		service_args.append('--disk-cache=yes')  ##开启缓存
		service_args.append('--ignore-ssl-errors=true') ##忽略https错误
		service_args.append('--ssl-protocol=any')
		browser=webdriver.PhantomJS(service_args=service_args)#PhantomJS
		browser.get(url)
		time.sleep(3)
		print '=================================second!!!!'
		#third_urls= browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a").get_attribute("href")
		#video_names = browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a/div[2]/p[1]").text
		videos = browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a/div[2]/p[1]")
		for i in range(0,5):
			ranking = i + 1
			item['ranking'] = str(ranking)
			#item['video_name'] = videos[i].text
			ActionChains(browser).click_and_hold(videos[i])
			time.sleep(2)
			#UP_name = browser.find_element_by_xpath("//*[@class='usname']/a[1]").text
			#video_view = browser.find_element_by_xpath("//*[@id='dianji']").text
			#详细类型`
			detail_type = browser.find_element_by_xpath("//*[@class='info']/div[3]/span[2]/a").text
			print detail_type
			self.item['detail_type'] = detail_type
			
			#类型`
			type = browser.find_element_by_xpath("//*[@class='info']/div[3]/span[1]/a").text
			print type
			self.item['type'] = type
			#排名`
			print ranking 
			#video_name`
			video_name = browser.find_element_by_xpath("//*[@class='info']//h1").text
			print video_name
			self.item['video_name'] = video_name
			#UP主`
			UP_name = browser.find_element_by_xpath("//*[@class='usname']/a[1]").text
			print UP_name
			self.item['UP_name'] = UP_name
			#视频播放量
			video_view = browser.find_element_by_xpath("//*[@id='dianji']").text
			print video_view
			self.item['video_view'] = video_view
			#弹幕量
			Barrage = browser.find_element_by_xpath("//*[@id='dm_count']").text
			print Barrage
			self.item['Barrage'] = Barrage
			#在线观看人数
			online_num = browser.find_element_by_xpath("//*[@class='bilibili-player-watching-number']").text
			print online_num
			self.item['online_num'] = online_num
			#收藏量stow_count
			collection = browser.find_element_by_xpath("//*[@id='stow_count']").text
			print collection
			self.item['collection'] = collection
			#硬币数量
			coin_num = browser.find_element_by_xpath("//*[@id='v_ctimes']").text
			print coin_num
			self.item['coin_num'] = coin_num
			#视频时长
			video_time = browser.find_element_by_xpath("//*[@class='bilibili-player-video-time-total']").text
			print video_time
			self.item['video_time'] = video_time
			#投稿时间
			Submission_time = self.item['coin_num'] = browser.find_element_by_xpath("//*[@itemprop='startDate']/i").text
			print Submission_time
			self.item['Submission_time'] = Submission_time
			yield item
			
			
			