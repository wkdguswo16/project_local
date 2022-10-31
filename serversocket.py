from datetime import datetime
import socket
from threading import Thread
import json
from time import sleep
HOST = 'lockscale.kro.kr'
PORT = 5000
ID = 1234

def socket_connect():
    global client_socket
    print("connecting")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.settimeout(10)
        sleep(5)
        client_socket.connect((HOST, PORT))
    except:
        return
    socket_send("new")
    sleep(0.5)


def socket_send(data):
    send = {
        'identify': 'region',
        'id': ID,
        'data': data
    }
    try:
        client_socket.send(json.dumps(send).encode())
        print("Send Success")
    except:
        print("Send Failed")


def receiver():
    while True:
        try:
            recv = client_socket.recv(1024)
            if len(recv) == 0:
                print("disconnected")
                socket_connect()

            data = json.loads(recv.decode())
            status = data.get('status')
            info = data.get('data')
            if status == "ok":
                print("연결됨")
            if not info:
                break
            info.get("id")
        except:
            pass


def concurrent():
    while True:
        sleep(60)
        message = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        socket_send(message)


# 키보드로 입력한 문자열을 서버로 전송하고
# 서버에서 에코되어 돌아오는 메시지를 받으면 화면에 출력합니다.
# quit를 입력할 때 까지 반복합니다.
if __name__ == "__main__":
    socket_connect()
    Thread(target=receiver).start()
    Thread(target=concurrent).start()
    while True:
        message = input()
        socket_send(message)
    client_socket.close()
