import asyncio
from bleak import BleakClient
import json
from time import sleep
from wifi import *
WIFI_NAME = get_current_wifi()
WIFI_INFO = get_wifi_info(WIFI_NAME)
WIFI_INFO['host'] = get_my_local_ip()

address = "70:B8:F6:42:C4:FE"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def main(address):
    async with BleakClient(address, timeout=10) as client:
        print(client)
        await client.write_gatt_char(MODEL_NBR_UUID, data=json.dumps(WIFI_INFO).encode("utf-8"))
        value = await client.read_gatt_char(MODEL_NBR_UUID)
        print(value.decode("utf-8"))
        await asyncio.sleep(1)
        await client.disconnect()
asyncio.run(main(address))
