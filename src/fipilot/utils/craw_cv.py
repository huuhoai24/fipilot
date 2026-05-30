import re
import os
import csv
import json
import base64
import signal
import sys
from datetime import datetime
from cloakbrowser import launch
from config.settings import cfg

# Flag toàn cục để dừng graceful khi nhấn Ctrl+C
_stop_requested = False

class SwitchAccountException(Exception):
    pass

# Đường dẫn file CSV và JSON cơ sở dữ liệu để đối chiếu loại trùng
CSV_PATH = "data/candidates_lead_list.csv"
DB_PATH = "data/crawled_db.json"

def block_unnecessary_resources(route):
    """Chặn các tài nguyên không cần thiết để tăng tốc"""
    resource_type = route.request.resource_type
    if resource_type in ["image", "font", "media"]:
        route.abort()
    else:
        route.continue_()

# DANH SÁCH ROLE CẦN CÀO VÀ SỐ LƯỢNG YÊU CẦU TƯƠNG ỨNG
TARGET_ROLES = {
    # Backend
    # "Backend Developer": 150,
    # "Java Backend": 70,
    # ".NET Backend": 50,
    # "Python Backend": 70,
    
    # Frontend
    # "Frontend Developer": 70,
    # "React Developer": 50,
    # "Vue Developer": 35,
    # "UI Engineer": 15,
    
    # Fullstack
    # "Fullstack Developer": 80,
    
    # Mobile
    # "Android Developer": 50,
    # "iOS Developer": 30,
    # "Flutter Developer": 20,
    
    # AI/ML/Data
    "AI Engineer": 100,
    # "ML Engineer": 70,
    # "LLM Engineer": 70,
    # "Applied AI Engineer": 50,
    # "NLP Engineer": 50,
    # "Computer Vision Engineer": 30,
    # "MLOps Engineer": 40,
    # "Data Scientist": 40,
    # "Data Engineer": 45,
    # "Data Analyst": 50,
    # "BI Analyst": 15,
    # "Big Data Engineer": 10,
    
    # # DevOps/Cloud/Infra
    # "DevOps Engineer": 60,
    # "Cloud Engineer": 35,
    # "Kubernetes Engineer": 20,
    # "Platform Engineer": 15,
    
    # # Security
    # "Security Engineer": 30,
    # "DevSecOps Engineer": 20,
    
    # # QA/QC/Testing
    # "QA Engineer": 30,
    # "Automation Tester": 35,
    # "Manual Tester": 20,
    
    # # Embedded/IoT
    # "Embedded Engineer": 20,
    # "IoT Engineer": 15,
    
    # # IT/System
    # "System Administrator": 15,
    # "Network Engineer": 15,
    # "IT Support": 15,
    
    # # Business/Product
    # "Business Analyst": 30,
    # "Product Owner": 15,
    # "Product Manager": 20,
    
    # # Design
    # "UI Designer": 20,
    # "UX Designer": 15,
    
    # # Management/Architecture
    # "Tech Lead": 15,
    # "Engineering Manager": 8,
    # "Solution Architect": 7,
    # "Project Manager": 10,
    
    # # Game
    # "Game Developer": 15
}

