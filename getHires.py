from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import csv


def create_csv(path):
    with open(path, 'w', newline="", encoding='utf-8-sig') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(['id', 'projectName', 'lianxi', 'phone', 'address', 'teamType', 'memo', 'time'])


def write_csv(path, row_data):
    with open(path, 'a+', encoding="utf-8-sig") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(row_data)

# 获取  http://m.qushigong.com/zhaogong/ 详情 获取中间4位号码   
def get_m_detail_html(url):
    m_base_url = 'http://m.qushigong.com/zhaogong/'
    a = url.split('/')
    b = a[4] + '/' + a[5]
    m_detail_url = m_base_url + a[4] + '/' + a[5]
    print(m_detail_url)
    m_html = urlopen(m_detail_url)
    return BeautifulSoup(m_html.read(), 'html.parser')


# 获取详情页面html
def get_detail_html(detailUrl):
    html = urlopen(detailUrl)
    return BeautifulSoup(html.read(), 'html.parser')

def parser_detail_html_2_csv(html, m_detail_html, csv_path, idx):
    m_phone = m_detail_html.find("div", id='teldiv').get('data-t') 
    
    c = html.find("div", class_="rts").find_all("div")
    name = c[0].find("a").get_text()
    contacts = c[1].find("a").get_text()
    address = c[3].find("span").get_text()
    teamType = c[4].find("span").get_text()
    memo = html.find("div", class_="atc").get_text().replace(' ', '')
    time = html.find("div", class_="lC").get_text().split("：")[1]

    phone = c[2].find("a").get_text()
    if '***' not in phone:
        print('.....')
    else:
        print(',1,2.333...')
        phone = m_phone[0:7] + phone[9:13]
    write_csv(csv_path, [idx, name, contacts, phone, address, teamType, memo, time])

# 获取列表页
def get_li_html(bodyStr):
    return bodyStr.find("div", class_='inc cmsHdmC').find("ul").find_all("li")

def initData(bodyStr, csv_path, currentPage):
    lis = get_li_html(bodyStr)
    for i in range(len(lis)):
        itmUrl = lis[i].find("a").get("href")
        detail_html = get_detail_html(itmUrl)
        m_detail_html = get_m_detail_html(itmUrl)
        # 休眠10s
        time.sleep(4)
        parser_detail_html_2_csv(detail_html, m_detail_html, csv_path, str(currentPage) + "" + str(i))

def main():
    print("开始........")
    csv_path = "hires.csv"
    totalPage = 8
    currentPage = 1
    baseUrl = "http://www.qushigong.com"
    url = "/zhaogong/0_0_0_1/"
    create_csv(csv_path)
    while currentPage < totalPage:
        html = urlopen(baseUrl + url)
        bodyStr = BeautifulSoup(html.read(), 'html.parser')
        initData(bodyStr, csv_path, currentPage)
        # 下一页地址
        url = bodyStr.find("a", class_="next").get("href")
        currentPage = currentPage + 1
    print("完成........")
    #get_m_detail_html('http://www.qushigong.com/zhaogong/sc/z390365.html');

if __name__ == "__main__":
    main()
