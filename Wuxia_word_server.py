import random
import socket
import threading

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.combat_power = 10
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 10

    def attack_enemy(self, enemy):
        damage = random.randint(self.attack - 5, self.attack + 5)
        enemy.hp -= damage
        if enemy.hp <= 0:
            enemy.hp = 0
            print(f"{self.name} 击败了 {enemy.name}!")
        else:
            print(f"{self.name} 对 {enemy.name} 造成了 {damage} 点伤害! {enemy.name} 还剩下 {enemy.hp} 点生命值。")

    def defend(self):
        defense = random.randint(5, 10)
        print(f"{self.name} 进行了防御，增加了 {defense} 点防御力!")
        self.combat_power += defense

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
                while player.hp > 0 and opponent.hp > 0:
                    player.attack_enemy(opponent)
                    player.defend()
                    if opponent.hp > 0:
                        opponent.attack_enemy(player)
                if player.hp <= 0:
                    conn.sendall(f"你被 {opponent.name} 击败了！".encode())
                else:
                    conn.sendall(f"你击败了 {opponent.name}！".encode())
            else:
                conn.sendall("暂时没有其他玩家可战斗。".encode())
        else:
            conn.sendall("无效的指令，请重新输入。".encode())

    players.

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
