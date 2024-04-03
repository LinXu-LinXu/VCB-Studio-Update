import smtplib
import requests
from bs4 import BeautifulSoup

import logging
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from datetime import datetime


# 网站地址
url = 'https://vcb-s.com'
# 文件保存
old_vcb = 'old_vcb.json'
new_vcb = 'new_vcb.json'

# 设置SMTP服务器名称
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587

# 设置发件人和收件人的电子邮件地址
FROM_EMAIL = "xxxxxxxxxxx@xxx.com"    # 发信人
FROM_NAME = "Miku"                  
FROM_PASSWORD = "xxxxxxxxxxxx"        # SMTP 邮箱密码
TO_EMAIL = "xxxxxxxxxx@xxx.com"       # 收信人

# 网站更新检测函数
def get_new_article():
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('div', class_='article well clearfix')

        for i, article in enumerate(articles):
            # 只读取最新的一篇文章
            if i >= 1:
                break
            title = article.find('h1').text.strip() if article.find('h1') else article.find('h4').text.strip()
            link = article.find('a')['href']
            date = article.find('span', class_='label label-zan').text.strip()
            image_src = article.find('img')['src'] if article.find('img') else 'No image available'
            alert_content = soup.find('div', class_='alert alert-zan')
            alert_html_contents = alert_content.decode_contents()
            new_data = {
                'title': title,
                'link': link,
                'date': date,
                'image_src': image_src,
                'alert_html_contents': alert_html_contents
            }  # 读取文章信息整合
            # 将信息写入 new_vcb 中
            with open(new_vcb, 'w') as file:
                json.dump(new_data, file, indent=4)
            # 判断是否是第一次运行
            first_run = 'first_run.txt'
            if not os.path.exists(first_run):  # 路径不存在改文件，是第一次运行
                print("第一次运行")
                send_mail()
                with open(first_run, 'w') as f:  # 创建文件，打上标记
                    f.write('The program has already run.')
                # 第一次运行 old_vcb 与 new_vcb 值相同
                with open(old_vcb, 'w') as file:
                    json.dump(new_data, file, indent=4)
        return

    except Exception as e:
        print(f'Error fetching updates: {e}')
        return []


def send_mail():
    # 读取新文章内容
    with open(new_vcb, 'r') as file:
        data = json.load(file)
    title = data['title']
    link = data['link']
    date = data['date']
    image_src = data['image_src']
    alert_html_contents = data['alert_html_contents']

    date_object = datetime.strptime(date, "%y-%m-%d")

    month = date_object.month
    day = date_object.strftime("%d")

    # 创建一个MIMEMultipart对象，这是一个包含所有邮件元素的容器
    msg = MIMEMultipart('alternative')

    # 设置邮件的基本属性
    msg['Subject'] = title
    msg['From'] = formataddr((str(Header(FROM_NAME, 'utf-8')), FROM_EMAIL))
    msg['To'] = TO_EMAIL

    # 创建HTML版本的邮件内容

    html_content = f"""
    <!DOCTYPE html>
<html lang="zh">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <style>
      .article {{
        font-family: "Arial", sans-serif;
        background-color: #fff;
        color: #333;
        max-width: 800px; /* adjust as necessary */
        margin: 20px auto;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
        position: relative;
        padding-top: 10px;
        padding-bottom: 60px;
      }}

      .data-article {{
        font-size: 12px;
        color: #999;
        position: absolute;
        top: -15px;
        left: -25px;

        background-color: #e16b50;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        text-align: center;
        line-height: 50px; /* Adjust line height to vertically center */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }}

      .data-article .month{{
        display: block;
        line-height: 1;
        font-size: 1.3em;
        color: #fff;
        margin-top: 14px;
      }}

      .data-article .day {{
        display: block;
        line-height: 1;
        font-size: 3em;
        color: #fff;
        margin-top: 3px;
      }}

      .title-article h4 {{
        text-align: center;
        padding: 35px;
        background-color: #41b6d7ce;
        color: #333;
      }}

      .title-article h4 a {{
        line-height: 1.5;
        font-size: 1.5em;
        text-decoration: none;
        color: #333;
      }}

      .thumbnail img {{
        width: 100%;
        height: auto;
        border-bottom: 5px solid #eee;
      }}

      .alert-zan {{
        padding: 15px;
        background-color: #f2dede;
        border: 1px solid #ebccd1;
        border-radius: 4px;
        margin: 15px;
      }}
      .alert-zan p {{
        margin: 0 0 10px;
      }}
      .alert-zan strong {{
        color: #d9534f;
      }}
      .btn-danger {{
        position: absolute;
        right: 20px;

        width: 90px;
        height: 20px;
        display: block;

        text-align: center;
        line-height: 20px;
        text-decoration: none;
        color: #fff;
        background-color: #d9534f;
        padding: 15px 15px;
        font-weight: bold;
        border-radius: 10px;
      }}

      .btn-danger:hover {{
        background-color: #c9302c;
        color: #fff;
        text-decoration: none;
      }}
    </style>
  </head>

  <body>
    <div class="article well clearfix">
      <div class="data-article hidden-xs">
        <span class="month">{month}月</span>
        <span class="day">{day}</span>
      </div>

      <div class="title-article">
        <h4>
          <a href="{link}"
            >{title}</a
          >
        </h4>
      </div>

      <div class="content-article">
        <figure class="thumbnail">
          <a href="{link}"
            ><img
              width="1400"
              height="936"
              src="{image_src}"
              class="attachment-full size-full wp-post-image"
              alt=""
              decoding="async"
              sizes="(max-width: 1400px) 100vw, 1400px"
          /></a>
        </figure>
        <div class="alert alert-zan">
          {alert_html_contents}
        </div>
      </div>
      <a
        class="btn btn-danger pull-right read-more btn-block"
        href="{link}"
        title="详细阅读 {title}"
        >阅读全文
      </a>
    </div>
  </body>
</html>
    """

    # 创建纯文本版本的邮件内容（如果收件人的邮件客户端不支持HTML）
    text_content = title + '\n' + link

    # 将HTML和纯文本版本的邮件内容添加到MIMEMultipart对象中
    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    # 连接到SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.close()
        print('Email sent successfully!')
    except Exception as e:
        print('Failed to send email:', str(e))


def check_new():
    get_new_article()
    with open(new_vcb, 'r') as file:
        data_new = json.load(file)
    new_link = data_new['link']

    with open(old_vcb, 'r') as file:
        data_old = json.load(file)
    old_link = data_old['link']

    if new_link == old_link:
        print("没有新文章")
        return
    else:
        with open(old_vcb, 'w') as file:
            json.dump(data_new, file, indent=4)
        send_mail()


def main():
    logging.basicConfig(filename='logfile.log', level=logging.INFO)
    logging.info(f'Script executed at {datetime.now()}')
    check_new()


if __name__ == '__main__':
    main()
