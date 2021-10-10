import random
import socket
import threading

import cx_Oracle

# DB 접속
conn = cx_Oracle.connect("seonmin", "1234", "localhost:1521/xe")
cur = conn.cursor()

host = ""
port = 4000
user_list = {}
notice_flag = 0


# 대기실
class Room:
    def __init__(self):
        self.clients = []  # 접속한 클라이언트를 담당하는 ChatClient 객체 저장
        self.clientsid = []

    def addClient(self, c, id):  # 클라이언트 하나를 채팅방에 추가
        self.clients.append(c)
        self.clientsid.append(id)

    def delClent(self, c):  # 클라이언트 하나를 채팅방에서 삭제
        self.clients.remove(c)

    def sendAllClients(self, msg):
        for c in self.clients:
            c.sendall(msg.encode(encoding='utf-8'))


def sendAllClients(msg):
    for c in clients:
        c.sendall(msg.encode(encoding='utf-8'))


def data_base_admin(admin_socket, admin, user_pw):  # 관리자가 dB에 접근해서 작업할 때의 함수

    while True:
        print('start')
        data = client_socket.recv(8192)
        db_query = data.decode()  # db_query = select * from player

        if db_query == "/exit":
            break
        cur.execute(db_query)
        query_result = cur.fetchall()
        print(str(query_result))
        db_query = "%s : %s" % (admin, db_query)
        try:
            admin_socket.send(str(query_result).encode())
        except:
            print("abnormal")
    del user_list[user]
    client_socket.close()


class Player:
    def __init__(self, ps):
        self.budget = 100000
        self.batting = 0
        self.deck = []
        self.order = 0
        self.state = 0
        self.Game_ID = 0
        self.ps = ps

    def raising(self, line):
        while True:
            money = int(input("얼마를 배팅하시겠습니까"))
            if money >= line and money <= self.budget:
                self.batting += money
                break

    def call(self, line):
        money = line
        self.batting += money
    # def fold(self):
    #
    # def askCard(self,Winner):
    #
    # def leave(self,ID):


def handle_notice(client_sockets, players):  # 사용자들이 게임에 접속 해서 포커를 치는 함수
    new_game = Game()
    # 방만들기
    for i in client_sockets:
        gameroom.clients.append(i)

    gameroom.sendAllClients("게임을 시작합니다\n")

    # 카드 생성 후 자동 섞기
    new_card = new_game.makingCard()

    # 카드 배분 대상 구분
    for i in client_sockets:
        new_game.alive_list.append(Player(i))

    # 카드 나눠주기
    for i in new_game.alive_list:
        c = new_card.pop()
        i.deck.append(c)
        msg = "첫번째 카드는 " + c.pattern + str(c.number)
        i.ps.sendall(msg.encode(encoding='utf-8'))
    for i in new_game.alive_list:
        c = new_card.pop()
        i.deck.append(c)
        msg = "두번째 카드는 " + c.pattern + str(c.number)
        i.ps.sendall(msg.encode(encoding='utf-8'))


class Card:
    def __init__(self, number, pattern):
        self.number = number
        self.pattern = pattern


class Game:
    def __init__(self):
        self.game_ID = 50
        self.state = 0
        self.batting_line = 0
        self.deck = []
        self.alive_list = []

    def makingCard(self):
        number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        pattern = ['SPADE', 'HEART', 'DIA', 'CLOVER']
        card_list = []
        for i in number:
            for j in pattern:
                card_list.append(Card(i, j))
        random.shuffle(card_list)
        return card_list

    # def card_pop(self,card_list):
    #
    # def card_open(self,deck):
    #
    # def changeDealerPoint(self,player_list):
    #
    # def scoring(selfplayer_list,deck):
    #
    # def money(self,player_list,winner):


print("Setting server...")
# IPv4 체계, TCP 타입 소켓 객체를 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 포트를 사용 중 일때 에러를 해결하기 위한 구문
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# ip주소와 port번호를 함께 socket에 바인드 한다.
server_socket.bind((host, port))

# 서버가 최대 5개의 클라이언트의 접속을 허용한다.
server_socket.listen(5)
print("Setting server - 5 clients")

user_id = []
user_pw = 0


