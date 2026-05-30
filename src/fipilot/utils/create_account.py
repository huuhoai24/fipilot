#!/usr/bin/env python3
"""
Tự động tạo tài khoản VietnamWorks Employer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Flow (theo recorded script):
  Page 1 → basic info → Continue
  Page 2 → company + location → Continue
  CAPTCHA checkbox → Submit (CloakBrowser tự bypass)
  Email → kích hoạt
"""

import os
import re
import json
import time
import random
import string
import tempfile
import threading
import requests
import speech_recognition as sr
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed
from cloakbrowser import launch

# ─── CONFIG ───────────────────────────────────────────────────────────────────
PASSWORD         = "Fipilot2025@"
NUM_ACCOUNTS     = 100
PARALLEL_WORKERS = 1        # 1 luồng để debug
ACCOUNTS_FILE    = "account.json"
MAIL_TM_API      = "https://api.mail.tm"

# ─── CAPTCHA CONFIG ──────────────────────────────────────
CAPSOLVER_KEY    = ""       # ← capsolver.com  (~$1/1000, đưa chuột vào)
TWOCAPTCHA_KEY   = ""       # ← 2captcha.com   (~$3/1000, fallback)
SITEKEY          = "6Lfu1qMUAAAAAPWa4vlbVVHDepiOHtkmknQFX_Sx"

# ─── PROXY CONFIG ───────────────────────────────────────────
AUTO_SCRAPE_PROXIES = False  # Bật True để tự động cào hàng ngàn proxy miễn phí
# Mỗi tài khoản sẽ rotate qua danh sách này.
# None = dùng IP thật (không proxy)
# Format: {"server": "http://host:port"} hoặc {"server": "http://host:port", "username": "u", "password": "p"}
PROXIES = [
    None,   # IP thật — thêm proxy vào đây
    # {"server": "http://proxy1.example.com:8080"},
    # {"server": "http://proxy2.example.com:8080", "username": "user", "password": "pass"},
]

FIRST_NAMES = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Vu", "Dang", "Bui"]
LAST_NAMES  = ["An", "Binh", "Cuong", "Dung", "Giang", "Hung", "Khanh", "Long"]
COMPANIES   = ["Tech Hub", "Dev Studio", "Code Factory", "Smart Systems", "Digital Lab"]
LOCATIONS   = ["Ha Noi", "Ho Chi Minh", "Da Nang", "Can Tho", "Hai Phong"]

