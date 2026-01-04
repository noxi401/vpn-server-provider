import requests
import base64

# لیست کامل منابع شما
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

# بخش اول: دریافت SSTP
print("Step 1: Fetching SSTP...")
sstp_data = []
try:
    r_sstp = requests.get("https://www.vpngate.net/api/iphone/", timeout=20)
    for line in r_sstp.text.replace("\r", "").split("\n"):
        if line.startswith("vpn"):
            d = line.split(",")
            if len(d) > 14:
                sstp_data.append(f"SSTP|{d[1]}|{d[4]}ms|{d[6]}")
except:
    print("SSTP Fetch Failed")

# بخش دوم: دریافت V2Ray
print("Step 2: Fetching V2Ray...")
v2ray_data = []
for url in SOURCES:
    try:
        r_v = requests.get(url, timeout=15)
        if r_v.status_code == 200:
            content = r_v.text
            if "vless://" not in content and "vmess://" not in content:
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
            v2ray_data.extend(content.splitlines())
    except:
        continue

# بخش سوم: ذخیره نهایی
print("Step 3: Saving results...")
with open("results.txt", "w", encoding="utf-8") as f:
    f.write("--- SSTP SERVERS ---\n")
    f.write("\n".join(sstp_data))
    f.write("\n\n--- V2RAY CONFIGS ---\n")
    f.write("\n".join(list(set(v2ray_data))))

print("Success! Everything is done.")
