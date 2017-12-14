# -*- coding: UTF-8 -*-
import re
a = 'https://www.bilibili.com/bangumi.bilibili.com/anime/timeline'
flag = re.search('bilibili',a)
if flag:
	a ='//bangumi.bilibili.com/anime/timeline'
print a