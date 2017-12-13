# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	pass
import scrapy


class DoubanMovieItem(scrapy.Item):
	# 排名
	ranking = scrapy.Field()
	# 电影名称
	movie_name = scrapy.Field()
	# 评分
	score = scrapy.Field()
	# 评论人数
	score_num = scrapy.Field()
class WeiboItem(scrapy.Item):

	title = scrapy.Field()

	reviewurl = scrapy.Field()

	time_record = scrapy.Field()
class TaobaoItem(scrapy.Item):
	#store_name@
	store_name =scrapy.Field()
	#店铺地址@
	store_location= scrapy.Field()
	#商品名@
	goods_name = scrapy.Field()
	#价格@
	price = scrapy.Field()
	#销量@
	sales = scrapy.Field()
	#月销量@
	month_sales = scrapy.Field()
	#评论数
	reviews = scrapy.Field()
	#评价星级
	star_rating = scrapy.Field()
	#店铺评价分数
	store_rating = scrapy.Field()
	#店铺商品数
	#goods_quantity = scrapy.Field()
	#店铺平均价格
	#average_price = scrapy.Field()
	#店铺平均销量
	#average_sales = scrapy.Field()
	#描述与相符评分
	decribe_score = scrapy.Field()
	#服务态度评分
	attitude_score = scrapy.Field()
	#物流服务评分
	logistics_score = scrapy.Field()