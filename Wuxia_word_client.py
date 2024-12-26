import socket

# 连接服务器
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('192.168.31.137', 5000))  # 请根据实际服务器地址和端口修改
except ConnectionRefusedError:
    print("服务器拒绝！")
    exit()
except TimeoutError:
    print("连接服务器超时！")
    exit()
except:
    print("连接服务器失败！")
    exit()

# 输入角色名
name = input("请输入您的角色名：")
client.sendall(name.encode())

while True:
    print("请输入操作：")
    print("1. 接任务（输入'task'）")
    print("2. 战斗（输入'battle'）")
    print("3. 退出（输入'quit'）")
    operation = input()
    client.sendall(operation.encode())
    data = client.recv(1024).decode()
    print(data)
    if operation == 'quit':
        break

client.sendall("client close".encode())
client.close()
