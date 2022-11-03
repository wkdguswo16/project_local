
from modules.ble_couple import auto_coupling
from modules.redis_handler import *
from modules.sql import *
import json
from modules.env import *
from threading import Thread
env_main = json.load(open("secret_key.json"))
env_redis = env_main['redis']

local_server = RedisHandler(host='localhost', port=6379, db=0)
main_server = RedisHandler(
    env_redis['host'], env_redis['port'], db=0, password=env_redis['password'])
my_region = LockRegion.get(region_id)


def locker_handler(channel: str, data):
    sender, context, pos = map(int, data.split(":"))
    print(data)
    lock_info = LockInfo.get(sender)
    if not lock_info:
        LockInfo.create(sender, my_region.reg_id, int(pos), 0)
    usage = LockUsage.get_by_own_id(sender)
    if not usage:
        return
    if context == 0:
        return
    log = Thread(target=LockLog.create_by_token, args=(usage, context))
    log.start()
    log.join()
    user = User.get(usage.stu_id)
    result = json.dumps({"door_state": context, "noti_token": user.noti_token})
    print(result)
    main_server.publish("server", result)


def server_handler(channel: str, data):
    data = json.loads(data)
    print(data)

    if data.get("target"):
        local_server.set(data['target'], data['action'])
    


def read_property_direct():
    keys = [{"key": key.decode("utf-8"), "value": local_server.get(key).decode("utf-8")}
            for key in local_server.keys() if "r" != key.decode("utf-8")[0]]
    print(keys, end="\\ \r")
    for key in local_server.keys():
        if "r" != key.decode("utf-8")[0]:
            local_server.delete(key)
    return keys


if __name__ == "__main__":
    auto_coupling()
    main_server.listen(my_region.reg_id, server_handler)
    local_server.listen("local", locker_handler)
    input("service started")
