import re
import csv

def create_csv(path):
    with open(path, 'w', newline="", encoding='utf-8-sig') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(['id', '标题', '联系人', '联系号码', '所在地', '工种', '招工详情', '发布时间'])


def write_csv(path, row_data):
    with open(path, 'a+', encoding="utf-8-sig") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(row_data)

def get_with_phone_msg(msg_content):
    msg_content = msg_content.replace(" ", "")
    msg_content = msg_content.replace("-", "")

    m = re.findall(r"1\d{10}", msg_content)
    print(m)

def write_to_csv_file(msg, creat_time, province, city, phone):
    print("sss")



get_with_phone_msg("一级房建转、市政转、公路转、江苏二级水利、公路 山东二级公路、机电电话：13128775413（微信同号，价格美丽） ")