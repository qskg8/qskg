import json
import time
from playwright.sync_api import sync_playwright
import random
import requests

# 配置参数
MIN_PAGE = 100000000000000000000000000
MAX_PAGE = 1929868153955269923726183083478131797547292737984581739710086052358636024906
API_KEY = '12RU83G1ATVA9V4EMM3U45X8BG4RG9PM6T'  # 示例API KEY
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
DINGTALK_WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=e40d2c94bb41f0b403d44fecb3e68f33af4c6dbff053e4aaaa09c2adaa43d219'  # 钉钉Webhook地址

def get_api_response(url):
    with sync_playwright() as p:
        # 配置浏览器参数
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()
        response_data = None

        # 响应拦截回调
        def handle_response(response):
            nonlocal response_data
            if response.url.startswith("https://api.etherscan.io/api") and "balancemulti" in response.url:
                try:
                    response_data = response.json()
                except:
                    print(f"[ERROR] 响应解析失败: {response.url}")

        page.on("response", handle_response)
        
        try:
            page.goto(url, timeout=60000)
            time.sleep(6 + random.uniform(1, 3))  # 随机延迟防止封禁
        except Exception as e:
            print(f"[TIMEOUT] 页面加载超时: {url}")
            return None
        finally:
            context.close()
            browser.close()
        
        return response_data

def generate_valid_page():
    """生成有效页面编号"""
    while True:
        # 生成符合范围的随机数
        num = random.randint(MIN_PAGE, MAX_PAGE)
        if num >= MIN_PAGE and num <= MAX_PAGE:
            return str(num)

def check_balance(data):
    """检查余额有效性"""
    valid_accounts = []
    if data.get("status") == "1":
        for account in data["result"]:
            balance = int(account["balance"])
            if balance > 0:
                valid_accounts.append({
                    "address": account["account"],
                    "balance_wei": balance,
                    "balance_eth": balance / 1e18
                })
    return valid_accounts

def send_dingtalk_message(message):
    """发送消息到钉钉群"""
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(DINGTALK_WEBHOOK, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("[INFO] 钉钉通知发送成功")
        else:
            print(f"[ERROR] 钉钉通知发送失败: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] 发送钉钉消息时发生错误: {str(e)}")

def main():
    base_url = "https://privatekeyfinder.io/private-keys/ethereum/"
    
    while True:
        try:
            # 生成目标页面
            page_num = generate_valid_page()
            target_url = f"{base_url}{page_num}"
            print(f"[INFO] 正在探测: {target_url}")

            # 获取API响应
            api_data = get_api_response(target_url)
            
            if not api_data:
                print(f"[WARN] 未获取到有效数据: {target_url}")
                continue

            # 解析有效余额
            valid = check_balance(api_data)
            if valid:
                with open("88.txt", "a", encoding="utf-8") as f:
                    for acc in valid:
                        record = (
                            f"发现有效账户 | 探测页面: {target_url}\n"
                            f"地址: {acc['address']}\n"
                            f"余额: {acc['balance_eth']:.18f} ETH\n"
                            f"原始数据: {acc['balance_wei']} wei\n"
                            f"{'-'*40}\n"
                        )
                        f.write(record)
                        print(record)
                        
                        # 向钉钉发送通知
                        dingtalk_message = (
                            f"发现有效账户！\n"
                            f"探测页面: {target_url}\n"
                            f"地址: {acc['address']}\n"
                            f"余额: {acc['balance_eth']:.18f} ETH\n"
                            f"原始数据: {acc['balance_wei']} wei\n"
                        )
                        send_dingtalk_message(dingtalk_message)
            
            # 随机间隔防止封禁
            time.sleep(random.uniform(4, 10))

        except Exception as e:
            print(f"[CRITICAL] 主循环错误: {str(e)}")
            time.sleep(30)

if __name__ == "__main__":
    main()
