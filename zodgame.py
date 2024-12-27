import requests
import os

# 签到请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Cookie': os.environ['ZODGAME_COOKIE'],
    'Referer': 'https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign'
}

sign_url = "https://zodgame.xyz/plugin.php"
params = {
    'id': 'dsu_paulsign:sign',
    'operation': 'qiandao',
    'infloat': '1',
    'inajax': '1',
    'formhash': os.environ['ZODGAME_FORMHASH'],
    'qdxq': 'kx',
    'qdmode': '1',
    'todaysay': '我是第一个',
    'fastreply': '0'
}

try:
    # 执行签到
    response = requests.post(sign_url, params=params, headers=headers)
    message = response.text
    print(message)

    # 判断签到结果
    if "签到成功" in message:
        success = True
        import re
        reward = re.search(r'获得随机奖励\s*(.*?)\s*\.\s*', message)
        reward_text = reward.group(1) if reward else "未知奖励"
        status_message = f"签到成功！奖励：{reward_text}"
    else:
        success = False
        status_message = "签到失败或已经签到"

    # Gotify 推送
    gotify_url = os.environ['GOTIFY_URL']
    gotify_token = os.environ['GOTIFY_TOKEN']

    print("**开始执行 Gotify 推送:**\n")
    gotify_response = requests.post(
        gotify_url,
        headers={"X-Gotify-Key": gotify_token},
        json={
            "title": "Zodgame签到",
            "message": status_message,
            "priority": 5 if success else 8
        }
    )

    if gotify_response.status_code == 200:
        print(f"Gotify 消息推送成功: {status_message}\n")
    else:
        print(f"推送失败，状态码: {gotify_response.status_code}\n")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {str(e)}")