def start():
    msg = '<회원가입>:1 <로그인>:2 <종료>:3\n'
    client_socket.sendall(msg.encode(encoding='utf-8'))
    oneortwo = client_socket.recv(1024).decode()
    if oneortwo == '1':
        assignment()
    elif oneortwo == '2':
        log_in()


# 회원가입
def assignment():
    try:
        msg = '사용할 id : '
        client_socket.sendall(msg.encode(encoding='utf-8'))
        user_id = client_socket.recv(1024).decode()
        user_list[user_id] = client_socket

        msg = '사용할 pw : '
        client_socket.sendall(msg.encode(encoding='utf-8'))
        user_pw = client_socket.recv(1024).decode()

        db_query = 'insert into player(player_id,player_pw) values(:id,:pw)'
        cur.execute(db_query, id=user_id, pw=user_pw)
        conn.commit()
        print('플레이어 저장완료')
        msg = '회원가입 완료\n'
        client_socket.sendall(msg.encode(encoding='utf-8'))
        clients.append(client_socket)
        log_complete(user_id)

    except cx_Oracle.IntegrityError:
        msg = '사용할 수 없는 아이디입니다\n'
        client_socket.sendall(msg.encode(encoding='utf-8'))
        assignment()


def log_in():
    msg = 'id : '
    client_socket.sendall(msg.encode(encoding='utf-8'))
    login_id = client_socket.recv(1024).decode()

    msg = 'pw : '
    client_socket.sendall(msg.encode(encoding='utf-8'))
    login_pw = client_socket.recv(1024).decode()

    db_query = 'select * from player where player_id = :loginid and player_pw = :pw'
    cur.execute(db_query,loginid = str(login_id),pw = login_pw)
    query_result = cur.fetchall()

    if query_result == []:
        msg = '잘못됐습니다\n'
        client_socket.sendall(msg.encode(encoding='utf-8'))
        log_in()
    else :
        log_complete(login_id)

def log_complete(user_id) :
    # DB에 log_in 기록 저장
    db_query = 'insert into log_in(log_in_id,player_id,log_int_time) values(AAA.NEXTVAL,:id,sysdate)'
    cur.execute(db_query, id=user_id)
    conn.commit()
    print('로그인 기록 저장완료')
    msg = '로그인 완료\n'
    client_socket.sendall(msg.encode(encoding='utf-8'))

def waiting():
    msg = user_id + "님이 입장하셨습니다\n"
    waitingroom.addClient(client_socket, user_id)
    waitingroom.sendAllClients(msg)
    msg = "<게임 참여>:1 <프로필>2 <랭킹>3 <플레이시간>4\n"
    client_socket.sendall(msg.encode(encoding='utf-8'))
    participate = client_socket.recv(1024).decode()

    if participate == '1':
        msg = "대기중입니다\n"
        client_socket.sendall(msg.encode(encoding='utf-8'))
        gameroom.addClient(client_socket, user_id)
        waitingroom.clients.remove(client_socket)
        waitingroom.clientsid.remove(user_id)
        if len(gameroom.clients) >= 3:
            handle_notice(waitingroom.clients, waitingroom.clientsid)

    #윤형 6번 쿼리
    elif participate =='2':
        db_query = 'select nickname, round(wins/games * 100, 2) as win_rate, amount, credit from casino_player p, win_rate w, budget b where (p.id = w.id) and p.id = b.id and p.id = yhcha;'
        cur.execute(db_query)
        query_result = cur.fetchall()

   #윤형 1번 쿼리
    elif participate == '3' :
        db_query = 'SELECT nickname, round(wins/games * 100, 2) as win_rate from casino_player p, win_rate w where p.id = w.id and ROWNUM <= 10 order by wins/games desc;'
        cur.execute(db_query)
        query_result = cur.fetchall()
    #선민 1번 쿼리
    elif participate == '4' :
        db_query = ''
        cur.execute(db_query)
        query_result = cur.fetchall()





clients = []

waitingroom = Room()
gameroom = Room()
while 1:
    try:
        # 클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
        client_socket, addr = server_socket.accept()
        print(addr)
        print('접속')
    except KeyboardInterrupt:
        for user, con in user_list:
            con.close()
        server_socket.close()
        print("Keyboard interrupt")
        break

    notice_thread = threading.Thread(target=start, args=())
    notice_thread.daemon = True
    notice_thread.start()