_lock = threading.Lock()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def rand_str(n=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def random_phone():
    return "09" + ''.join(random.choices(string.digits, k=8))


# ─── MAIL.TM ──────────────────────────────────────────────────────────────────
class MailTM:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["Content-Type"] = "application/json"
        self.address = None

    def create(self):
        domains = self.s.get(f"{MAIL_TM_API}/domains", timeout=10).json()["hydra:member"]
        domain  = domains[0]["domain"]
        self.address = f"{rand_str(12)}@{domain}"
        pwd = rand_str(16) + "A1!"
        self.s.post(f"{MAIL_TM_API}/accounts",
                    json={"address": self.address, "password": pwd},
                    timeout=10).raise_for_status()
        tok = self.s.post(f"{MAIL_TM_API}/token",
                          json={"address": self.address, "password": pwd},
                          timeout=10).json()["token"]
        self.s.headers["Authorization"] = f"Bearer {tok}"
        return self.address

    def wait_email(self, timeout=120, poll=3):
        seen = set()
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                msgs = self.s.get(f"{MAIL_TM_API}/messages", timeout=8).json().get("hydra:member", [])
                for m in msgs:
                    mid = m["id"]
                    if mid not in seen:
                        seen.add(mid)
                        return self.s.get(f"{MAIL_TM_API}/messages/{mid}", timeout=8).json()
            except Exception:
                pass
            time.sleep(poll)
        return None


# ─── 1SECMAIL (FALLBACK) ──────────────────────────────────────────────────────
class Mail1Sec:
    def __init__(self):
        self.login = rand_str(12)
        self.domain = "1secmail.com"
        self.address = f"{self.login}@{self.domain}"

    def create(self):
        try:
            r = requests.get("https://www.1secmail.com/api/v1/?action=getDomainList", timeout=10)
            if r.status_code == 200:
                domains = r.json()
                if domains:
                    self.domain = random.choice(domains)
                    self.address = f"{self.login}@{self.domain}"
        except Exception:
            pass
        return self.address

    def wait_email(self, timeout=120, poll=5):
        seen = set()
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={self.login}&domain={self.domain}"
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    msgs = r.json()
                    for m in msgs:
                        mid = m["id"]
                        if mid not in seen:
                            seen.add(mid)
                            # Fetch full message
                            detail_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={self.login}&domain={self.domain}&id={mid}"
                            detail = requests.get(detail_url, timeout=10).json()
                            # Standardize to match MailTM schema (returning a dict)
                            return {
                                "id": mid,
                                "subject": detail.get("subject", ""),
                                "html": detail.get("htmlBody", ""),
                                "text": detail.get("textBody", ""),
                            }
            except Exception:
                pass
            time.sleep(poll)
        return None


# ─── RESILIENT EMAIL CLIENT ────────────────────────────────────────────────────
class ResilientMail:
    def __init__(self):
        self.provider = None

    def create(self):
        try:
            print("📬 Thử tạo email bằng Mail.tm...")
            self.provider = MailTM()
            addr = self.provider.create()
            return addr
        except Exception as e:
            print(f"⚠️ Mail.tm thất bại ({e}). Chuyển sang 1secmail làm fallback...")
            self.provider = Mail1Sec()
            return self.provider.create()

    def wait_email(self, timeout=120, poll=5):
        if self.provider:
            return self.provider.wait_email(timeout, poll)
        return None


# ─── EXTRACT LINK ─────────────────────────────────────────────────────────────
def extract_link(email_data):
    html_raw = email_data.get("html") or ""
    html_str = " ".join(html_raw) if isinstance(html_raw, list) else str(html_raw)
    body = html_str + " " + (email_data.get("text") or "")
    for pat in [
        r'href=["\']([^"\' ]*(?:activat|verify|confirm)[^"\' ]*)["\']',
        r'(https?://[^\s<>"\']*(?:activat|verify|confirm)[^\s<>"\']*)',
        r'href=["\']([^"\' ]*vietnamworks[^"\' ]*)["\']',
    ]:
        m = re.findall(pat, body, re.I)
        if m:
            return m[0].strip()
    return None


# ─── 2CAPTCHA SOLVER ─────────────────────────────────────────────────────
def solve_recaptcha_2captcha(page, tag=""):
    """
    Giải reCAPTCHA v2 bằng 2captcha API:
      1. Gửi sitekey + URL lên 2captcha
      2. Chờ token (30-60s)
      3. Inject token vào g-recaptcha-response
      4. Trigger reCAPTCHA callback
    """
    if not TWOCAPTCHA_KEY:
        return False  # Không có API key → dùng audio

    page_url = page.url
    print(f"{tag} 📲 2captcha: gửi request...")
    try:
        # Submit task
        resp = requests.post(
            "https://2captcha.com/in.php",
            data={
                "key": TWOCAPTCHA_KEY,
                "method": "userrecaptcha",
                "googlekey": SITEKEY,
                "pageurl": page_url,
                "json": 1,
            },
            timeout=15,
        ).json()

        if resp.get("status") != 1:
            print(f"{tag} ⚠️ 2captcha error: {resp}")
            return False

        task_id = resp["request"]
        print(f"{tag} ⏳ Chờ 2captcha giải (task {task_id})...")

        # Poll kết quả (tối đa 120s)
        for _ in range(24):
            time.sleep(5)
            result = requests.get(
                "https://2captcha.com/res.php",
                params={"key": TWOCAPTCHA_KEY, "action": "get",
                        "id": task_id, "json": 1},
                timeout=10,
            ).json()
            if result.get("status") == 1:
                token = result["request"]
                print(f"{tag} ✅ 2captcha token nhận được!")

                # Inject token vào hidden textarea
                page.evaluate(f"""
                    document.getElementById('g-recaptcha-response').value = '{token}';
                    document.getElementById('g-recaptcha-response').style.display = 'block';
                """)

                # Trigger callback của reCAPTCHA
                page.evaluate(f"""
                    if (window.___grecaptcha_cfg) {{
                        const cfg = window.___grecaptcha_cfg;
                        const keys = Object.keys(cfg.clients);
                        if (keys.length > 0) {{
                            const client = cfg.clients[keys[0]];
                            const cb = Object.values(client).find(v => typeof v === 'function');
                            if (cb) cb('{token}');
                        }}
                    }}
                """)
                page.wait_for_timeout(1000)
                return True

            if result.get("request") != "CAPCHA_NOT_READY":
                print(f"{tag} ⚠️ 2captcha: {result}")
                return False

        print(f"{tag} ⚠️ 2captcha timeout")
        return False

    except Exception as e:
        print(f"{tag} ⚠️ 2captcha exception: {e}")
        return False


# ─── AUDIO CAPTCHA SOLVER (fallback) ────────────────────────────────────
def solve_recaptcha_audio(page, tag=""):
    """
    Giải CAPTCHA theo thứ tự ưu tiên:
      1. CapSolver API  (nếu có CAPSOLVER_KEY)
      2. 2captcha API  (nếu có TWOCAPTCHA_KEY)
      3. Audio challenge (fallback cuối cùng, độc lập ngôn ngữ)
    """
    page_url = page.url

    # ─ 1. CapSolver ──────────────────────────────────────────────
    if CAPSOLVER_KEY:
        token = solve_capsolver(page_url, tag)
        if token:
            inject_captcha_token(page, token, tag)
            return True

    # ─ 2. 2captcha ─────────────────────────────────────────────
    if TWOCAPTCHA_KEY:
        return solve_recaptcha_2captcha(page, tag)

    print(f"{tag} 🔊 Audio challenge (fallback)...")
    try:
        cb_frame = page.frame_locator("iframe[name^='a-']").first
        anchor = cb_frame.get_by_role("checkbox").first
        
        # Hàm kiểm tra checkbox đã được check chưa (độc lập ngôn ngữ)
        def is_checked():
            try:
                return anchor.get_attribute("aria-checked", timeout=1000) == "true"
            except Exception:
                return False

        # Click checkbox (thử nhiều cách để đảm bảo trigger sự kiện)
        ch_frame = page.frame_locator("iframe[name^='c-']").first
        for attempt_click in range(3):
            try:
                if attempt_click == 0:
                    anchor.click(timeout=3000)
                elif attempt_click == 1:
                    cb_frame.locator(".recaptcha-checkbox-border").click(force=True, timeout=3000)
                else:
                    anchor.evaluate("el => el.click()")
                
                page.wait_for_timeout(2000)
                
                is_vis = False
                try:
                    is_vis = ch_frame.locator("body").is_visible(timeout=500)
                except Exception:
                    pass
                    
                if is_checked() or is_vis:
                    break
            except Exception as e:
                print(f"{tag} ⚠️ Lỗi khi click checkbox (lần {attempt_click+1}): {e}")



        if is_checked():
            print(f"{tag} ✅ CAPTCHA auto-passed!")
            return True

        # Kiểm tra có challenge iframe không
        ch_frame = page.frame_locator("iframe[name^='c-']").first
        try:
            ch_frame.locator("body").wait_for(state="visible", timeout=3000)
        except Exception:
            # Nếu challenge iframe không xuất hiện mà đã checked thì ok
            if is_checked():
                print(f"{tag} ✅ CAPTCHA auto-passed!")
                return True
            else:
                print(f"{tag} ⚠️ Challenge không hiện, thử click lại checkbox...")
                try:
                    anchor.click(timeout=3000)
                    page.wait_for_timeout(2000)
                    if is_checked():
                        print(f"{tag} ✅ CAPTCHA auto-passed sau khi click lại!")
                        return True
                except Exception:
                    pass
                return False

        # Thử chọn ảnh sai 2 lượt trước khi chuyển sang Audio (Heuristic tránh bị Google chặn)
        print(f"{tag} 🖼️ Tiến hành mô phỏng chọn sai 2 lượt ảnh để tránh bị Google chặn...")
        for round_idx in range(2):
            if is_checked():
                break
            
            # Quét các ô ảnh
            tiles = ch_frame.locator(".rc-imageselect-tile")
            try:
                tiles.first.wait_for(state="visible", timeout=3000)
            except Exception:
                break
                
            count = tiles.count()
            if count > 0:
                print(f"{tag} 🖼️ Lượt chọn ảnh {round_idx+1}/2: Tìm thấy {count} ô ảnh. Click ngẫu nhiên 3 ô...")
                indices = random.sample(range(count), min(3, count))
                for idx in indices:
                    try:
                        tiles.nth(idx).click(timeout=2000)
                        page.wait_for_timeout(400 + random.randint(100, 300))
                    except Exception:
                        pass
                
                # Bấm xác minh (Verify / Next)
                try:
                    ch_frame.locator("#recaptcha-verify-button").click(timeout=3000)
                    print(f"{tag} 🖼️ Lượt chọn ảnh {round_idx+1}/2: Bấm Xác minh.")
                    page.wait_for_timeout(2000)
                except Exception:
                    pass

        # Kiểm tra xem có giải tay xong hoặc tự thông qua không
        if is_checked():
            print(f"{tag} ✅ CAPTCHA đã được giải!")
            return True

        # Click nút Audio challenge (ID: #recaptcha-audio-button)
        try:
            print(f"{tag} 🔊 Chuyển đổi thử thách sang dạng Âm thanh...")
            ch_frame.locator("#recaptcha-audio-button").click(timeout=3000)
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"{tag} ⚠️ Không click được nút Audio: {e}")

        # Thử tối đa 5 lần giải bằng âm thanh
        for attempt in range(5):
            if is_checked():
                print(f"{tag} ✅ CAPTCHA đã được giải!")
                return True

            print(f"{tag} 🎵 Audio attempt {attempt+1}/5")
            try:
                # Click PLAY (ID: #recaptcha-audio-play hoặc nút có chứa play/listen)
                try:
                    play_btn = ch_frame.locator(".rc-audiochallenge-play-button button, #recaptcha-audio-play").first
                    play_btn.click(timeout=3000)
                    page.wait_for_timeout(1000)
                except Exception:
                    pass

                # Kiểm tra nếu bị block "Try again later / automated queries" (hỗ trợ cả tiếng Anh và tiếng Việt)
                is_blocked = False
                try:
                    block_text = ch_frame.locator("body").inner_text().lower()
                    if "automated queries" in block_text or "yêu cầu tự động" in block_text or "try again later" in block_text or "thử lại sau" in block_text:
                        is_blocked = True
                except Exception:
                    pass

                if is_blocked:
                    print(f"{tag} ⚠️ Bị Google block Audio (Try again later / automated queries)!")
                    print(f"{tag} ⏳ Đang tải lại captcha hình, bạn có 90 giây để tự giải...")
                    try:
                        ch_frame.locator("#recaptcha-reload-button").click(timeout=2000)
                    except Exception:
                        pass
                    # Chờ 90 giây cho người dùng giải tay
                    for _ in range(90):
                        if page.is_closed():
                            print(f"{tag} 🚪 Trình duyệt đã bị đóng.")
                            return False
                        try:
                            page.wait_for_timeout(1000)
                        except Exception as e:
                            if "closed" in str(e).lower():
                                print(f"{tag} 🚪 Trình duyệt đã bị đóng.")
                                return False
                            raise e
                        if is_checked():
                            print(f"{tag} ✅ CAPTCHA đã được giải thủ công!")
                            return True
                    print(f"{tag} ❌ Vẫn chưa giải xong, bỏ qua.")
                    return False

                # Lấy URL audio (chờ tối đa 5 giây để audio xuất hiện)
                audio_src = None
                t_start = time.time()
                while time.time() - t_start < 5:
                    if page.is_closed():
                        return False
                    for sel in ["audio#audio-source", "audio", ".rc-audiochallenge-tdownload-link"]:
                        try:
                            el = ch_frame.locator(sel).first
                            if sel.endswith("link"):
                                audio_src = el.get_attribute("href", timeout=500)
                            else:
                                audio_src = el.get_attribute("src", timeout=500)
                            if audio_src:
                                break
                        except Exception:
                            pass
                    if audio_src:
                        break
                    page.wait_for_timeout(500)

                if not audio_src:
                    print(f"{tag} ⚠️ Không tìm thấy audio src, tải thử thách mới...")
                    try:
                        ch_frame.locator("#recaptcha-reload-button").click(timeout=3000)
                        page.wait_for_timeout(2000)
                    except Exception:
                        pass
                    continue

                # Tải file MP3 và chuyển sang WAV
                headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.google.com/"}
                audio_bytes = requests.get(audio_src, headers=headers, timeout=15).content
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    f.write(audio_bytes)
                    mp3 = f.name
                wav = mp3.replace(".mp3", ".wav")
                AudioSegment.from_mp3(mp3).export(wav, format="wav")
                os.unlink(mp3)

                # Dịch giọng nói
                r = sr.Recognizer()
                with sr.AudioFile(wav) as src:
                    audio_data = r.record(src)
                text = r.recognize_google(audio_data).lower().strip()
                os.unlink(wav)
                print(f"{tag} 🗣️ STT: '{text}'")

                # Điền kết quả và bấm Xác minh
                try:
                    inp = ch_frame.locator("#audio-response")
                    inp.click(timeout=3000)
                    inp.fill(text)
                    page.wait_for_timeout(500)
                    
                    ch_frame.locator("#recaptcha-verify-button").click(timeout=3000)
                    page.wait_for_timeout(2500)
                except Exception as e:
                    print(f"{tag} ⚠️ Lỗi điền/xác minh: {e}")

                # Kiểm tra xem đã giải thành công chưa
                if is_checked():
                    print(f"{tag} ✅ CAPTCHA giải xong!")
                    return True

                # Nếu vẫn sai, kiểm tra xem có thông báo lỗi hiển thị không
                try:
                    err_el = ch_frame.locator(".rc-audiochallenge-error-message")
                    if err_el.is_visible(timeout=1000):
                        err_text = err_el.inner_text().strip()
                        if err_text:
                            print(f"{tag} ⚠️ Lỗi: '{err_text}', lấy audio mới...")
                            try:
                                ch_frame.locator("#recaptcha-reload-button").click(timeout=3000)
                                page.wait_for_timeout(2000)
                            except Exception:
                                pass
                            continue
                except Exception:
                    pass

            except sr.UnknownValueError:
                print(f"{tag} ⚠️ STT không nhận dạng được, lấy audio mới...")
                try:
                    ch_frame.locator("#recaptcha-reload-button").click(timeout=3000)
                    page.wait_for_timeout(2000)
                except Exception:
                    pass
            except Exception as e:
                if "closed" in str(e).lower() or (page and page.is_closed()):
                    print(f"{tag} 🚪 Trình duyệt đã bị đóng.")
                    return False
                print(f"{tag} ⚠️ Lỗi lần {attempt+1}: {e}")
                try:
                    page.wait_for_timeout(1000)
                except Exception:
                    pass

        print(f"{tag} ❌ Hết 5 lần thử, CAPTCHA thất bại")
        return False

    except Exception as e:
        if "closed" in str(e).lower() or (page and page.is_closed()):
            print(f"{tag} 🚪 Trình duyệt đã bị đóng.")
        else:
            print(f"{tag} ❌ solve_recaptcha: {e}")
        return False


