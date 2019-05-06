import requests
import itchat
import re
import csv
import time
import os

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '8ac5431fc803497cb907c762e3b848f6',  # Tuling Key
        'info': msg,  # 这是我们发出去的消息
        'userid': '建筑港Root',  # 这里你想改什么都可以
    }
    # 我们通过如下命令发送一个post请求
    r = requests.post(apiUrl, data=data).json()
    return r.get('text')

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print('----')
    #return get_response(msg['Text'])

@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
def print_content(msg):
    group_name = msg["User"]["NickName"]  # 群名称
    if '建筑港' in group_name:
        print('建筑港...群')
        return parser_msg(msg)
    else:
        print("非建筑港群....")
        #return get_response(msg['Text'])

def autu_replay(msg_text, group_name, is_with_phone):
    worker_group_name = ['【建筑港】总群', '【建筑港】工作汇报群']
    if '@所有人' in msg_text:  
        return '收到'
    if '【建筑港】' in group_name:
        if group_name in worker_group_name:   # 工作群
            print('工作群...')
        else:
            print('个人管理微信群..')
            if is_with_phone:
                return '好的...'
            else:
                flag = random.randint(1, 5)
                if flag == 3:
                    return get_response(msg_text)
                print('...')
                # return get_response(msg_text)
    else:
        return

@itchat.msg_register([itchat.content.PICTURE, itchat.content.RECORDING, itchat.content.ATTACHMENT, itchat.content.VIDEO], isGroupChat=True)
def download_files(msg): #保存记录接受的图片、表情等信息
    cwd = os.getcwd()
    file_url = cwd + '/meFiles/' + msg['FileName']
    # file_url = '/files/' + msg['FileName']
    msg['Text'](file_url)
    print("文件类型....")

def create_csv():
    print(file_name)
    print(os.getcwd())
    print(os.path)
    if os.path.exists(file_name):
        print('----' + file_name + '-存在--')
    else:
        with open(file_name, 'w', newline="", encoding='utf-8-sig') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(['id', '群名称', '昵称', '是否带手机号', 'msg', '时间'])

def write_csv(row_data):
    with open(file_name, 'a+', encoding="utf-8-sig") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(row_data)

def parser_msg(msg):
    # ['id', '群名称', '昵称', 'msg', '时间']
    group_name = msg["User"]["NickName"]
    jock_name = msg["ActualNickName"]
    group_msg = msg["Text"]
    createTime = parser_unix_time(msg['CreateTime'])
    phone = get_with_phone_msg(group_msg)
    is_phone = "否"
    if phone:
        is_phone = "是"
    write_csv(["", group_name, jock_name, is_phone, group_msg, createTime])
    return autu_replay(group_msg, group_name, phone)

def parser_unix_time(timestamp):
    #转换成localtime
    time_local = time.localtime(timestamp)
    #转换成新的时间格式(2016-05-05 20:28:54)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)

def get_file_name():
    date_str = time.strftime('%Y%m%d',time.localtime(time.time()))
    return "weChatLog_" + date_str + ".csv"

def get_with_phone_msg(msg_content):
    msg_content = msg_content.replace(" ", "")
    msg_content = msg_content.replace("-", "")
    m = re.findall(r"1\d{10}", msg_content)
    if m:
        return m
    else:
        return

file_name = get_file_name()

def main():
    create_csv()
    itchat.auto_login(True)
    itchat.run()

if __name__ == "__main__":
    main()











