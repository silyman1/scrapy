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
	count = 0#对爬取的条目进行计数
	error_num = 0#对发送错误的条目进行计数
	name = 'bili'
	url = 'https://www.bilibili.com'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	}
	def start_requests(self):
		fo = open('bilibili.log','w')
		sys.stdout = fo
		print self.url
		print u'开始============================================='
		yield Request(self.url,headers =self.headers,callback = self.parse_h)

	def parse_h(self,response):
		#获取所有的type：如动画，番剧等
		results = response.xpath("//*[@class='nav-item']")
		for result in results:
			soup = BeautifulSoup(result.extract())
			details = soup.find_all('li',attrs={'class':'sub-nav-item'})
			#获取所有的type中的详细类型
			for detail in details:
				detail_url = detail.a['href']
				print detail_url.encode('utf-8')
				next_url = self.url + str(detail_url)
				#过滤一些不是我们所想要的连接
				flag1 = re.search('bilibili',detail_url)
				flag2 = re.search('bangumi',detail_url)
				if flag1 and flag2:
					print '此处无有用信息'
					continue
				print next_url
				#获取每个详细类型内的有用信息
				self.get_details(next_url)
			print 'comlete one type++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print 'comlete all types############################################'
		print '总计数为',self.count
		print '错误数为',self.error_num
	def get_details(self,next_url):
		item = BilibiliItem()
		print '?????????'
		#设置浏览器参数
		service_args=[]
		service_args.append('--load-images=no')  ##关闭图片加载
		service_args.append('--disk-cache=yes')  ##开启缓存
		service_args.append('--ignore-ssl-errors=true') ##忽略https错误
		service_args.append('--ssl-protocol=any')
		browser=webdriver.PhantomJS(service_args=service_args)#PhantomJS
		#browser = webdriver.Chrome()
		browser.maximize_window()#窗口最大化，避免有时候selenium找不到元素的情况
		print 'begin=================================second!!!!'
		browser.get(next_url)
		time.sleep(2)
		#刷新页面，避免浮窗挡住我们所要的元素
		browser.refresh()
		time.sleep(3)
		target = browser.find_element_by_xpath("//*[@class='name']")
		browser.execute_script("arguments[0].scrollIntoView();", target) #下拉浏览器时要获取的元素都呈现出来
		browser.save_screenshot('E:\\gitprojects\\scrapy\\1111.png')
		print browser.current_window_handle
		print 'complete=================================second!!!!'
		#third_urls= browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a").get_attribute("href")
		#video_names = browser.find_elements_by_xpath("//*[@class='rank-list hot-list']//li/a/div[2]/p[1]").text
		
		videos = browser.find_elements_by_xpath("//*[@class='ri-title']")#获取热度排行榜的视频元素
		test_help =browser.find_element_by_xpath("//*[@class='name']")#此元素用来辅助，用于点击避免屏幕失去焦点
		print videos
		print test_help
		if videos is []:
			return
		#获取热度版排名前五的元素
		for i in range(0,5):
			self.count +=1
			ranking = i + 1
			#item['video_name'] = videos[i].text
			#ActionChains(browser).click_and_hold(videos[i])
			#browser.save_screenshot('E:\\gitprojects\\scrapy\\1111.png')
			try:
				test_help.click()
				videos[i].click()
			except:
				print '出错了！！！'
				self.error_num += 1#出错统计
				return
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
			self.set_item(ranking,browser,item)
			browser.close()
			print now_handle
			#切换回主窗口
			browser.switch_to_window(now_handle)
			#browser.refresh()
			print 'ok'
			time.sleep(1)
			for i in self.parse(item):
				pass
		browser.quit()
		print 'comlete one detail============================================'
	def set_item(self,ranking,browser,item):
		#详细类型`
		detail_type = browser.find_element_by_xpath("//*[@class='info']/div[3]/span[2]/a").text
		print detail_type
		item['detail_type'] = detail_type
		#类型`
		type = browser.find_element_by_xpath("//*[@class='info']/div[3]/span[1]/a").text
		print type
		item['type'] = type
		#排名`
		print ranking 
		item['ranking'] = str(ranking)
		#video_name`
		video_name = browser.find_element_by_xpath("//*[@class='info']//h1").text
		print video_name
		item['video_name'] = video_name
		#UP主`
		try:
			UP_name = browser.find_element_by_xpath("//*[@class='usname']/a[1]").text
		except:
			print 'something wrong with up_NAME'
			UP_name = 'unknown'
		print UP_name
		item['UP_name'] = UP_name
		#视频播放量
		video_view = browser.find_element_by_xpath("//*[@id='dianji']").text
		print video_view
		item['video_view'] = video_view
		#弹幕量
		Barrage = browser.find_element_by_xpath("//*[@id='dm_count']").text
		print Barrage
		item['Barrage'] = Barrage
		#在线观看人数
		#online_num = browser.find_element_by_xpath("//*[@class='bilibili-player-watching-number']").text
		online_num = '爸爸无能为力'
		print online_num
		item['online_num'] = online_num
		#收藏量stow_count order_count
		try:
			collection = browser.find_element_by_xpath("//*[@id='stow_count']").text
		except:
			collection = browser.find_element_by_xpath("//*[@id='order_count']").text
		print collection
		item['collection_or_zhuifan'] = collection
		#硬币数量
		try:
			coin_num = browser.find_element_by_xpath("//*[@id='v_ctimes']").text
		except:
			coin_num = browser.find_element_by_xpath("//*[@id='icon_count']").text
		print coin_num
		item['coin_num'] = coin_num
		#视频时长
		#video_time = browser.find_element_by_xpath("//*[@class='bilibili-player-video-time-total']").text
		video_time = '爸爸也无能为力'
		print video_time
		item['video_time'] = video_time
		#投稿时间
		Submission_time = browser.find_element_by_xpath("//*[@itemprop='startDate']/i").text
		print Submission_time
		item['Submission_time'] = Submission_time
	def parse(self,item):
		print 'creating item'
		yield item
		print 'comleting one item ********************'