# ─── LƯU FILE ─────────────────────────────────────────────────────────────────
def append_account(email, password):
    with _lock:
        accounts = []
        if os.path.exists(ACCOUNTS_FILE):
            try:
                with open(ACCOUNTS_FILE, "r") as f:
                    accounts = json.load(f)
            except Exception:
                pass
        if not any(a.get("email") == email for a in accounts):
            accounts.append({"email": email, "password": password})
            with open(ACCOUNTS_FILE, "w") as f:
                json.dump(accounts, f, indent=4)
            print(f"  💾 {ACCOUNTS_FILE} → {len(accounts)} tài khoản")


# ─── TẠO MỘT TÀI KHOẢN ───────────────────────────────────────────────────────
def create_one_account(worker_id: int, num: int) -> dict | None:
    tag = f"[W{worker_id}|#{num}]"
    mail = ResilientMail()

    try:
        email = mail.create()
        print(f"{tag} 📧 {email}")
    except Exception as e:
        print(f"{tag} ❌ Email: {e}")
        return None

    first   = random.choice(FIRST_NAMES)
    last    = random.choice(LAST_NAMES)
    phone   = random_phone()
    company = random.choice(COMPANIES) + " " + rand_str(4).upper()
    location = random.choice(LOCATIONS)

    # headless=False để debug trực quan
    proxy = PROXIES[num % len(PROXIES)] if PROXIES else None
    if proxy:
        print(f"{tag} 🌐 Proxy: {proxy['server']}")
    browser = launch(headless=False, humanize=True)
    # Cung cấp đầy đủ quyền định vị, timezone và locale từ hệ thống để tăng điểm tin cậy (trust score) với Google
    context = browser.new_context(
        locale="vi-VN",
        timezone_id="Asia/Ho_Chi_Minh",
        permissions=["geolocation"],
        **({"proxy": proxy} if proxy else {})
    )
    page    = context.new_page()

    try:
        # ── PAGE 1: Thông tin cơ bản ──────────────────────────────────────────
        page.goto("https://employer.vietnamworks.com/v2/signup/", wait_until="domcontentloaded")
        page.wait_for_timeout(800)

        page.locator("input[name='firstName']").fill(first)
        page.locator("input[name='lastName']").fill(last)
        page.locator("input[name='phoneNumber']").fill(phone)
        page.locator("input[name='emailAddress']").fill(email)
        page.locator("input[name='password']").fill(PASSWORD)
        page.locator("input[name='reenterPassword']").fill(PASSWORD)
        page.wait_for_timeout(300)

        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(1000)
        print(f"{tag} ✅ Page 1 xong")

        # ── PAGE 2: Công ty + location ────────────────────────────────────────
        page.wait_for_timeout(1500) # Đợi page 2 render xong
        try:
            page.get_by_role("textbox").first.fill(company)
        except Exception:
            pass
        try:
            loc_input = page.locator(".ant-select-selection-search-input").nth(1)
            loc_input.click(force=True, timeout=3000)
            page.wait_for_timeout(500) # Đợi dropdown cũ đóng và dropdown mới mở
            opts = page.locator(".ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option:visible")
            opts.first.wait_for(state="visible", timeout=5000)
            
            count = opts.count()
            if count > 0:
                opts.nth(random.randint(0, min(count - 1, 10))).click(timeout=3000)
        except Exception as e:
            print(f"{tag} ⚠️ Location error: {e}")
        page.wait_for_timeout(300)

        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(1000)
        print(f"{tag} ✅ Page 2 xong")

        # ── PAGE 3: Hiring Info ───────────────────────────────────────────────
        page.wait_for_timeout(1500) # Đợi page 3 render xong
        print(f"{tag} 📝 Điền Hiring Info...")

        # 1. Job title — react-select (Dùng keyboard.type thay vì fill id)
        try:
            # Click vào control để mở dropdown
            page.locator(".react-select__control").click(timeout=3000)
            page.wait_for_timeout(600)
            # Type trực tiếp bằng bàn phím (an toàn hơn là tìm ô input bên trong)
            page.keyboard.type("Software Engineer", delay=50)
            page.wait_for_timeout(800)
            # Chọn option đầu tiên xuất hiện
            page.locator(".react-select__option").first.click(timeout=3000)
            print(f"{tag} ✅ Job title ok")
        except Exception as e:
            print(f"{tag} ⚠️ Job title: {e}")

        # 2. Job level — ant-select-multiple (optional)
        try:
            lvl_input = page.locator("label", has_text="level").locator("xpath=..").locator(".ant-select-selection-search-input").first
            # Đề phòng trường hợp label không chứa "level" hoặc structure bị đổi
            if lvl_input.count() == 0:
                lvl_input = page.locator(".ant-select-selection-search-input").nth(0)
            
            lvl_input.click(force=True, timeout=3000)
            page.wait_for_timeout(500) # Đợi dropdown mở
            opts = page.locator(".ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option:visible")
            opts.first.click(timeout=3000)
            
            page.wait_for_timeout(200)
            page.keyboard.press("Escape")
            print(f"{tag} ✅ Job level ok")
        except Exception as e:
            print(f"{tag} ⚠️ Job level: {e}")

        # 3. Budget
        try:
            bg_input = page.locator("label", has_text="budget").locator("xpath=..").locator(".ant-select-selection-search-input").first
            if bg_input.count() == 0:
                bg_input = page.locator(".ant-select-selection-search-input").nth(1)
            
            bg_input.click(force=True, timeout=3000)
            page.wait_for_timeout(500)
            opts = page.locator(".ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option:visible")
            opts.first.click(timeout=3000)
            
            print(f"{tag} ✅ Budget ok")
        except Exception as e:
            print(f"{tag} ⚠️ Budget: {e}")

        # 3. Terms checkbox — input[name="ckPolicy"]
        try:
            page.locator("input[name='ckPolicy']").check()
            print(f"{tag} ✅ Terms ok")
        except Exception as e:
            print(f"{tag} ⚠️ Terms: {e}")

        page.wait_for_timeout(500)

        # ── CAPTCHA ─────────────────────────────────────────────────
        if not solve_recaptcha_audio(page, tag):
            print(f"{tag} ❌ CAPTCHA không vượt qua được, dừng.")
            return None

        # ── Submit ─────────────────────────────────────────────────
        try:
            submit_btn = page.locator("button[type='submit']").first
            submit_btn.click(timeout=5000)
        except Exception:
            try:
                page.get_by_role("button", name="Submit").click(timeout=5000)
            except Exception as e:
                print(f"{tag} ❌ Không thể click Submit: {e}")
                return None
        page.wait_for_timeout(2000)
        print(f"{tag} ✅ Submitted!")


        # ── KÍCH HOẠT EMAIL ───────────────────────────────────────────────────
        email_data = mail.wait_email()
        if email_data:
            subj = email_data.get("subject", "")
            print(f"{tag} 📨 Subject: {subj}")
            link = extract_link(email_data)
            if link:
                act = context.new_page()
                try:
                    act.goto(link, wait_until="domcontentloaded", timeout=12000)
                    act.wait_for_timeout(1000)
                    print(f"{tag} ✅ Kích hoạt xong!")
                except Exception as e:
                    print(f"{tag} ⚠️ Link: {e}")
                finally:
                    act.close()
            else:
                print(f"{tag} ⚠️ Không tìm được link kích hoạt")
        else:
            print(f"{tag} ⚠️ Timeout email")

        return {"email": email, "password": PASSWORD}

    except Exception as e:
        print(f"{tag} ❌ {e}")
        return None
    finally:
        try:
            context.close()
            browser.close()
        except Exception:
            pass


