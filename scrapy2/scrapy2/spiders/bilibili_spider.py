# -*- coding: UTF-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from scrapy2.items import BilibiliItem
from selenium import webdriver
import sys
import time
import re
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
	
	def get_nextdetails(self,url):
		print '?????????'
		service_args=[]
		service_args.append('--load-images=no')  ##关闭图片加载
		service_args.append('--disk-cache=yes')  ##开启缓存
		service_args.append('--ignore-ssl-errors=true') ##忽略https错误
		service_args.append('--ssl-protocol=any')
		browser=webdriver.PhantomJS(service_args=service_args)#PhantomJS
		print 'begin=================================second!!!!'
		browser.get(url)
		time.sleep(3)
		print 'complete=================================second!!!!'
		#third_urls= browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a").get_attribute("href")
		#video_names = browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a/div[2]/p[1]").text
		videos = browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a/div[2]/p[1]")
		for i in range(0,5):
			ranking = i + 1
			self.item['ranking'] = str(ranking)
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
			yield self.item
	def parse(self,response):
		results = response.xpath("//*[@class='nav-item']")
		for result in results:
			soup = BeautifulSoup(result.extract())
			details = soup.find_all('li',attrs={'class':'sub-nav-item'})
			for detail in details:
				detail_url = detail.a['href']
				print detail_url.encode('utf-8')
				next_url = self.url + str(detail_url)
				flag = re.search('bilibili',detail_url)
				if flag:
					print '此处无有用信息'
					break
				print next_url
				print '?????????'
				service_args=[]
				service_args.append('--load-images=no')  ##关闭图片加载
				service_args.append('--disk-cache=yes')  ##开启缓存
				service_args.append('--ignore-ssl-errors=true') ##忽略https错误
				service_args.append('--ssl-protocol=any')
				#browser=webdriver.PhantomJS(service_args=service_args)#PhantomJS
				browser = webdriver.Chrome()
				print 'begin=================================second!!!!'
				browser.get(next_url)
				time.sleep(2)
				#browser.save_screenshot('E:\\gitprojects\\scrapy\\1111.png')
				print browser.current_window_handle
				print 'complete=================================second!!!!'
		#third_urls= browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a").get_attribute("href")
		#video_names = browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a/div[2]/p[1]").text
				videos = browser.find_elements_by_xpath("//*[@class='ri-title']")
				test_helps =browser.find_elements_by_xpath("//*[@class='ri-num']")
				if videos is []:
					break
				for i in range(0,5):
					ranking = i + 1
					self.item['ranking'] = str(ranking)
					#item['video_name'] = videos[i].text
					#ActionChains(browser).click_and_hold(videos[i])
					try:
						test_helps[i].click()
						videos[i].click()
					except:
						print '出错了'
						break
					time.sleep(3)
					now_handle = browser.current_window_handle #获取当前窗口句柄
					print now_handle   #输出当前获取的窗口句柄
					all_handles = browser.window_handles #获取所有窗口句柄
					for handle in all_handles:
						if handle != now_handle:
							print handle, '输出待选择的窗口句柄'#输出待选择的窗口句柄
							browser.switch_to_window(handle) #绑定
					print browser.current_window_handle
					#print browser.page_source
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
					try:
						UP_name = browser.find_element_by_xpath("//*[@class='usname']/a[1]").text
					except:
						print 'something wrong with up_NAME'
						UP_name = 'unknown'
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
					#online_num = browser.find_element_by_xpath("//*[@class='bilibili-player-watching-number']").text
					online_num = '爸爸无能为力'
					print online_num
					self.item['online_num'] = online_num
					#收藏量stow_count order_count
					try:
						collection = browser.find_element_by_xpath("//*[@id='stow_count']").text
					except:
						collection = browser.find_element_by_xpath("//*[@id='order_count']").text
					print collection
					self.item['collection_or_zhuifan'] = collection
					#硬币数量
					try:
						coin_num = browser.find_element_by_xpath("//*[@id='v_ctimes']").text
					except:
						coin_num = browser.find_element_by_xpath("//*[@id='icon_count']").text
					print coin_num
					self.item['coin_num'] = coin_num
					#视频时长
					#video_time = browser.find_element_by_xpath("//*[@class='bilibili-player-video-time-total']").text
					video_time = '爸爸也无能为力'
					print video_time
					self.item['video_time'] = video_time
					#投稿时间
					Submission_time = browser.find_element_by_xpath("//*[@itemprop='startDate']/i").text
					print Submission_time
					self.item['Submission_time'] = Submission_time
					browser.close()
					print now_handle
					browser.switch_to_window(now_handle) 
					print 'ok'
					yield self.item
				browser.quit()
				print 'comlete one detail============================================'
			print 'comlete one type++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print 'comlete all types############################################'
		

