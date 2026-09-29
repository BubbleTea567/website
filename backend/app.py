from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time

app = Flask(__name__)
# 允许前端跨域访问（开发阶段方便本地联调）
CORS(app)

# ============ 模拟数据 ============
# 香草猫娘的各种反应文案
GREETINGS = [
    {"text": "喵～ 主人你来啦～", "mood": "happy", "emoji": "😺"},
    {"text": "香草味的小鱼干…想吃！", "mood": "hungry", "emoji": "🐟"},
    {"text": "今天也要摸摸头吗？", "mood": "shy", "emoji": "😽"},
    {"text": "呜…被摸头好舒服喵～", "mood": "blissful", "emoji": "💕"},
    {"text": "主人主人，陪我玩一会儿嘛～", "mood": "playful", "emoji": "🐾"},
    {"text": "喵呜…有点困了呢…", "mood": "sleepy", "emoji": "😴"},
    {"text": "香草猫娘，随时待命喵！", "mood": "cheerful", "emoji": "🌿"},
]

# 猫娘状态（简单内存存储，仅作演示）
neko_state = {
    "name": "香草猫娘",
    "fullness": 80,
    "mood_level": 90,
    "affection": 42,
}

# ============ API 接口 ============

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "service": "vanilla-neko-backend",
        "timestamp": time.time()
    })


@app.route('/api/greet', methods=['POST'])
def greet():
    """
    摸摸猫娘 —— 前端点击按钮时调用
    返回一句猫娘的反应 + 更新后的状态
    """
    data = request.get_json(silent=True) or {}
    action = data.get('action', 'pat')  # 默认动作：摸头

    # 根据不同动作选择不同回复
    if action == 'feed':
        reply = {"text": "小鱼干！最喜欢了喵～", "mood": "happy", "emoji": "🐟"}
        neko_state["fullness"] = min(100, neko_state["fullness"] + 10)
    elif action == 'play':
        reply = {"text": "球球！接住啦喵～", "mood": "playful", "emoji": "🎾"}
    else:
        # 随机抽取一条反应
        reply = random.choice(GREETINGS)

    # 更新亲密度 & 心情
    neko_state["affection"] = min(100, neko_state["affection"] + 1)
    neko_state["mood_level"] = min(100, neko_state["mood_level"] + 2)
    neko_state["fullness"] = max(0, neko_state["fullness"] - 1)

    return jsonify({
        "success": True,
        "reply": reply,
        "state": neko_state,
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route('/api/neko/status', methods=['GET'])
def neko_status():
    """获取猫娘当前状态"""
    return jsonify({
        "success": True,
        "neko": neko_state
    })


@app.route('/api/neko/feed', methods=['POST'])
def feed_neko():
    """投喂接口（可扩展）"""
    neko_state["fullness"] = min(100, neko_state["fullness"] + 15)
    neko_state["affection"] = min(100, neko_state["affection"] + 2)
    return jsonify({
        "success": True,
        "message": "香草猫娘吃得很开心喵～",
        "state": neko_state
    })


if __name__ == '__main__':
    # 开发模式运行，生产环境建议用 gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)