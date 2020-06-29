#舔狗舔到最后，终将一无所有！
#      2020.05.15初版
#
#      2020.06.29日更新
#更新日志：
#接入数据API，移除页面分析
#
#      作者：C K
#如果程序运行报错就安装下面的库  安装命令：pip install 包名，例如pip install requests
import re
import json
import smtplib
import requests
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
#正则真实地址获取ID
def realurl(newurl):
    pattern = re.compile('(?<=sec_uid=).*(?=&u_code)')
    ree = pattern.search(newurl)
    return ree.group()
#拼接抖音信息api
def dyapi(dyid):
    dyapi = "https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid="+dyid
    response = requests.get(dyapi).text
    content = json.loads(response)
    douyin_info = {}
    # 获取昵称
    douyin_info['女神昵称'] = content["user_info"]["nickname"]
    douyin_info['女神ID'] = content["user_info"]["short_id"]
    # 关注的用户数
    douyin_info['女神的关注数'] = content["user_info"]["following_count"]
    # 作品数
    douyin_info['女神的作品数'] = content["user_info"]["aweme_count"]
    # 喜欢

    douyin_info['女神的喜欢'] = content["user_info"]["favoriting_count"]
    # 粉丝

    douyin_info['女神的粉丝数'] = content["user_info"]["follower_count"]

    # 点赞

    douyin_info['女神的获赞数'] = content["user_info"]["total_favorited"]


    return douyin_info
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
