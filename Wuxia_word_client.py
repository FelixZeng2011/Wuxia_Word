import socket
import json
import sys


def input_and_check(prompt, check_func=None, check_list=None, unexpected_list=None):
    while True:
        input_str = input(prompt)
        if check_func is not None:
            if check_func(input_str):
                return input_str
        elif check_list is not None:
            if input_str in check_list:
                return input_str
        elif unexpected_list is not None:
            if input_str not in unexpected_list:
                return input_str

        print("输入有误，请重新输入!")

def send_json_message(client, server, data):
    message = json.dumps(data).encode('utf-8')
    client.sendto(message, server)

def receive_json_message(client, server):
    while True:
        data, from_addr = client.recvfrom(1024)
        if from_addr == server:
            return json.loads(data.decode('utf-8'))

def retrieve_hero(client, server):
    send_json_message(client, server, {"message": "请求存档"})
    data = receive_json_message(client, server)
    message = data.get("message")
    if message == "没有存档":
        name = input("请输入您的角色名：")
        send_json_message(client, server, {"name": name})
    else:
        curr_name = data.get("name")
        if curr_name is not None:
            print("已创建角色：" + curr_name + "，请选择：")
            print("继续该角色(1)")
            print("创建新角色(2)")
            operation = input_and_check("", check_list=["1", "2"])
            if operation == "2":
                name = input_and_check("请输入您的角色名：", unexpected_list=[curr_name])
                send_json_message(client, server, {"name": name})
            else:
                send_json_message(client, server, {"message": "继续该角色"})
                data = receive_json_message(client, server)
                curr_player = data.get("name")
                if curr_player is not None:
                    print("角色信息：")
                    print(curr_player)
        else:
            print("收到未知消息：%s" % data)


def get_battle_messages(client, server):
    while True:
        data = receive_json_message(client, server)
        message = data.get("message")
        if message is not None:
            print(message)
        else:
            end_message = data.get("battle_end")
            if end_message is not None:
                print(end_message)
                break
            else:
                print("收到未知消息：%s" % data)

# 连接服务器
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('192.168.31.137', 4000))
server = ('192.168.31.137', 5000)
retrieve_hero(client, server)

while True:
    print("请输入操作：")
    print("接任务（输入'1'）")
    print("战斗（输入'2'）")
    print("退出（输入'q'）")
    operation = input()
    send_json_message(client, server, {"message": operation})

    if operation == 'q':
        break
    elif operation == '1':
        data = receive_json_message(client, server)
        print(data)
    elif operation == '2':
        get_battle_messages(client, server)

send_json_message(client, server, {"message": "client close"})

