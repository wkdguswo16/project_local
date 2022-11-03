import subprocess
import json
import socket
def get_my_local_ip():
    return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
    if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
    s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
    socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
def get_wifi_info(name:str=None):
    info = list()
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'r') as r:
        text = r.read()
        while text.find('{') != -1:
            t = text[text.find('{'):text.find('}')+1]
            t = "\n".join([x for x in t.split("\n") if "key_mgmt" not in x])
            t = t.replace('"\n\t', '",\n\t').replace("\t", '\t"').replace("=", '"=').replace("=",":")
            text = text[text.find('}')+1:]
            g = json.loads(t)
            if g['ssid'] == name:
                return g
            info.append(g)
    return info

def get_current_wifi():
    subprocess_result = subprocess.Popen('iwgetid',shell=True,stdout=subprocess.PIPE)
    subprocess_output = subprocess_result.communicate()[0],subprocess_result.returncode
    network_name = subprocess_output[0].decode('utf-8')
    return network_name.split(":")[1].replace('"', '').rstrip()

if __name__ == "__main__":
    name = get_current_wifi()
    print(get_wifi_info(name))