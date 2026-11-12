把网页数据传进 Roblox 游戏（轮询方案）
==========================================

这个文件夹包含一套完整的示例：
1. app.py          —— 网页 + 后端接口（Python Flask）
2. requirements.txt —— 依赖
3. roblox/roboserver.lua      —— 放进 ServerScriptService 的 Script
4. roblox/client_display.lua  —— 放进 StarterPlayer/StarterPlayerScripts 的 LocalScript

工作流程
--------
你的网页(按钮) -> POST /send -> 服务器保存到 data.json
Roblox 服务器脚本 -> 每 3 秒 GET /data -> 收到消息 -> 通过 RemoteEvent 广播
所有玩家的 LocalScript -> 在屏幕顶部显示消息

第一步：本地测试网页（可选）
----------------------------
1. 安装 Python 3
2. 在这个文件夹里运行：
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
3. 浏览器打开 http://localhost:5000
   点"发送到游戏"，再打开 http://localhost:5000/data 能看到刚发的内容，说明后端正常。

注意：Roblox 访问不了 localhost，所以本地运行只能验证网页和后端，
真正连游戏必须部署到公网（见下一步）。

第二步：部署到公网（必须）
--------------------------
推荐免费平台：Render.com / Glitch.com / Railway / Replit。
把 app.py 和 requirements.txt 传上去，部署后你会得到一个类似
https://你的名字.onrender.com 的 HTTPS 地址。

第三步：接入 Roblox Studio
--------------------------
1. 开启 HTTP 请求：
   命令栏执行 game:GetService("HttpService").HttpEnabled = true
   （发布后的游戏在 游戏设置 -> 安全 里勾选 Allow HTTP Requests）
2. 新建 Script，粘贴 roblox/roboserver.lua 的内容，
   把 URL 改成你的公网地址（记得末尾是 /data）。
3. 新建 LocalScript，粘贴 roblox/client_display.lua 的内容，
   放进 StarterPlayer -> StarterPlayerScripts。
4. 点 Play 运行，然后在你的网页输入内容点发送，游戏里 3 秒内会显示。

可选：加口令
------------
部署时设置环境变量 SEND_TOKEN=你的口令，
网页上就必须输入相同口令才能发送，防止别人乱发。
