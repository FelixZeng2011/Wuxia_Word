import socket
import json

def input_and_check(prompt, check_func = None, check_list = None, unexpected_list = None):
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

def send_json_message(conn, data):
    message = json.dumps(data).encode('utf-8')
    conn.sendall(message)

def receive_json_message(conn):
    print("收到消息：")
    data = conn.recv(1024)
    message = json.loads(data.decode('utf-8'))
    print(message)
    return message

def retrieve_hero(client):
    send_json_message(client, {"message": "请求存档"})
    data = receive_json_message(client)
    message = data.get("message")
    if message == "没有存档":
        name = input("请输入您的角色名：")
        send_json_message(client, {"name": name})
    else:
        curr_name = data.get("name")
        if curr_name is not None:
            print("已创建角色：" + curr_name + "，请选择：")
            print("继续该角色(1)")
            print("创建新角色(2)")
            operation = input_and_check("", check_list=["1", "2"])
            if operation == "2":
                name = input_and_check("请输入您的角色名：", unexpected_list=[curr_name])
                send_json_message(client, {"name": name})
            else:
                send_json_message(client, {"message": "继续该角色"})
                data = receive_json_message(client)
                curr_player = data.get("player_info")
                if curr_player is not None:
                    print("角色信息：")
                    print(curr_player)
        else:
            print("收到未知消息：%s, 来自: %s" % (data, addr))

def get_battle_messages(client):
    while True:
        data = receive_json_message(client)
        message = data.get("message")
        if message is not None:
            print(message)
        else:
            end_message = data.get("battle_end")
            if end_message is not None:
                print(end_message)
                break
            else:
                print("收到未知消息：%s, 来自: %s" % (data, addr))

# 连接服务器
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('192.168.31.137', 5000))  # 请根据实际服务器地址和端口修改
except ConnectionRefusedError:
    print("服务器拒绝连接！")
    exit()
except TimeoutError:
    print("连接服务器超时，请重试。")
    exit()
except:
    print("连接服务器失败!")
    exit()

retrieve_hero(client)

while True:
    print("请输入操作：")
    print("接任务（输入'1'）")
    print("战斗（输入'2'）")
    print("退出（输入'q'）")
    operation = input()
    send_json_message(client, {"message": operation})

    if operation == 'q':
        break
    elif operation == '1':
        data = receive_json_message(client)
        print(data)
    elif operation == '2':
        get_battle_messages(client)

send_json_message(client, {"message": "client close"})
client.close()
