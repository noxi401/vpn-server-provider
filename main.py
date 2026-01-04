import requests
import base64
import re

# لیست تمامی منابعی که شما فرستادید
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

def get_sstp_from_vpngate():
    """استخراج سرورهای SSTP از سایت VPN Gate"""
    try:
        print("Connecting to VPN Gate...")
        r = requests.get("https://www.vpngate.net/api/iphone/", timeout=20)
        content = r.text.replace("\r", "")
        lines = content.split("\n")
        sstp_list = []
        for line in lines:
            if line.startswith("vpn"):
                data = line.split(",")
                # فرمت خروجی: IP, HostName, Ping, Country
                if len(data) > 14:
                    sstp_list.append(f"SSTP|{data[1]}|{data[3]}|{data[4]}ms|{data[6]}")
        return sstp_list
    except Exception as e:
        print(f"Error fetching SSTP: {e}")
        return []

def get_v2ray_configs():
    """استخراج و تمیزکاری لینک‌های V2Ray"""
    all_configs = []
    for url in SOURCES:
        try:
            print(f"Fetching V2Ray from: {url}")
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                text = r.text
                # اگر محتوا کد شده (Base64) بود، بازش می‌کنیم
                if "vless://" not in text and "vmess://" not in text:
                    try:
                        text = base64.b64decode(text).decode('utf-8')
                    except:
                        pass
                # جدا کردن لینک‌ها بر اساس خط جدید
                lines = text.splitlines()
                for l in lines:
                    if len(l) > 10: all_configs.append(l.strip())
        except:
            continue
    return list(set(all_configs)) # حذف تکراری‌ها

if name == "main":
    # اجرای عملیات
    sstp_servers = get_sstp_from_vpngate()
    v2ray_configs = get_v2ray_configs()
    
    # ذخیره در فایل نهایی
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("--- SSTP SERVERS ---\n")
        f.write("\n".join(sstp_servers))
        f.write("\n\n--- V2RAY CONFIGS ---\n")
        f.write("\n".join(v2ray_configs))
    
    print(f"Done! Saved {len(sstp_servers)} SSTP and {len(v2ray_configs)} V2Ray configs.")
