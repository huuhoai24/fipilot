import os
import json
import base64
from cloakbrowser import launch
from config.settings import cfg

def main():
    print("Launching CloakBrowser...")
    browser = launch(headless=True, humanize=False)
    context = browser.new_context()
    page = context.new_page()
    
    email = "l2cu3whrp37n@wshu.net"
    password = "Fipilot2025@"
    
    print(f"Đăng nhập với tài khoản: {email}...")
    page.goto("https://employer.vietnamworks.com/v2/login/", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.locator("input[name=\"email\"]").fill(email)
    page.locator("input[name=\"password\"]").fill(password)
    page.get_by_role("button", name="Sign in").click()
    
    page.wait_for_timeout(5000)
    print(f"URL hiện tại: {page.url}")
    
    # In toàn bộ các link và button có trên trang
    elements = page.locator("a, button").all()
    print(f"Tìm thấy {len(elements)} liên kết/nút bấm trên trang:")
    
    results = []
    for i, el in enumerate(elements):
        try:
            tag = el.evaluate("el => el.tagName.toLowerCase()")
            text = el.inner_text().strip()
            href = el.get_attribute("href") or ""
            outer_html = el.evaluate("el => el.outerHTML")
            
            if "search" in text.lower() or "search" in href.lower() or "tìm" in text.lower():
                item = f"[{i}] TAG: {tag} | TEXT: '{text}' | HREF: '{href}' | HTML: {outer_html[:200]}"
                print(item)
                results.append(item)
        except Exception as e:
            pass
            
    # Lưu kết quả
    os.makedirs("debug", exist_ok=True)
    with open("debug/elements_search.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
        
    context.close()
    browser.close()
    print("Xong!")

if __name__ == "__main__":
    main()
