import socket
import threading

# 玩家信息类
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.combat_power = 10
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 10

# 处理客户端连接的函数
def handle_client(conn, addr, players):
    # 接收玩家创建的角色名
    name = conn.recv(1024).decode()
    player = Player(name)
    players.append(player)

    while True:
        data = conn.recv(1024).decode()
        if data == "quit":
            conn.sendall("quit game".encode())
        elif data == "client close":
            # 结束 handle_client，退出线程
            break
        elif data == "task":
            # 处理任务逻辑
            conn.sendall(f"你接到了一个新任务！".encode())
        elif data == "battle":
            # 处理战斗逻辑
            opponent = None
            for p in players:
                if p!= player:
                    opponent = p
                    break
            if opponent:
                conn.sendall(f"你与 {opponent.name} 进入战斗！".encode())
            else:
                conn.sendall("暂时没有其他玩家可战斗。".encode())
        else:
            conn.sendall("无效的指令，请重新输入。".encode())

# 启动服务器
def start_server():
    players = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.31.137', 5000))
    server.listen(5)
    print("服务器启动，等待连接...")

    while True:
        conn, addr = server.accept()
        print(f"连接来自 {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr, players))
        thread.start()

if __name__ == "__main__":
    start_server()