# ─── FREE PROXY SCRAPER ────────────────────────────────────────────────────────
def fetch_free_proxies():
    print("🌐 Đang tự động quét danh sách Proxy miễn phí để xoay vòng tránh chặn IP...")
    proxies = [None]  # Giữ lại IP thật làm phương án đầu tiên
    try:
        url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            lines = r.text.strip().splitlines()
            count = 0
            for line in lines:
                line_str = line.strip()
                if line_str and ":" in line_str:
                    if not (line_str.startswith("http://") or line_str.startswith("https://") or line_str.startswith("socks") or line_str.startswith("socks5://")):
                        line_str = f"http://{line_str}"
                    proxies.append({"server": line_str})
                    count += 1
            print(f"✅ Đã nạp thành công {count} Proxy miễn phí vào hệ thống!")
    except Exception as e:
        print(f"⚠️ Không thể cào proxy tự động: {e}")
    return proxies


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    global PROXIES
    print("=" * 60)
    print(f"  🚀 TẠO {NUM_ACCOUNTS} TÀI KHOẢN | {PARALLEL_WORKERS} LUỒNG")
    print(f"  Password: {PASSWORD} | File: {ACCOUNTS_FILE}")
    print("=" * 60)

    # Tự động tải free proxies nếu AUTO_SCRAPE_PROXIES là True và PROXIES chỉ chứa None hoặc rỗng
    if AUTO_SCRAPE_PROXIES and len(PROXIES) <= 1 and PROXIES[0] is None:
        PROXIES = fetch_free_proxies()

    t_start  = time.time()
    results  = []

    with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as pool:
        futures = {
            pool.submit(create_one_account, (i % PARALLEL_WORKERS) + 1, i + 1): i + 1
            for i in range(NUM_ACCOUNTS)
        }
        for future in as_completed(futures):
            num = futures[future]
            try:
                acc = future.result()
                if acc:
                    results.append(acc)
                    append_account(acc["email"], acc["password"])
                else:
                    print(f"  ❌ #{num} thất bại")
            except Exception as e:
                print(f"  ❌ #{num} exception: {e}")

    elapsed = time.time() - t_start
    print("\n" + "=" * 60)
    print(f"  ✅ {len(results)}/{NUM_ACCOUNTS} tài khoản | ⏱ {elapsed:.0f}s")
    print("=" * 60)
    for acc in results:
        print(f'  email: str = "{acc["email"]}"')
        print(f'  password: str = "{acc["password"]}"')
        print()
    print(f"  📁 {ACCOUNTS_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
