#coding:utf-8
from math import sqrt
# 一个设计影评着及其对几部影片评分情况对字典
critics={
	'Lisa':{'Lady in the Water':2.5, 'Snakes on a Plane':3.5, 'Just My Luck': 3.0, 'Superman Returns':3.5, 'You, Me and Dupree':2.5, 'The Night Listener':3.0, 'My Lover':5.0},
	'Gene':{'Lady in the Water':3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener':3.0,'You, Me and Dupree': 3.5, 'My Lover':3.5},
	'Michael':{'Lady in the Water':2.5, 'Snakes on a Plane':3.0, 'Superman Returns':3.5, 'The Night Listener':4.0},
	'Claudia':{'Snakes on a Plane':3.5, 'Just My Luck': 3.0, 'Superman Returns':4.0, 'You, Me and Dupree':2.5, 'The Night Listener':4.5, 'My Lover':4.0},
	'Jack':{'Lady in the Water':3.0, 'Snakes on a Plane':4.0, 'Superman Returns':5.0, 'You, Me and Dupree':3.5, 'The Night Listener':3.0},
	'Toby':{'Snakes on a Plane':4.5, 'Superman Returns':4.0, 'You, Me and Dupree':1.0},
	'Amo':{'Snakes on a Plane':3.5, 'Superman Returns':4.5,'My Lover':4.5}
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

# 返回p1 个p2的皮尔逊相关系数
def sim_pearson(prefs,p1,p2):
	# 得到双方都曾评价过的物品列表
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item]=1
	# 得到列表元素的个数
	n=len(si)
	# 如果两者没有共同之处， 则返回1
	if n==0:
		return 1
	# 对所有偏好求和
	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])

	#求平方和
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

	# 求乘积之和
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

	# 计算皮尔逊评价值
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0:
		return 0
	r=num/den
	return r

# 从反映偏好的字典中返回最为匹配者
# 返回结果的个数和相似度函数均为可选参数
def topMatches(prefs,person,n=5,similarity=sim_pearson):
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

	# 对列表进行排序，评价值最高的排在最前边
	scores.sort()
	scores.reverse()
	return scores[0:n]

# 利用所有他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs,person,similarity=sim_pearson):
	# 加权后总值
	totals={}
	# 参与评论的平均值之和
	simSums={}
	for other in prefs:
		# 不要和自己做比较
		if other==person:
			continue
		sim=similarity(prefs,person,other)

		#忽略评价值为零或小于零的情况
		if sim<=0:
			continue
		for item in prefs[other]:
			#只对自己还未曾看过的影片进行评价
			if item not in prefs[person] or prefs[person][item]==0:
				# 相似度*评价值
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				# 相似度之和
				simSums.setdefault(item,0)
				simSums[item]+=sim
		# 建立一个归一化的列表
		rankings=[(total/simSums[item],item) for item,total in totals.items()]
		#返回经过排序的列表
		rankings.sort()
		rankings.reverse()
		return rankings

# critics 将物品人人员对调
def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})

			# 将物品和人员对调
			result[item][person]=prefs[person][item]
	return result
# 构造物品相似数据集
def calculateSimilarItems(prefs,n=10):
	# 建立字典，以给出与这些物品最为相近的所有其他物品
	result = {}
	# 以物品为中心对偏好矩阵实施倒置处理
	itemPrefs=transformPrefs(prefs)
	c=0
	for item in itemPrefs:
		# 针对大数据集更新状态变量
		c+=1
		if c%1==0:
			print '%d / %d' % (c,len(itemPrefs))
			# 寻找最为相近的物品
		scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
		result[item]=scores
	return result



# 读取影片数据代码
def loadMovieLens(path='data_movies/'):
	# 获取影片标题
	movies={}
	for line in open(path+'movies.csv'):
		(id,title)=line.split(',')[0:2]
		movies[id]=title

	# 加载数据
	prefs={}
	for line in open(path+'ratings.csv'):
		(user,moiveId,raw_rating,ts)=line.split(',')
		# 过滤错误评分，如评分异常，置0.0
		try:
			rating=float(raw_rating)
		except:
			rating=0.0
		prefs.setdefault(user,{})
		prefs[user][movies[moiveId]]=rating
		
	return prefs

	
