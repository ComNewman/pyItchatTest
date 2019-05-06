from selenium import webdriver
import csv

#第一页内容
url = "http://www.qushigong.com/zhaogong/0_0_0_1/"

# 从第一页起，总共爬取页数
totalPage = 6
# 当前页
currentPage = 0
# 序号
idx = 0

# 准备存储招工cvs文件
cvs_file = open("hiresFromShiGong.csv", "w", newline="", encoding='utf-8-sig')
writer = csv.writer(cvs_file)
writer.writerow(['id', '标题', '联系人', '联系号码', '所在地', '工种', '招工详情', '发布时间'])

driver = webdriver.Chrome(executable_path="/Volumes/mData/meSoft/chromedriver")
print("start.....")
# 遍历 从第一页开始
while currentPage < totalPage:
	driver.get(url)
	data = driver.find_element_by_css_selector("div.cmsHdmC").find_elements_by_tag_name("li")
	for i in range(len(data)):
		# 获取详情页地址
		detailUrl = data[i].find_elements_by_tag_name("span")[0].find_element_by_tag_name("a").get_attribute('href')
		detailDriver = webdriver.Chrome(executable_path="/Volumes/mData/meSoft/chromedriver")
		detailDriver.get(detailUrl)

		detailItems = detailDriver.find_element_by_css_selector("div.rts").find_elements_by_tag_name("div")
		# 项目名称
		projectName = detailItems[0].find_element_by_tag_name("a").text
		# 联系人
		contacts = detailItems[1].find_element_by_tag_name("a").text
		# # 联系电话
		phone = detailItems[2].find_element_by_tag_name("a").text
		# # 项目所在地
		address = detailItems[3].find_element_by_tag_name("span").text
		# # 所需工种
		teamType = detailItems[4].find_element_by_tag_name("span").text
		# 招工说明
		memo = detailDriver.find_element_by_css_selector("div.atc").text
		# 发布时间 ：
		time = detailDriver.find_element_by_css_selector("div.lC").text.split("：")[1]
		writer.writerow([idx, projectName, contacts, phone, address, teamType, memo, time])
		idx = idx + 1
	currentPage = currentPage + 1
	url = detailDriver.find_element_by_css_selector("a.next").get_attribute('href')
	print(url)
print("end......")
cvs_file.close()
