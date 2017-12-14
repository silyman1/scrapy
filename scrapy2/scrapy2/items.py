# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
	
	
class BilibiliItem(scrapy.Item):
	#详细类型`
	detail_type = scrapy.Field()
	#类型`
	type = scrapy.Field()
	#排名`
	ranking = scrapy.Field()
	#video_name`
	video_name = scrapy.Field()
	#UP主`
	UP_name = scrapy.Field()
	#视频播放量
	video_view = scrapy.Field()
	#弹幕量
	Barrage = scrapy.Field()
	#在线观看人数
	online_num = scrapy.Field()
	#收藏量
	collection_or_zhuifan = scrapy.Field()
	#硬币数量
	coin_num = scrapy.Field()
	#视频时长
	video_time = scrapy.Field()
	#投稿时间
	Submission_time = scrapy.Field()
