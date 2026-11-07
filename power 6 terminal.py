"""
╔══════════════════════════════════════════════════════════════════╗
║ 🌟 OOREDOO CLI - VERSION 1.0.0 (TERMINAL ACTIVATOR) 🌟           ║
║           تفعيل هدية أوريدو مباشرة من الترمينال                   ║
║                        by moon                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import requests
from requests.adapters import HTTPAdapter
import json, os, re, uuid, base64, time, urllib.parse, sys
from datetime import datetime, timedelta
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== الإعدادات ====================
OOREDOO_BFF = "https://apis.ooredoo.dz/api/ooredoo-bff"
OOREDOO_AUTH = "https://apis.ooredoo.dz/api/auth/realms/myooredoo/protocol/openid-connect/token"
OOREDOO_CLIENT_ID = "myooredoo-app"
OOREDOO_X_VERSION = "1.5.17"
OOREDOO_X_SIG = "5c7641dbb82cf11066df68afc91541c967640106a95192740b43d51a5ce6777a"
OOREDOO_PLATFORM = "android"
OOREDOO_PLATFORM_ORIGIN = "mobile-android"

OOREDOO_INTEGRITY_1 = "JWBTpxXcH7KY9EXYeIRp8NjQMx2dt3vF8ejjoARazyoFzOw6Cu8+wkeV+zSVHSTeI6a12SG/FU+Q/9uBrcN71RlYO4CulD2x375NKwJRAInar8DVUilHBKUfjEsoHd6EwfLCfdYzLNXJu9POfEf6tqKn3PUe0pY6qZxWLhyVAFHw8Qwb52ZqdI2soCH4S3mrz+OZL+YovdGSUKlXKIkxVroAMTAg3jljLF7gvXaEsB/O3uW+tbkBMwSX2uTOwf+rh3sgOF/zPhKCFgRvZmU1o87Fa96Y/+wOcK+UpfXTCBYVrvQ1wG6ryC7vHMSqgUhYJK4tbSoti0zv4av9pwxh9Iv2MgsMENjyKBK/TuFZxEG3xQCKj1LTMgn2xBEeKcbsKrEW3xDRwsccGI3D7GHnbUlhdI4ujDIRQVKHaZSwhTp+32Cr4EB/Qt8p/xRbdgCde9MUlM4AYIGlfyVoHSkOvTu5c0DIIy1EhowtAkbKIJl49wsYKWvpT/nXFWzeXP3R2qzaclCnIb9qihhrarmwz8l8XH2T+f7AK2uSNiuWLG5Fy2mM/YLmuJPZT9Ciag/mpy7JGImKNQAcFbSAInBdKQjUKT+COzZfrXj5rwil9/HDMtuzIovq8hrQGY+roTfVPheTLWmcjkVCOL8VXAHjPb22vOuqrkMioWT9CQ5O8RgW7RKHrObeKQMp8F7tSjOqkxYDFkPVN1G4nkEBrTlPKK9YtPl+j7IuH9fGcDTwhCTTqP8peuBryW0L11tApvAEi7VkJyBxpVxW"
OOREDOO_INTEGRITY_2 = "JWBTpxXcH7KR/kzaHeUUydDWODuU4i3H4fL9gCgKzyYfyN4qLJJE8keV+zSVHSTeI6aEyC2tbSza/NGmkflQ/UgaNZSN9SKxz7tcdQckHY25n6mOaDZ9PPMQmF4sKZqDwebce/c1SNGNn6qvTULW/L348aJvy7Vii6dyPTu3OSPV9AwKwGwQKNHN61HyK3jx/fa8Os5ux9u3Q654YLZrAJ99QGEm/C9nEBPmlHC98RjovLGBnuJOGx6k7fnyrt/Ogy5fNg+tBgi5HEsoXDAwutX7TOWfx4YKHpKW//TvPRQgp69e2Xqa+CvGJJ+a/WlPMPhRCSsfo0OG04mVvlkc8eXiLzV/GPuJCEmcRf9Z6V+xoDyMtU7OZ3XT5BMhI/D/N68LsRn/9dIBH6X7n0WAW3tzeKZK1zENWFKrd7aLlzEdwFzO/1JTQsEDom5TRie0Kd5yic4BGvS1C1BsA2wJhzyiZ2j7RUE9m8tOAkPEIs929FYIfmH8XcCQKHT0TqT0+N+wCiyfNawPlDhZWcObscFZeEmKgvqiUFCoCj6xI1hvyHK0nu7fnZ/sGc6oNT/SrFjubYWjOyoYFL7gMnlYAhyjZhjuAwN1m1/wjwrOx8DbFr2NW8qb3hv+CIzK1zL3LDryKjqNkTxcOp4aJnmSTa73guCEmWc7pnLkLw5O8RgW7RKHrObeeQ0l9lu4HWXwlhdWRxvVMQDimhtTrGASL6sIuaxyhOkrH4HFImP70SaCoK9+euMxnzkPjg9HqPIFj+I0KSMloVxW"

OOREDOO_PROXIES = [
    "gate.busyip.com:18080:bi_23ee2cd9-session-s1-type-residential-mode-sticky:9C0h1L16DX5gwKbv",
]

SESSION_FILE = "ooredoo_session.json"

http_session = requests.Session()
adapter = HTTPAdapter(pool_connections=20, pool_maxsize=20, max_retries=1)
http_session.mount("https://", adapter)
http_session.mount("http://", adapter)

# ==================== أدوات مساعدة ====================

def mask_msisdn(msisdn):
    if not msisdn or len(msisdn) < 4: return "05********"
    return msisdn[:2] + "********"

def parse_proxy(raw):
    try:
        if not raw or not isinstance(raw, str): return None
        p = raw.strip().split(":", 3)
        if len(p) >= 4: return {"host": f"{p[0]}:{p[1]}", "userpass": f"{p[2]}:{p[3]}"}
        elif len(p) == 2: return {"host": f"{p[0]}:{p[1]}", "userpass": ""}
    except: pass
    return None

def get_valid_proxies():
    return [parse_proxy(p) for p in OOREDOO_PROXIES if parse_proxy(p)]

def _do_request(method, url, headers, body="", proxy=None, timeout=6):
    proxies = None
    if proxy and proxy.get("host"):
        up = f"{proxy['userpass']}@" if proxy.get("userpass") else ""
        proxies = {"http": f"http://{up}{proxy['host']}", "https": f"http://{up}{proxy['host']}"}
    try:
        if method == "GET": r = http_session.get(url, headers=headers, proxies=proxies, timeout=timeout, verify=False)
        elif method == "HEAD": r = http_session.head(url, headers=headers, proxies=proxies, timeout=timeout, verify=False)
        else: r = http_session.post(url, headers=headers, data=body, proxies=proxies, timeout=timeout, verify=False)
        txt = r.text
        if "<!DOCTYPE" in txt or "<html" in txt: return {"ip_blocked": True, "code": r.status_code}
        try: j = r.json()
        except: j = None
        return {"code": r.status_code, "body": txt, "headers": {k.lower(): v for k, v in r.headers.items()}, "json": j}
    except Exception as e:
        return None

def http_request(method, url, headers, body="", proxy=None, timeout=6):
    res = _do_request(method, url, headers, body, proxy, timeout)
    if res is None and proxy is not None:
        res = _do_request(method, url, headers, body, None, timeout)
    return res

def now_ms(): return str(int(time.time() * 1000))
def new_instance_id():
    u = uuid.uuid4().hex
    return f"{u[:8]}-{u[8:12]}-11{u[12:16]}-{u[16:20]}-{u[20:32]}{now_ms()}"
def new_plat_sig(iid):
    return base64.b64encode(json.dumps({"platform": "android", "is-physical-device": True, "device-id": iid}, separators=(',', ':')).encode()).decode()
def new_corr_id(): return uuid.uuid4().hex + now_ms()
def new_fingerprint(): return uuid.uuid4().hex + uuid.uuid4().hex[:32]

def base_headers(msisdn, fp, corr, ts, iid, psig):
    return {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
            "x-device-fingerprint": fp, "x-platform-origin": OOREDOO_PLATFORM_ORIGIN,
            "x-correlation-id": corr, "platform": OOREDOO_PLATFORM, "x-version": OOREDOO_X_VERSION,
            "x-signature": OOREDOO_X_SIG, "x-platform-data-signature": psig,
            "x-timestamp": ts, "x-instance-id": iid}

def authed_headers_web(msisdn, token, tok_hdrs):
    ts = tok_hdrs.get("tok_timestamp") or now_ms()
    iid = tok_hdrs.get("tok_instance_id") or new_instance_id()
    psig = tok_hdrs.get("tok_plat_sig") or new_plat_sig(iid)
    return {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
            "x-device-fingerprint": new_fingerprint(), "x-platform-origin": "web",
            "authorization": f"Bearer {token}", "x-correlation-id": new_corr_id(),
            "platform": "web", "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
            "x-platform-data-signature": psig, "x-timestamp": ts, "x-instance-id": iid,
            "origin": "https://my.ooredoo.dz", "referer": "https://my.ooredoo.dz/"}

# ==================== إرسال OTP ====================

def send_otp(msisdn):
    print("⏳ جاري إرسال رمز التحقق (OTP)...")
    iid = new_instance_id(); psig = new_plat_sig(iid)
    all_proxies = get_valid_proxies() + [None]
    for proxy in all_proxies:
        ts, corr = now_ms(), new_corr_id()
        h1 = base_headers(msisdn, new_fingerprint(), corr, ts, iid, psig)
        r1 = http_request("GET", f"{OOREDOO_BFF}/users/status?msisdn={msisdn}", h1, proxy=proxy, timeout=5)
        if not r1 or r1.get("ip_blocked") or r1.get("code") != 200:
            continue

        h2 = base_headers(msisdn, new_fingerprint(), new_corr_id(), now_ms(), iid, psig)
        r2 = http_request("HEAD", f"{OOREDOO_BFF}/userInfo?msisdn={msisdn}", h2, proxy=proxy, timeout=5)
        if not r2 or r2.get("ip_blocked") or r2.get("code") not in (200, 204):
            continue

        for p34 in all_proxies:
            ts = now_ms(); corr = new_corr_id()
            h3 = base_headers(msisdn, new_fingerprint(), corr, ts, iid, psig)
            h3["content-type"] = "application/json; charset=utf-8"
            h3["x-native-integrity-token"] = OOREDOO_INTEGRITY_1
            h3["x-path"] = "/api/auth/realms/myooredoo/protocol/openid-connect/token"
            h3["x-method"] = "POST"
            r3 = http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, body="{}", proxy=p34, timeout=5)
            if not r3 or r3.get("ip_blocked"): continue

            nonce = r3.get("headers", {}).get("x-nonce-id")
            chronos = r3.get("headers", {}).get("x-chronos-id")
            if not nonce or not chronos: continue

            h4 = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
                  "x-device-fingerprint": new_fingerprint(), "x-nonce-id": nonce,
                  "x-platform-origin": OOREDOO_PLATFORM_ORIGIN, "platform": OOREDOO_PLATFORM,
                  "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
                  "x-chronos-id": chronos, "x-timestamp": ts, "x-platform-info": psig,
                  "x-force-update": "true", "x-instance-id": iid,
                  "Content-Type": "application/x-www-form-urlencoded"}
            body4 = urllib.parse.urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "password", "username": msisdn})
            r4 = http_request("POST", OOREDOO_AUTH, h4, body=body4, proxy=p34, timeout=6)
            if r4 and r4.get("code") in (401, 403):
                print("✅ تم إرسال رمز التحقق (OTP) إلى هاتفك.")
                return {"proxy": p34}
    print("❌ فشل إرسال رمز التحقق. تحقق من الرقم أو اتصال الإنترنت/البروكسي.")
    return None

# ==================== التحقق من OTP ====================

def verify_otp(msisdn, otp, proxy):
    print("⏳ جاري التحقق من الرمز...")
    iid = new_instance_id(); psig = new_plat_sig(iid)
    ts = now_ms(); corr = new_corr_id()
    h6 = base_headers(msisdn, new_fingerprint(), corr, ts, iid, psig)
    h6["content-type"] = "application/json; charset=utf-8"
    h6["x-native-integrity-token"] = OOREDOO_INTEGRITY_2
    h6["x-path"] = "/api/auth/realms/myooredoo/protocol/openid-connect/token"
    h6["x-method"] = "POST"
    r6 = http_request("POST", f"{OOREDOO_BFF}/checkpoint/token", h6, body="{}", proxy=proxy, timeout=5)
    if not r6 or r6.get("ip_blocked"):
        print("❌ فشل التحقق (checkpoint)."); return None
    nonce2 = r6.get("headers", {}).get("x-nonce-id")
    chronos2 = r6.get("headers", {}).get("x-chronos-id")
    if not nonce2 or not chronos2:
        print("❌ فشل التحقق (nonce/chronos)."); return None

    fp7 = new_fingerprint()
    h7 = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn,
          "x-device-fingerprint": fp7, "x-nonce-id": nonce2, "x-platform-origin": OOREDOO_PLATFORM_ORIGIN,
          "platform": OOREDOO_PLATFORM, "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
          "x-chronos-id": chronos2, "x-timestamp": ts, "x-platform-info": psig,
          "x-force-update": "true", "x-instance-id": iid, "Content-Type": "application/x-www-form-urlencoded"}
    body7 = urllib.parse.urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "password", "username": msisdn, "otp": otp})
    r7 = http_request("POST", OOREDOO_AUTH, h7, body=body7, proxy=proxy, timeout=6)
    if not r7: return None
    if r7.get("code") in (401, 403): return "wrong_otp"
    if r7.get("code") == 200 and r7.get("json") and "access_token" in r7["json"]:
        j = r7["json"]
        return {"access_token": j["access_token"], "refresh_token": j.get("refresh_token", ""),
                "token_proxy_host": proxy["host"] if proxy else "direct",
                "token_proxy_user": proxy["userpass"] if proxy else "",
                "tok_fingerprint": fp7, "tok_timestamp": ts, "tok_instance_id": iid,
                "tok_plat_sig": psig, "tok_correlation": corr}
    return None

# ==================== التفعيل ====================

def purchase_bundle(account, bundle_code="BTL_24H_DATA_Free_2Go"):
    msisdn = account.get("msisdn"); token = account.get("access_token")
    if not token or not msisdn:
        return {"success": False, "message": "⚠️ لا يوجد توكن صالح."}

    tok_hdrs = {"tok_timestamp": account.get("tok_timestamp"),
                "tok_instance_id": account.get("tok_instance_id"),
                "tok_plat_sig": account.get("tok_plat_sig")}
    headers = authed_headers_web(msisdn, token, tok_hdrs)
    headers["content-type"] = "application/json; charset=utf-8"
    headers["accept"] = "*/*"

    body = json.dumps({"bundleCode": bundle_code})
    proxy = {"host": account.get("token_proxy_host"), "userpass": account.get("token_proxy_user")} \
        if account.get("token_proxy_host") != "direct" else None

    print("⏳ جاري تفعيل الهدية...")
    res = http_request("POST", f"{OOREDOO_BFF}/cvm/dynamic-bundle-purchase",
                       headers, body=body, proxy=proxy, timeout=12)
    if not res:
        return {"success": False, "message": "❌ خطأ في الاتصال بالخادم."}
    if res.get("code") == 200:
        next_time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M')
        return {"success": True, "message": f"🎉 تم تفعيل الهدية (2GB / 24h)\n⏰ إعادة التفعيل بعد: {next_time}"}
    else:
        return {"success": False, "message": f"⏳ لا يمكن التفعيل حالياً (code={res.get('code')})."}

# ==================== عرض الرصيد ====================

def check_balance(account):
    msisdn = account.get("msisdn")
    tok_hdrs = {"tok_timestamp": account.get("tok_timestamp"),
                "tok_instance_id": account.get("tok_instance_id"),
                "tok_plat_sig": account.get("tok_plat_sig")}
    headers = authed_headers_web(msisdn, account.get("access_token"), tok_hdrs)
    proxy = {"host": account.get("token_proxy_host"), "userpass": account.get("token_proxy_user")} \
        if account.get("token_proxy_host") != "direct" else None

    print("⏳ جاري جلب الرصيد...")
    res = http_request("GET", f"{OOREDOO_BFF}/api/v1/subscribers/main-balance/{msisdn}",
                       headers, proxy=proxy, timeout=10)
    if res and res.get("code") == 200 and res.get("json"):
        balance = res["json"].get("mainBalance", "غير متاح")
        print(f"💰 الرصيد: {balance} DA")
    else:
        print("⚠️ تعذّر جلب الرصيد.")

# ==================== التخزين ====================

def save_session(data):
    try:
        with open(SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ فشل حفظ الجلسة: {e}")

def load_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return None
    return None

# ==================== واجهة المستخدم ====================

BANNER = r"""
╔══════════════════════════════════════════╗
║  🌟 OOREDOO CLI ACTIVATOR - by moon 🌟   ║
║     تفعيل هدية أوريدو من الترمينال        ║
╚══════════════════════════════════════════╝
"""

def show_menu(account):
    print("\n" + "=" * 45)
    print(f"📱 الرقم النشط: {mask_msisdn(account.get('msisdn',''))}")
    print("=" * 45)
    print("1) 🎁 تفعيل هدية 2GB / 24h")
    print("2) 💰 عرض الرصيد")
    print("3) 🔄 تسجيل رقم آخر (إعادة تسجيل)")
    print("4) ❌ خروج")
    print("=" * 45)

def login_flow():
    """تسجيل الدخول: طلب الرقم ثم OTP"""
    while True:
        msisdn = input("📱 أدخل رقم الهاتف الجزائري (مثال 056232XXXX): ").strip()
        if not re.match(r"^0?[567]\d{8}$", msisdn):
            print("⚠️ رقم غير صحيح. جرب مجدداً.")
            continue
        if msisdn.startswith("0"): msisdn = "213" + msisdn[1:]
        break

    otp_res = send_otp(msisdn)
    if not otp_res:
        return None
    proxy = otp_res.get("proxy")

    while True:
        otp = input("📩 أدخل رمز OTP: ").strip()
        if not otp: continue
        auth_data = verify_otp(msisdn, otp, proxy)
        if auth_data == "wrong_otp":
            print("❌ رمز خاطئ، أعد المحاولة.")
            continue
        if auth_data and isinstance(auth_data, dict):
            account = {"msisdn": msisdn, **auth_data}
            save_session(account)
            print("✅ تم تسجيل الدخول بنجاح!")
            return account
        print("❌ فشل التحقق. جرب مجدداً.")
        return None

# ==================== التشغيل الرئيسي ====================

def main():
    print(BANNER)

    account = load_session()
    if account:
        print(f"🔑 تم العثور على جلسة محفوظة: {mask_msisdn(account.get('msisdn',''))}")
        choice = input("هل تريد استخدام الجلسة المحفوظة؟ (y/n): ").strip().lower()
        if choice != 'y':
            account = None

    if not account:
        account = login_flow()
        if not account:
            print("❌ لم يتم تسجيل الدخول. الخروج.")
            return

    while True:
        show_menu(account)
        choice = input("اختر: ").strip()
        if choice == "1":
            res = purchase_bundle(account)
            print("\n" + res["message"])
        elif choice == "2":
            check_balance(account)
        elif choice == "3":
            account = login_flow()
            if not account:
                print("⚠️ لم يتم تسجيل الدخول الجديد، سنبقى على الجلسة الحالية إن وُجدت.")
        elif choice == "4":
            print("👋 إلى اللقاء!")
            return
        else:
            print("⚠️ خيار غير معروف.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 تم الإيقاف.")
        sys.exit(0)