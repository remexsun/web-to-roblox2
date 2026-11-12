import json
import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

# 安全口令：网页必须带上它才能写入。
# 部署时用环境变量 SEND_TOKEN 设置；留空表示不校验（仅适合本地测试）。
SECRET_TOKEN = os.environ.get("SEND_TOKEN", "")


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"message": "还没有收到数据", "updated_at": None}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# 程序启动时读回上次保存的数据（重启不丢）
store = load_data()

HTML = """<!doctype html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>发送数据到 Roblox 游戏</title>
</head>
<body>
  <h2>把数据发到我的 Roblox 游戏</h2>
  <input id="msg" type="text" placeholder="输入要发送的内容" />
  <input id="token" type="password" placeholder="口令（未设置可留空）" />
  <button onclick="send()">发送到游戏</button>
  <p id="status"></p>
  <script>
    async function send() {
      const msg = document.getElementById("msg").value;
      const token = document.getElementById("token").value;
      const r = await fetch("/send", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg, token: token})
      });
      const d = await r.json();
      document.getElementById("status").textContent =
        d.ok ? ("已发送：" + msg) : ("失败：" + (d.error || ""));
    }
  </script>
</body>
</html>"""


@app.route("/")
def index():
    return HTML


@app.route("/send", methods=["POST"])
def send():
    body = request.get_json(silent=True) or {}
    message = body.get("message", "")
    token = body.get("token", "")

    # 校验口令：只有口令正确才允许写入
    if SECRET_TOKEN and token != SECRET_TOKEN:
        return jsonify({"ok": False, "error": "口令错误"}), 403

    store["message"] = message
    store["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_data(store)
    return jsonify({"ok": True})


@app.route("/data")
def data():
    # 游戏只读的接口
    return jsonify(store)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
