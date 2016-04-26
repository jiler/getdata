# coding=utf-8
__author__ = 'lenovo'

from function import keywords_judge

#title分割函数
def title_split(title, keywords):
    #print '正在分割title'
    article_website = ['aaa','未知']
    try:
        #首先按照 - 分割
        listone = title.split('-')
        #如果分割失败，继续分割（为了区分文章名和网站名）
        if(len(listone)==1):
            listtwo = listone[0].split('_')
            #分割还是失败
            if(len(listtwo)==1):
                article_website = [listtwo[0], '未知']
            else:
                article_website = [listtwo[0], listtwo[-1]]
        else:
            #再分割一次，这次分割是为了精确网站名
            listtwo = listone[-1].split('_')
            #这次分割失败也没事。直接取最后一个
            article_website = [listone[0], listtwo[-1]]
        #判断文章标题是否包含关键字，如果不包含，那就是分割错误
        key_flag = keywords_judge.keywords_judge(article_website[0], keywords)
            #如果不包含必要的关键字，则交换两者顺序
        if key_flag == 0:
            article_website = [article_website[1],article_website[0]]
    except Exception,e:
        print e
    return article_website
