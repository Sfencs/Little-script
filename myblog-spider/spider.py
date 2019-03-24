import requests
import yagmail
import lxml.html
import re
import time

# 链接邮箱服务器
yag = yagmail.SMTP( user="article_release@163.com", password=".....", host='smtp.163.com')

# # 邮箱正文
# contents = ['This']
#
# # 发送邮件
# yag.send('15832381691@163.com', '博客园博客记录', contents)


def spider(url,RESULT_LIST):
    html_ = requests.get(
        url)
    html_str = html_.content.decode()
    # print(html_str)

    selector = lxml.html.fromstring(html_str)
    article_list = selector.xpath(
        '//div[@class="day"]')

    for article in article_list:
        title = article.xpath('div[@class="postTitle"]/a/text()')[0]
        read = article.xpath('div[@class="postDesc"]/text()')[0]
        read_num = re.findall('(\d+)',read)[5]
        print(title, read_num)
        dict={'title':title,'read_num':int(read_num)}
        RESULT_LIST.append(dict)
    next_url = selector.xpath('//div[@id="nav_next_page"]/a/@href')
    next_url2 = selector.xpath('//div[@class="pager"]/a/@href')
    max = selector.xpath('//div[@class="pager"]/text()')
    if max:
        num = re.findall('(\d+)', max[0])[0]
        print('num',num)
        if num == url[-1]:
            return
    if next_url:
        spider(next_url[0],RESULT_LIST)
    elif next_url2:
        spider(next_url2[-1], RESULT_LIST)




if __name__ == '__main__':
    while True:
        RESULT_LIST = []
        spider('https://www.cnblogs.com/sfencs-hcy/',RESULT_LIST)
        RESULT_LIST = sorted(RESULT_LIST,key=lambda x:x['read_num'])
        RESULT_LIST.reverse()
        print(RESULT_LIST)
        sum1 = sum([ i['read_num'] for i in RESULT_LIST])
        print('sum',str(sum1))
        RESULT_LIST = [ i['title']+'  '+str(i['read_num']) for i in RESULT_LIST]
        content = '\n'.join(RESULT_LIST)+'\n'+'sum'+'   '+str(sum1)

        # 邮箱正文
        # html_ = requests.get('https://www.cnblogs.com/sfencs-hcy/')#catListBlogRank
        # html_str = html_.content.decode()
        # selector = lxml.html.fromstring(html_str)
        # rank_list = selector.xpath(
        #     '//div[@class="catListBlogRank"]/ul')[0]
        # rank_1 = rank_list.xpath('li[@class="liScore"]/text()')[0]
        # rank_2 = rank_list.xpath('li[@class="liRank"]/text()')[0]
        #
        # content = content+'  '+rank_1+'\n'+rank_2
        contents = content
        print(content)
        # 发送邮件
        yag.send('15832381691@163.com', '博客园博客记录', contents)
        print('正在等待下一次发生中...')

        time.sleep(2*60*60)


