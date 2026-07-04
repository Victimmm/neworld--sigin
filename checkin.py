"""
@File : checkin.py
@Author : WorkBuddy
@Date : 2026/7/4
@Description : 新界梯子每日自动签到脚本（适配新版 JSON API + 动态指纹）
"""
import requests
import os
import hashlib
import uuid
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def mask_secret(secret: str, head: int = 3, tail: int = 6) -> str:
    """脱敏显示账号"""
    if not secret:
        return ""
    if len(secret) <= head + tail:
        return "*" * len(secret)
    return secret[:head] + "*" * (len(secret) - head - tail) + secret[-tail:]


def generate_fingerprint(seed: str = "") -> str:
    """
    生成类似 FingerprintJS v3 的 visitorId。
    FingerprintJS 在新版登录页面中已改为动态生成，不再使用硬编码值。
    此函数基于用户名生成稳定的 32 位 hex 指纹，保证每次签到的指纹一致。
    """
    if seed:
        return hashlib.md5(seed.encode()).hexdigest()
    return uuid.uuid4().hex


def try_login(session, base_url: str, email: str, password: str) -> bool:
    """
    登录新界。
    新版登录接口使用 JSON 格式，并需要 fingerprint 字段。
    使用 requests.Session 自动管理登录后的 cookies。
    """
    url = f"{base_url}/auth/login"

    fingerprint = generate_fingerprint(email)

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json',
        'Origin': base_url,
        'Referer': f'{base_url}/auth/login',
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0.0.0 Safari/537.36'
        ),
        'X-Requested-With': 'XMLHttpRequest',
    }

    payload = {
        'code': '',
        'email': email,
        'passwd': password,
        'remember_me': 'false',
        'fingerprint': fingerprint,
    }

    try:
        resp = session.post(url, json=payload, headers=headers, timeout=30, verify=False)
        result = resp.json()
    except Exception as e:
        print(f"  请求异常: {e}")
        return False

    if result.get('ret') == 1:
        print(f"  ✅ 登录成功: {result.get('msg', '')}")
        return True
    else:
        print(f"  ❌ 登录失败: {result.get('msg', '')}")
        return False


def do_checkin(session, base_url: str):
    """执行签到请求"""
    url = f"{base_url}/user/checkin"

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '0',
        'Origin': base_url,
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0.0.0 Safari/537.36'
        ),
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        resp = session.post(url, headers=headers, timeout=30, verify=False)
        result = resp.json()
        print(f"  ✅ 签到结果: {result.get('msg', '')}")
    except Exception as e:
        print(f"  ❌ 签到请求异常: {e}")


def process_account(base_url: str, username_env: str, password_env: str):
    """处理单个账号：登录 → 签到"""
    user = os.environ.get(username_env)
    password = os.environ.get(password_env)

    if not user or not password:
        print(f"⚠️ 跳过 {username_env}/{password_env}：环境变量未配置")
        return

    print(f"用户账号：{mask_secret(user)}")

    # 每个账号使用独立会话，避免 cookie 串扰
    session = requests.Session()

    # 第一步：访问登录页获取初始 cookies
    try:
        session.get(f"{base_url}/auth/login", timeout=15, verify=False)
    except Exception as e:
        print(f"  ❌ 无法访问登录页: {e}")
        return

    # 第二步：登录
    if try_login(session, base_url, user, password):
        # 第三步：签到
        do_checkin(session, base_url)
    else:
        print("  ⏭️ 跳过签到")


def main():
    # ============================================================
    # 基础域名配置
    # 如果 neworld.cloud 无法使用，可改为 "https://neworld.tv"
    # ============================================================
    BASE_URL = "https://neworld.cloud"

    print(f"🌐 签到服务: {BASE_URL}")
    print(f"📅 {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 处理多个账号
    process_account(BASE_URL, "USERNAME", "PASSWORD")
    process_account(BASE_URL, "USERNAME8344", "PASSWORD8344")
    process_account(BASE_URL, "USERNAME1325", "PASSWORD1325")

    print("=" * 50)
    print("✅ 签到流程执行完毕")


if __name__ == "__main__":
    main()
