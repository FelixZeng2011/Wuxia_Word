import socket
import threading
import json
import random

# 玩家信息类
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.exp_for_next_level = 100
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 30
        self.speed = 5

def find_list_as_key(List, KeyName, KeyValue):
    for item in List:
        if item[KeyName] == KeyValue:
            return item
    return None

def send_json_message(conn, data):
    message = json.dumps(data).encode('utf-8')
    conn.sendall(message)

def receive_json_message(conn):
    data = conn.recv(1024)
    return json.loads(data.decode('utf-8'))

def handle_message(message_dict, conn, addr, players):
    print("received message: ")
    print(message_dict)
    ip_addr = addr[0]

    StrMsg = message_dict.get("message")
    if StrMsg == "q":
        return StrMsg
    elif StrMsg == "请求存档":
        current_dict = find_list_as_key(players, "addr", ip_addr)
        if current_dict is None:
            send_json_message(conn, {"message": "没有存档"})
        else:
            send_json_message(conn, {"name": current_dict["player"].name})
    elif StrMsg == "继续该角色":
        current_dict = find_list_as_key(players, "addr", ip_addr)
        send_json_message(conn, {"name": current_dict["player"].name})
    elif StrMsg == "client close":
        return StrMsg
    elif StrMsg == "1":
        send_json_message(conn, {"message": "暂无任务"})
    elif StrMsg == "2":
        current_dict = find_list_as_key(players, "addr", ip_addr)
        start_battle(conn, current_dict["player"])
    else:
        name = message_dict.get("name")
        if name is not None:
            player = Player(name)
            # TODO: 检查是否name已被使用
            current_dict = find_list_as_key(players, "addr", ip_addr)
            if current_dict is not None:
                players.remove(current_dict)
            players.append({"addr": ip_addr, "player": player})
            current_player = player
            print("新创建角色"+name)
            print(players)
        else:
            print("收到未知消息：%s, 来自: %s" % (message_dict, addr))
        
def start_battle(conn, player):
    if player is None:
        print("未创建角色")
        send_json_message(conn, {"battle_end": "未创建角色！"})
        return
    opponent = get_opponent(player)
    if opponent is None:
        print("无对手")
        send_json_message(conn, {"battle_end": "目前只有一个玩家，无法对战！"})
        return
    else:
        print("开始战斗")
        while True:
            one_round(conn, player, opponent)
            if player.hp <= 0:
                message = {"battle_end": "你输给了" + opponent.name + "！"}
                send_json_message(conn, message)
                player.hp = player.max_hp
                print(message)
                return
            elif opponent.hp <= 0:
                message = {"battle_end": "你战胜了" + opponent.name + "！"}
                send_json_message(conn, message)
                opponent.hp = opponent.max_hp
                print(message)
                return

def one_round(conn, player, opponent):
    print("开始回合")
    if player.speed >= opponent.speed:
        first = player
        second = opponent
    else:
        first = opponent
        second = player

    attack(conn, first, second)
    if second.hp > 0:
        attack(conn, second, first)

def attack(conn, attacker, defender):
    attack = attacker.attack
    damage = attacker.attack + random.randint(-attack/10, attack/10)
    defender.hp -= damage
    message = attacker.name + "对" + defender.name + "造成了" + str(damage) + "点伤害"
    print("先手攻击")
    send_json_message(conn, {"message": message})
    message = defender.name + "剩余生命值为" + str(defender.hp)
    print("后手攻击")
    send_json_message(conn, {"message": message})
    return damage

def get_opponent(player):
    for opponent in players:
        if opponent["player"] != player:
            return opponent["player"]
    return None

# 处理客户端连接的函数
def handle_client(conn, addr, players):

    while True:
        message = receive_json_message(conn)
        result = handle_message(message, conn, addr, players)
        if result == "client close" or result == "q":
            break

    '''while True:
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

    players.'''

# 启动服务器
def start_server():
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
    players = []
    start_server()
