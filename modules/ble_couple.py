from bleak import BleakScanner, BleakClient
from modules.wifi import *
import asyncio
import os
from time import sleep
from threading import Thread


WIFI_NAME = get_current_wifi()
WIFI_INFO = get_wifi_info(WIFI_NAME)
WIFI_INFO['host'] = get_my_local_ip()
connect_table = []
os.system("sudo hciconfig hci0 piscan")
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


def on_disconnect(client):
    print("Client with address {} got disconnected!".format(client.address))


def detection_callback(device, advertisement_data):
    # 장치 주소와 신호세기, 그리고 어드버타이징 데이터를 출력한다.
    connect_table.append({"dev": device, "adv": advertisement_data})
    # if SERVICE_UUID in advertisement_data.service_uuids:
    #     print(device.address, "RSSI:", device.rssi, advertisement_data)
    # await connect(device.address.lower())
    # connect_table.remove(device.address)


async def connect(address):
    async with BleakClient(address) as client:
        print('ble connected')
        await client.write_gatt_char(CHAR_UUID, data=json.dumps(WIFI_INFO).encode("utf-8"))
        print('ble setup complete')
        await client.disconnect()


async def run():
    scanner = BleakScanner(detection_callback)
    # 콜백 함수 등록
    # 검색 시작
    await scanner.start()
    # 5초간 대기 이때 검색된 장치들이 있다면 등록된 콜백함수가 호출된다.
    await asyncio.sleep(5.0)
    # 검색 중지
    await scanner.stop()
    # 지금까지 찾은 장치들 가져오기
    devices = await scanner.get_discovered_devices()

    return devices
    # 지금까지 찾은 장치 리스트 출력
    # for d in devices:
    #     print(d)


def auto_coupling():
    executer = asyncio.get_event_loop()
    def loop():
        while True:
            executer.run_until_complete(run())
            sleep(0.5)
            for i in connect_table:
                dev, adv = i['dev'], i['adv']
                if not SERVICE_UUID in adv.service_uuids:
                    continue
                print(dev, adv)

                try:
                    executer.run_until_complete(connect(dev.address))
                except Exception as e:
                    print(f"failed: {e}")
            connect_table.clear()
    Thread(target=loop).start()