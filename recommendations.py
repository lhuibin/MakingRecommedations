#coding:utf-8
from math import sqrt
# 一个设计影评着及其对几部影片评分情况对字典
critics={
	'Lisa Rose':{'Lady in the Water':2.5, 'Snakes on a Plane':3.5, 'Just My Luck': 3.0, 'Superman Returns':3.5, 'You, Me and Dupree':2.5, 'The Night Listener':3.0},
	'Gene Seymour':{'Lady in the Water':3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener':3.0,'You, Me and Dupree': 3.5},
	'Michael Phillips':{'Lady in the Water':2.5, 'Snakes on a Plane':3.0, 'Superman Returns':3.5, 'The Night Listener':4.0},
	'Claudia Puig':{'Snakes on a Plane':3.5, 'Just My Luck': 3.0, 'Superman Returns':4.0, 'You, Me and Dupree':2.5, 'The Night Listener':4.5},
	'Jack Matthews':{'Lady in the Water':3.0, 'Snakes on a Plane':4.0, 'Superman Returns':5.0, 'You, Me and Dupree':3.5, 'The Night Listener':3.0},
	'Toby':{'Snakes on a Plane':4.5, 'Superman Returns':4.0, 'You, Me and Dupree':1.0}
	}

# 返回一个有关 人1 于 人2 的基于距离的相似度评价
def sim_distance(prefs,person1,person2):
	# 得到 shared_items的列表
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1
	# 如果两者没有共同之处，则返回0
	if len(si)==0:
		return 0
	# 计算所有差值的平方和
	sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])

	return 1/(1+sqrt(sum_of_squares))