def load_database():
    """Tải cơ sở dữ liệu các CV đã cào từ file JSON"""
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_database(db):
    """Lưu cơ sở dữ liệu các CV đã cào vào file JSON"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

def get_account_from_json(current_email=None):
    """Lấy tài khoản chưa sử dụng từ account.json và comment tài khoản đã dùng."""
    if not os.path.exists("account.json"):
        return None, None
    try:
        with open("account.json", "r", encoding="utf-8") as f:
            accounts = json.load(f)
            
        # Đánh dấu tài khoản hiện tại là đã dùng
        if current_email:
            for acc in accounts:
                if acc.get("email") == current_email:
                    acc["used"] = True
            # Cập nhật lại file
            with open("account.json", "w", encoding="utf-8") as f:
                json.dump(accounts, f, indent=4)
                
        # Tìm tài khoản chưa dùng
        for acc in accounts:
            if not acc.get("used"):
                return acc.get("email"), acc.get("password")
    except Exception as e:
        print(f"Lỗi khi đọc/ghi account.json: {e}")
    return None, None

def login_account(page, email, password):
    """Thực hiện đăng nhập"""
    print(f"Đang đăng nhập với tài khoản: {email}...")
    try:
        os.makedirs("debug", exist_ok=True)
        page.goto("https://employer.vietnamworks.com/v2/login/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        page.screenshot(path="debug/login_page.png")
        print(f"Đã mở trang đăng nhập. URL hiện tại: {page.url}")
        
        # Check if email input exists
        if not page.locator("input[name=\"email\"]").is_visible():
            print("Không tìm thấy ô nhập email, chụp màn hình...")
            page.screenshot(path="debug/login_no_email.png")
            
        page.locator("input[name=\"email\"]").fill(email)
        page.locator("input[name=\"password\"]").fill(password)
        page.screenshot(path="debug/login_filled.png")
        
        page.get_by_role("button", name="Sign in").click()
        print("Đã click nút Sign in. Chờ chuyển trang...")
        
        page.wait_for_timeout(5000)
        page.screenshot(path="debug/after_signin.png")
        print(f"Sau đăng nhập. URL hiện tại: {page.url}")
    except Exception as e:
        print(f"Lỗi khi thực hiện đăng nhập: {e}")
        try:
            page.screenshot(path="debug/login_error.png")
        except Exception:
            pass


def save_to_csv(candidates):
    """Ghi danh sách ứng viên vào file CSV"""
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    file_exists = os.path.exists(CSV_PATH)
    
    headers = [
        "id", "name", "role", "experience", "salary", 
        "location", "last_updated", "vietnamworks_url", 
        "pdf_path", "search_query"
    ]
    
    try:
        with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            for candidate in candidates:
                writer.writerow(candidate)
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def extract_candidate_id(url: str) -> str:
    """Trích xuất ID duy nhất của ứng viên từ URL"""
    if not url:
        return ""
    match = re.search(r'candidate-detail/([^/?#]+)', url)
    if match:
        return match.group(1).split("?")[0]
    return url.split("/")[-1].split("?")[0]

def count_crawled_for_role(db, role_name):
    """Đếm xem role này đã cào được bao nhiêu ứng viên trong database"""
    target = role_name.strip()
    return sum(1 for c in db.values() if c.get("search_query", "").strip() == target)

def print_progress_report(db, session_downloaded=0, current_role=None, reason=""):
    """In báo cáo tiến trình chi tiết cho tất cả các role"""
    print(f"\n{'='*75}")
    print(f"  BÁO CÁO TIẾN TRÌNH CÀO CV  —  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if reason:
        print(f"  Lý do: {reason}")
    print(f"{'='*75}")
    
    total_target = 0
    total_done = 0
    total_remaining = 0
    
    done_roles = []
    pending_roles = []
    
    for role, target in TARGET_ROLES.items():
        done = count_crawled_for_role(db, role)
        remaining = max(0, target - done)
        total_target += target
        total_done += done
        total_remaining += remaining
        
        if remaining == 0:
            done_roles.append((role, done, target))
        else:
            pending_roles.append((role, done, target, remaining))
    
    # In các role chưa hoàn thành (cần chú ý)
    if pending_roles:
        print(f"\n  {'ROLE CẦN TẢI THÊM':<35} {'ĐÃ CÓ':>8} {'MỤC TIÊU':>10} {'CÒN THIẾU':>10}")
        print(f"  {'-'*65}")
        for role, done, target, remaining in pending_roles:
            marker = " ◀◀◀" if current_role and role == current_role else ""
            pct = (done / target * 100) if target > 0 else 0
            bar_len = 15
            filled = int(bar_len * pct / 100)
            bar = '█' * filled + '░' * (bar_len - filled)
            print(f"  {role:<35} {done:>5}/{target:<4} {bar} {remaining:>5} còn thiếu{marker}")
    
    # In các role đã hoàn thành
    if done_roles:
        print(f"\n  ✅ ĐÃ HOÀN THÀNH ({len(done_roles)} roles):")
        names = [f"{r}({d})" for r, d, _ in done_roles]
        # In 3 role mỗi dòng
        for i in range(0, len(names), 3):
            print(f"     {', '.join(names[i:i+3])}")
    
    # Tổng kết
    overall_pct = (total_done / total_target * 100) if total_target > 0 else 0
    print(f"\n  {'─'*65}")
    print(f"  TỔNG CỘNG: {total_done}/{total_target} CVs ({overall_pct:.1f}%)  |  Còn thiếu: {total_remaining}")
    if session_downloaded > 0:
        print(f"  Phiên này đã tải thêm: {session_downloaded} CVs mới")
    print(f"  Database: {len(db)} records  |  File: {DB_PATH}")
    print(f"{'='*75}\n")

def run() -> None:
    global _stop_requested
    
    # Bắt tín hiệu Ctrl+C để dừng graceful
    def signal_handler(signum, frame):
        global _stop_requested
        _stop_requested = True
        print("\n\n⚠️  Nhận tín hiệu DỪNG (Ctrl+C). Đang lưu dữ liệu và thoát an toàn...")
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Loading local database...")
    db = load_database()
    
    # In báo cáo tiến trình ban đầu
    print_progress_report(db, reason="BẮT ĐẦU PHIÊN CÀO MỚI")
    
    print("Launching CloakBrowser...")
    # browser = launch(headless=False, humanize=False)
    browser = launch(headless=True, humanize=False)
    
    context = browser.new_context()
    page = context.new_page()
    page.route("**/*", block_unnecessary_resources)
    session_total_downloaded = 0  # Đếm tổng số CV tải được trong phiên này
    current_role = None
    
    # Lấy tài khoản đầu tiên
    current_email, current_password = get_account_from_json()
    if not current_email:
        current_email, current_password = cfg.email, cfg.password
        
    login_account(page, current_email, current_password)
            
    # DUYỆT QUA TỪNG ROLE TRONG DANH SÁCH YÊU CẦU
    try:
        roles_items = list(TARGET_ROLES.items())
        role_idx = 0
        while role_idx < len(roles_items):
            search_role, target_qty = roles_items[role_idx]
            try:
                if _stop_requested:
                        print("\n⛔ Dừng theo yêu cầu người dùng (Ctrl+C).")
                        break
            
                current_role = search_role
                already_crawled = count_crawled_for_role(db, search_role)
                needed = target_qty - already_crawled
            
                if needed <= 0:
                    print(f"\n[HOÀN THÀNH] Role '{search_role}' đã đủ ({already_crawled}/{target_qty}). Bỏ qua.")
                    role_idx += 1
                    continue
                    
                print(f"\n=======================================================")
                print(f"TIẾN HÀNH TẢI CV PDF CHO ROLE: '{search_role}'")
                print(f"Tài khoản: {current_email}")
                print(f"Yêu cầu: {target_qty} | Đã có: {already_crawled} | Cần tải thêm: {needed}")
                print(f"=======================================================")
            
                # Khởi tạo lại trang tìm kiếm bằng cách quay lại dashboard và click nút Search Resumes
                print("Đang điều hướng tới dashboard để truy cập trang tìm kiếm...")
                page.goto("https://employer.vietnamworks.com/v2/", wait_until="domcontentloaded")
                page.wait_for_timeout(3000)
                
                # In ra tất cả link/button để tự động phát hiện selector đúng
                print("--- DANH SÁCH CÁC NÚT BẤM / ĐƯỜNG DẪN TRÊN DASHBOARD ---")
                elements = page.locator("a, button").all()
                search_btn_to_click = None
                for el in elements:
                    try:
                        text = el.inner_text().strip()
                        href = el.get_attribute("href") or ""
                        lower_text = text.lower()
                        lower_href = href.lower()
                        if text or href:
                            if "search" in lower_text or "search" in lower_href or "tìm" in lower_text:
                                print(f"  [PHÁT HIỆN] Text: '{text}' | Href: '{href}'")
                            # Kiểm tra khớp chính xác hoặc khớp phần lớn các từ khóa tìm kiếm hồ sơ
                            if ("search" in lower_text and "resume" in lower_text) or "search-resume" in lower_href or text == "Search resumes":
                                search_btn_to_click = el
                    except Exception:
                        pass
                print("-------------------------------------------------------")
                
                search_clicked = False
                if search_btn_to_click:
                    try:
                        print("Đang click thử phần tử tìm kiếm đã phát hiện...")
                        search_btn_to_click.click(timeout=10000)
                        page.wait_for_load_state("domcontentloaded")
                        print(f"Đã click thành công. URL hiện tại: {page.url}")
                        search_clicked = True
                    except Exception as e:
                        print(f"Lỗi khi click phần tử phát hiện được: {e}")
                
                if not search_clicked:
                    # Cố gắng tìm và click bằng các selector phổ biến
                    try:
                        search_btn = page.locator("a:has-text('Search resumes'), button:has-text('Search resumes'), [href*='search']").first
                        if search_btn.is_visible():
                            search_btn.click(timeout=10000)
                            page.wait_for_load_state("domcontentloaded")
                            print(f"Đã click Search Resumes bằng locator dự phòng. URL hiện tại: {page.url}")
                            search_clicked = True
                    except Exception as e:
                        print(f"Lỗi khi click locator dự phòng: {e}")
                
                if not search_clicked:
                    # Thử đi thẳng tới các URL có khả năng
                    print("Thử đi trực tiếp tới các URL tìm kiếm tiềm năng...")
                    for url in ["https://employer.vietnamworks.com/v2/search-resumes", "https://employer.vietnamworks.com/v2/search-resume"]:
                        try:
                            page.goto(url, wait_until="domcontentloaded", timeout=15000)
                            if page.locator("input[name='search']").is_visible(timeout=5000):
                                print(f"Đã tìm thấy ô tìm kiếm tại URL: {url}")
                                search_clicked = True
                                break
                        except Exception:
                            pass
                
                try:
                    page.wait_for_selector("input[name='search']", timeout=15000)
                except Exception:
                    print("Không thể tìm thấy input[name='search']. Chụp ảnh màn hình debug...")
                    os.makedirs("debug", exist_ok=True)
                    page.screenshot(path=f"debug/search_error_{search_role}.png")
                    
                page.wait_for_timeout(500)
        
        
                # Bước 1: Xóa các tag tìm kiếm cũ (nút X bên cạnh keyword cũ)
                close_btns = page.locator("i.icon-close.css-1vt7l4k").all()
                for btn in close_btns:
                    try:
                        btn.click()
                        page.wait_for_timeout(100)
                    except Exception:
                        pass
        
                # Bước 2: Nhập từ khóa mới vào ô input React
                search_input = page.locator("input[name='search']")
        
                clean_role = search_role.strip()
                max_type_attempts = 3
                current_val = ""
                for attempt in range(max_type_attempts):
                    try:
                        search_input.click()
                        page.wait_for_timeout(150)
                
                        # Thử fill() trước - nhanh và chính xác
                        search_input.fill(clean_role)
                        page.wait_for_timeout(300)
                
                        current_val = search_input.input_value().strip()
                        if current_val == clean_role:
                            break
                
                        # fill() không trigger React state → thử press_sequentially
                        search_input.click(click_count=3)
                        search_input.press("Delete")
                        page.wait_for_timeout(150)
                        search_input.press_sequentially(clean_role, delay=40)
                        page.wait_for_timeout(300)
                
                        current_val = search_input.input_value().strip()
                        if current_val == clean_role:
                            break
                    except Exception as e:
                        print(f"  Lỗi khi gõ từ khóa: {e}")
            
                    print(f"  [CẢNH BÁO] Nhập chưa khớp (được: '{current_val}', cần: '{clean_role}'). Đang gõ lại ({attempt + 1}/{max_type_attempts})...")
        
                print(f"  Ô search hiện tại: '{current_val}'")
        
                # Bước 3: Click nút Search
                page.locator("button.css-c3i2i2, button:has-text('Search')").last.click()
                print(f"  Đang chờ kết quả tìm kiếm cho '{search_role}'...")
        
                # Bước 4: Chờ loading spinner biến mất
                try:
                    page.wait_for_selector(".ant-spin, .loading, .ant-spin-spinning", timeout=3000)
                    page.wait_for_selector(".ant-spin, .ant-spin-spinning", state="hidden", timeout=15000)
                except Exception:
                    pass
        
                # Bước 5: Chờ DOM ổn định nhanh
                try:
                    page.wait_for_load_state("domcontentloaded", timeout=5000)
                except Exception:
                    pass
        
                page.wait_for_timeout(1000)
        
                downloaded_count = 0
                page_index = 0
        
                while downloaded_count < needed:
                    if _stop_requested:
                        break
                
                    print(f"\n--- [{search_role}] Page {page_index + 1} ---")
            
                    try:
                        page.wait_for_selector('button:has-text("View detail")', timeout=10000)
                    except Exception:
                        print(f"Không tìm thấy ứng viên cho role '{search_role}'. Chuyển sang role khác.")
                        break
                
                    page.wait_for_timeout(500)
            
                    cards = page.locator("div.css-d2ccqw").all()
                    if not cards:
                        cards = page.locator("//div[descendant::button[contains(text(), 'View detail')]]").all()
                
                    if not cards:
                        print("Không tìm thấy khối card ứng viên nào. Chuyển sang role khác.")
                        break
                
                    print(f"Phát hiện {len(cards)} ứng viên trên page {page_index + 1}.")
            
                    page_new_candidates = []
            
                    for card in cards:
                        if downloaded_count >= needed or _stop_requested:
                            break
                
                        name = "unknown"
                        page1 = None
                    
                        try:
                            name_link = card.locator("a.css-h9n7oy, a[href*='candidate-detail']").first
                            if not name_link.is_visible():
                                continue
                        
                            name = name_link.inner_text().strip()
                            relative_url = name_link.get_attribute("href")
                            vietnamworks_url = f"https://employer.vietnamworks.com{relative_url}" if relative_url.startswith("/") else relative_url
                    
                            candidate_id = extract_candidate_id(vietnamworks_url)
                    
                            role_el = card.locator("p.css-1oavcwl, p[class*='role']").first
                            role = role_el.inner_text().strip() if role_el.is_visible() else search_role
                    
                            safe_role = re.sub(r'[^\w\s-]', '', role).strip().replace(" ", "_") if role else "AI"
                            safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(" ", "_")
                            if not safe_name:
                                safe_name = f"candidate_{candidate_id}"
                            pdf_path = f"data/{safe_role}_{safe_name}.pdf"
                    
                            # Kiểm tra trùng lặp
                            if candidate_id in db or os.path.exists(pdf_path):
                                if candidate_id not in db:
                                    db[candidate_id] = {
                                        "name": name,
                                        "file_path": pdf_path,
                                        "url": vietnamworks_url,
                                        "search_query": search_role,
                                        "crawled_at": "unknown"
                                    }
                                    save_database(db)
                                print(f" -> [SKIP] '{name}' (ID: {candidate_id}) - Đã tải trước đó.")
                                continue
                    
                            # Thu thập metadata
                            updated_el = card.locator("p.css-1xw3g0c, p[class*='updated']").first
                            last_updated = updated_el.inner_text().replace("Last updated:", "").strip() if updated_el.is_visible() else ""
                    
                            info_elements = card.locator("div.css-1eid011 p.css-147exbc").all()
                            experience = "N/A"
                            salary = "N/A"
                            location = "N/A"
                            for el in info_elements:
                                text = el.inner_text().strip()
                                if "year" in text.lower() or "tháng" in text.lower() or "năm" in text.lower():
                                    experience = text
                                elif "$" in text or "negotiable" in text.lower() or "thỏa thuận" in text.lower():
                                    salary = text
                                elif "view full information" not in text.lower() and "buy search package" not in text.lower():
                                    location = text
                    
                            # Click "View detail"
                            print(f" -> [NEW] ({downloaded_count + 1}/{needed}) '{name}' (ID: {candidate_id}). Đang mở chi tiết...")
                    
                            view_detail_btn = card.get_by_role("button", name="View detail")
                            with page.expect_popup() as page1_info:
                                view_detail_btn.click()
                            page1 = page1_info.value
                    
                            page1.wait_for_load_state("domcontentloaded")
                            detail_url = page1.url
                    
                            # Kiểm tra xem có bị chặn bởi trial limitation không
                            if "limit-exceeded" in detail_url:
                                print("    [CẢNH BÁO] Tài khoản đã hết lượt xem trial! (limit-exceeded)")
                                page1.close()
                                raise SwitchAccountException("limit-exceeded")
                    
                            try:
                                # Đọc số lượt trial còn lại
                                trial_text_locator = page1.locator("div.css-lqk3j2", has_text="trial times")
                                if not trial_text_locator.is_visible(timeout=2000):
                                    trial_text_locator = page1.locator("div:has-text('trial times to view the resume')").last
                        
                                if trial_text_locator.is_visible(timeout=2000):
                                    trial_text = trial_text_locator.inner_text().strip()
                                    match = re.search(r'You have (\d+)\s*trial times', trial_text, re.IGNORECASE)
                                    if match:
                                        trial_left = int(match.group(1))
                                        print(f"    [INFO] Còn {trial_left} lượt xem trial.")
                                        if trial_left <= 1:
                                            print("    [CẢNH BÁO] Tài khoản chỉ còn <= 1 lượt xem! Sẽ đổi tài khoản sau CV này...")
                                            page1.evaluate("window.accountExhausted = true;")
                            except Exception as e:
                                pass
                    
                            try:
                                page1.get_by_role("button", name="Got it").click(timeout=2000)
                            except Exception:
                                pass
                        
                            print("    Đang tìm kiếm tệp PDF CV...")
                            blob_url = None
                            combined_selector = 'object.view-pdf, object[aria-label="PDF viewer"], object[data^="blob:"], iframe[src^="blob:"]'
                            try:
                                page1.wait_for_selector(combined_selector, timeout=8000)
                                el = page1.locator(combined_selector).first
                                blob_url = el.get_attribute('data') or el.get_attribute('src')
                            except Exception as e:
                                print(f"    Không tìm thấy selector PDF: {e}")
                                is_limit_exceeded = False
                                try:
                                    if "limit-exceeded" in page1.url:
                                        is_limit_exceeded = True
                                except Exception:
                                    pass
                                
                                if is_limit_exceeded:
                                    print("    [CẢNH BÁO] Tài khoản đã bị redirect sang trang hết hạn mức! (limit-exceeded)")
                                    try:
                                        page1.close()
                                    except Exception:
                                        pass
                                    raise SwitchAccountException("limit-exceeded-redirect")
                    
                            if blob_url and blob_url.startswith("blob:"):
                                base64_data = page1.evaluate("""async (url) => {
                                    const response = await fetch(url);
                                    const blob = await response.blob();
                                    return new Promise((resolve, reject) => {
                                        const reader = new FileReader();
                                        reader.onloadend = () => resolve(reader.result.split(',')[1]);
                                        reader.onerror = reject;
                                        reader.readAsDataURL(blob);
                                    });
                                }""", blob_url)
                        
                                pdf_bytes = base64.b64decode(base64_data)
                                os.makedirs("data", exist_ok=True)
                                with open(pdf_path, "wb") as f:
                                    f.write(pdf_bytes)
                                
                                candidate_data = {
                                    "id": candidate_id,
                                    "name": name,
                                    "role": role,
                                    "experience": experience,
                                    "salary": salary,
                                    "location": location,
                                    "last_updated": last_updated,
                                    "vietnamworks_url": vietnamworks_url,
                                    "pdf_path": pdf_path,
                                    "search_query": search_role
                                }
                        
                                page_new_candidates.append(candidate_data)
                        
                                db[candidate_id] = {
                                    "name": name,
                                    "file_path": pdf_path,
                                    "url": detail_url,
                                    "search_query": search_role,
                                    "crawled_at": page.evaluate("new Date().toISOString()")
                                }
                        
                                downloaded_count += 1
                                session_total_downloaded += 1
                                print(f"    [OK] '{name}' -> {pdf_path}")
                        
                                save_database(db)
                                page.wait_for_timeout(500)
                            else:
                                print("    [FAIL] Không tìm thấy tệp PDF CV hợp lệ.")
                        
                            # Kiểm tra flag đổi tài khoản
                            is_exhausted = False
                            try:
                                is_exhausted = page1.evaluate("window.accountExhausted === true")
                            except Exception:
                                pass
                        
                            page1.close()
                    
                            if is_exhausted:
                                raise SwitchAccountException("Trial left <= 1")
                    
                        except SwitchAccountException:
                            raise
                        except SystemExit:
                            raise
                        except Exception as e:
                            print(f" -> Lỗi khi xử lý ứng viên '{name}': {e}")
                            if page1:
                                try:
                                    page1.close()
                                except Exception:
                                    pass
                        
                    if page_new_candidates:
                        save_to_csv(page_new_candidates)
                        save_database(db)
                        print(f"Đã lưu thành công {len(page_new_candidates)} CVs cho role '{search_role}'.")
                
                    # Phân trang
                    if downloaded_count < needed and not _stop_requested:
                        print("Chuyển trang kết quả...")
                        next_btn = page.locator("li[title='Next Page'] button, li.ant-pagination-next button").first
                        if next_btn.is_visible() and next_btn.is_enabled():
                            next_btn.click()
                            try:
                                page.wait_for_selector(".ant-spin, .ant-spin-spinning", timeout=2000)
                                page.wait_for_selector(".ant-spin, .ant-spin-spinning", state="hidden", timeout=15000)
                            except Exception:
                                pass
                            try:
                                page.wait_for_load_state("domcontentloaded", timeout=5000)
                            except Exception:
                                pass
                            page.wait_for_timeout(1000)
                            page_index += 1
                        else:
                            print("Không thấy nút chuyển trang. Chuyển sang role mới.")
                            break
                print(f"Hoàn tất role '{search_role}'. Tải được {downloaded_count} CVs mới.")
                role_idx += 1
            
            except SwitchAccountException as e:
                print(f"\n🔄 Đã hết lượt xem ({e}). Tiến hành đổi tài khoản...")
                current_email, current_password = get_account_from_json(current_email)
                if not current_email:
                    print("\n❌ Hết tài khoản trong account.json. Dừng cào kịch bản.")
                    break
                else:
                    # Tạo lại context mới để xóa sạch 100% cache/cookies/local storage
                    try:
                        page.close()
                        context.close()
                    except Exception:
                        pass
                    
                    context = browser.new_context()
                    page = context.new_page()
                    page.route("**/*", block_unnecessary_resources)
                    
                    login_account(page, current_email, current_password)
                    print(f"Đã đổi tài khoản sang {current_email}, đang thử lại role '{search_role}'...")
                    continue
                        
    except SystemExit as e:
        print(f"\n⛔ Dừng do: {e}")
    except Exception as e:
        print(f"\n❌ LỖI KHÔNG MONG MUỐN: {e}")
    finally:
        # LUÔN LUÔN chạy dù thành công, lỗi, hay Ctrl+C
        # 1. Lưu database lần cuối
        try:
            save_database(db)
            print("\n💾 Database đã được lưu an toàn.")
        except Exception as e:
            print(f"\n⚠️ Lỗi khi lưu database: {e}")
        
        # 2. In báo cáo tiến trình cuối cùng
        if _stop_requested:
            reason = "DỪNG BỞI NGƯỜI DÙNG (Ctrl+C)"
        elif 'e' in dir() and isinstance(e, SystemExit) and "limit" in str(e).lower():
            reason = "HẾT HẠN MỨC TÀI KHOẢN"
        else:
            reason = "KẾT THÚC PHIÊN CÀO"
        
        print_progress_report(db, session_total_downloaded, current_role, reason)
        
        # 3. Đóng trình duyệt an toàn
        try:
            if context:
                context.close()
            if browser:
                browser.close()
            print("🌐 Browser đã đóng.")
        except Exception:
            pass
        
        print("\n🔄 Chạy lại script để tiếp tục tải các CV còn thiếu.")

if __name__ == "__main__":
    run()