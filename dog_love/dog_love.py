#舔狗舔到最后，终将一无所有！
#      2020.05.15
#      作者：C K
#如果程序运行报错就安装下面的库  安装命令：pip install 包名，例如pip install lxml
import re
import json
import smtplib
import requests
from lxml import etree
HEADERS = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}
#获取真实302地址
def get_real_address(url):
    if url.find('v.douyin.com') < 0:
        return url
    res = requests.get(url, headers=HEADERS, allow_redirects=False)
    newurl = res.headers['Location'] if res.status_code == 302 else None
    return newurl
#解密抖音加密信息
def handle_decode(input_data):
    regex_list = [
        {'name': [' &#xe603; ', ' &#xe60d; ', ' &#xe616; '], 'value': 0},
        {'name': [' &#xe602; ', ' &#xe60e; ', ' &#xe618; '], 'value': 1},
        {'name': [' &#xe605; ', ' &#xe610; ', ' &#xe617; '], 'value': 2},
        {'name': [' &#xe604; ', ' &#xe611; ', ' &#xe61a; '], 'value': 3},
        {'name': [' &#xe606; ', ' &#xe60c; ', ' &#xe619; '], 'value': 4},
        {'name': [' &#xe607; ', ' &#xe60f; ', ' &#xe61b; '], 'value': 5},
        {'name': [' &#xe608; ', ' &#xe612; ', ' &#xe61f; '], 'value': 6},
        {'name': [' &#xe60a; ', ' &#xe613; ', ' &#xe61c; '], 'value': 7},
        {'name': [' &#xe60b; ', ' &#xe614; ', ' &#xe61d; '], 'value': 8},
        {'name': [' &#xe609; ', ' &#xe615; ', ' &#xe61e; '], 'value': 9},
    ]
    for i1 in regex_list:
        for i2 in i1['name']:
            input_data = re.sub(i2, str(i1['value']), input_data)
    html = etree.HTML(input_data)
    douyin_info = {}
    # 获取昵称
    douyin_info['女神昵称'] = html.xpath("//div[@class='personal-card']/div[@class='info1']//p[@class='nickname']/text()")[0]
    # 获取抖音ID
    douyin_id = html.xpath("//div[@class='personal-card']/div[@class='info1']/p[@class='shortid']//text()")
    douyin_info['女神ID'] = ''.join(douyin_id).replace('抖音ID：', '').replace(' ', '')
    # 关注的用户数
    follow_count = html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='focus block']//i[@class='icon iconfont follow-num']/text()")
    douyin_info['女神的关注数'] = ''.join(follow_count).replace('关注', '').replace(' ', '')
    # 作品数
    works =html.xpath("//div[@class='tab-wrap']/div[@class='user-tab active tab get-list']//text()")
    douyin_info['女神的作品数'] = ''.join(works).replace('作品', '').replace(' ', '')
    #喜欢
    shelikes = html.xpath("//div[@class='like-tab tab get-list']//text()")
    douyin_info['女神的喜欢'] = ''.join(shelikes).replace('喜欢', '').replace(' ', '')
    # 粉丝
    fans_value = ''.join(html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='follower block']//i[@class='icon iconfont follow-num']/text()"))
    unit = html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='follower block']/span[@class='num']/text()")
    if unit[-1].strip() == 'w':
        douyin_info['女神的粉丝数'] = str(float(fans_value) / 10) + 'w'
    else:
        douyin_info['女神的粉丝数'] = fans_value
    # 点赞
    like = ''.join(html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='liked-num block']//i[@class='icon iconfont follow-num']/text()"))
    unit = html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='liked-num block']/span[@class='num']/text()")
    if unit[-1].strip() == 'w':
        douyin_info['女神的获赞数'] = str(float(like) / 10) + 'w'
    else:
        douyin_info['女神的获赞数'] = like
    return douyin_info
def handle_douyin_info(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
    }
    response = requests.get(url=url, headers=header)
    return handle_decode(response.text)
#发送邮件
def sendEmail(mail_msg):
    from email.mime.text import MIMEText
    # email 用于构建邮件内容
    from email.header import Header
    # 用于构建邮件头
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '1234@qq.com'
    password = '授权码'
    # 收信方邮箱
    to_addr = '1234@qq.com'
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(mail_msg , 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('女神的抖音有新动态啦')
    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()

if __name__ == '__main__':
    url = '女神的抖音主页链接，例如：https://v.douyin.com/ABCd/'
    url = get_real_address(url)
    json2 = handle_douyin_info(url)
    print(json2)


file = open('1.json','r',encoding='utf-8')
oldjson= json.load(file)
gz = int(oldjson['女神的关注数']);like =int(oldjson['女神的喜欢']) ; work = int(oldjson['女神的作品数'] ); fan = int(oldjson['女神的粉丝数']) ;
gz1 = int(json2['女神的关注数']) ; like1 =int(json2['女神的喜欢']) ; work1 = int(json2['女神的作品数']) ; fan1 = int(json2['女神的粉丝数']) ;

if (oldjson == json2):
    print('无变动')
else:
    bd = {}
    bd['关注新增'] = (gz1 - gz)
    bd['喜欢新增'] = (like1 - like)
    bd['作品新增'] = (work1 - work)
    bd['粉丝新增'] = (fan1 - fan)
    if (bd['关注新增']> 0):
        mail_msg1 = "女神关注了" + str(bd['关注新增']) + '个智障，我的女神不爱我了，危机感又多了'+ str(bd['关注新增']) + '分'

    elif (bd['关注新增'] < 0):
        mail_msg1 = "女神取关了"+str(abs(bd['关注新增']))+'个智障，，危机感少了' + str(abs(bd['关注新增'])) + '分耶'
    else :
        mail_msg1='关注无新增'
        print("没有变动")

    if (bd['喜欢新增'] > 0):
        mail_msg2 = '女神喜欢了别人的作品，危机感又多了' + str(bd['喜欢新增']) + '分'

    elif (bd['喜欢新增'] < 0):
        mail_msg2 = '女神讨厌了别人的作品，危机感少了' + str(abs(bd['喜欢新增'])) + '分耶'
    else:
        mail_msg2 = '喜欢无新增'
        print("没有变动")

    if (bd['作品新增'] > 0):
        mail_msg3 = "女神发布了" + str(bd['作品新增']) + '个新作品，快去给她点赞啦'

    elif (bd['作品新增'] < 0):
        mail_msg3 = "女神删除了" + str(abs(bd['作品新增'])) + '个作品，她为什么要删除呢？一定是有人惹她不开心了'
    else:
        mail_msg3 = '作品无新增'
        print("没有变动")

    if (bd['粉丝新增'] > 0):
        mail_msg4 = '女神多了' + str(bd['粉丝新增']) + '个粉丝，竞争对手又多了' + str(bd['粉丝新增']) + '位呢'

    elif (bd['粉丝新增'] < 0):
        mail_msg4 = '女神少了' + str(abs(bd['粉丝新增'])) + '个粉丝，竞争对手又少了' + str(abs(bd['粉丝新增'])) + '位耶'
    else:
        mail_msg4 = '粉丝无新增'
        print('没有变动')
    mail_msg5 = str(json2)
    mail_msg = mail_msg1+'\n'+'\n'+ mail_msg2+'\n'+'\n'+mail_msg3+'\n'+'\n'+mail_msg4+'\n'+'\n'+mail_msg5
    print(mail_msg)
    sendEmail(mail_msg)
    json_info = json2
    file = open('1.json', 'w', encoding='utf-8')
    json.dump(json_info, file)