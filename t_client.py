import threading,socket

HOST = 'localhost'
PORT = 4000

def sendMsg(soc):
    while True:
        message = input("")
        soc.sendall(message.encode(encoding='utf-8'))
        if message == 'quit':
            break
    print('클라이언트 메시지 입력 쓰레드 종료')


def recvMsg(soc):
    while True:
        data = client_socket.recv(1024)
        msg = data.decode()
        print(msg)
        if msg == 'quit':
            break
    client_soc.close()
    print('클라이언트 리시브 쓰레드 종료')


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

t = threading.Thread(target=sendMsg,args=(client_socket,))
t.start()
t2 =  threading.Thread(target=recvMsg, args=(client_socket,))
t2.start()

   
   
