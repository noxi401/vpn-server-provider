import requests
import base64

# لیست منابع V2Ray
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_base64_Sub.txt",
    "https://raw.githubusercontent.com/sakha1370/OpenRay/refs/heads/main/output/all_valid_proxies.txt",
    "https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/refs/heads/main/config.txt",
    "https://raw.githubusercontent.com/mohamadfg-dev/telegram-v2ray-configs-collector/refs/heads/main/category/vless.txt",
    "https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/main/Config/vless.txt",
    "https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/main/Config/vmess.txt",
    "https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/main/Config/shadowsocks.txt",
    "https://shadowmere.xyz/api/sub/",
    "https://shadowmere.xyz/api/b64sub/",
    "https://raw.githubusercontent.com/Danialsamadi/v2go/main/Splitted-By-Country/US.txt",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/python/hy2",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/python/hysteria",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/ss"
]

def get_sstp():
    try:
        r = requests.get("https://www.vpngate.net/api/iphone/", timeout=20)
        lines = r.text.replace("\r", "").split("\n")
        sstp_list = []
        for line in lines:
            if line.startswith("vpn"):
                data = line.split(",")
                if len(data) > 14:
                    sstp_list.append(f"SSTP|{data[1]}|{data[4]}ms|{data[6]}")
        return sstp_list
    except:
        return []

def get_v2ray():
    configs = []
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                text = r.text
                if "vless://" not in text and "vmess://" not in text:
                    try:
                        text = base64.b64decode(text).decode('utf-8')
                    except:
                        pass
                configs.extend(text.splitlines())
        except:
            continue
    return list(set(configs))

if name == "main":
    sstp = get_sstp()
    v2ray = get_v2ray()
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("--- SSTP ---\n" + "\n".join(sstp) + "\n\n--- V2RAY ---\n" + "\n".join(v2ray))
    print("Success!")
