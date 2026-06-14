from flask import Flask, render_template_string, request, redirect, session
import datetime

app = Flask(__name__)
app.secret_key = "vangram-secret"

kullanicilar = {
    "ali": {"sifre": "123", "ad": "Ali Ekber Çivi", "bio": "Van'dan kod yazıyorum 🚀", "avatar": "👨‍💻", "takipci": ["ayse"], "takip": ["mehmet"]},
    "ayse": {"sifre": "123", "ad": "Ayşe Kaya", "bio": "Fotoğraf severim 📸", "avatar": "👩", "takipci": ["mehmet"], "takip": ["ali"]},
    "mehmet": {"sifre": "123", "ad": "Mehmet Yılmaz", "bio": "Gezgin 🌍", "avatar": "🧑", "takipci": ["ali"], "takip": ["ayse"]},
}

gonderiler = [
    {"id": 1, "kullanici": "ali", "icerik": "Van Gölü manzarası inanılmaz! 🌊 #van #dogа", "emoji": "🏔️", "zaman": "2 saat önce", "begeni": ["ayse"], "yorumlar": [{"kullanici": "ayse", "yorum": "Çok güzel!"}]},
    {"id": 2, "kullanici": "ayse", "icerik": "Bugün harika bir gün ☀️ #mutlu #istanbul", "emoji": "🌸", "zaman": "4 saat önce", "begeni": ["ali", "mehmet"], "yorumlar": []},
    {"id": 3, "kullanici": "mehmet", "icerik": "Kapadokya'da balon turu! 🎈 #kapadokya #gezi", "emoji": "🎈", "zaman": "1 gün önce", "begeni": ["ali"], "yorumlar": [{"kullanici": "ali", "yorum": "Muhteşem!"}]},
]

mesajlar = [
    {"gonderen": "ayse", "alici": "ali", "icerik": "Merhaba! Nasılsın?", "zaman": "10:30"},
    {"gonderen": "ali", "alici": "ayse", "icerik": "İyiyim, sen?", "zaman": "10:31"},
]

sonId = 3

STYLE = """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, Arial; background: #fafafa; color: #262626; }
.header { background: white; border-bottom: 1px solid #dbdbdb; padding: 12px 0; position: sticky; top: 0; z-index: 100; }
.header-inner { max-width: 975px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }
.logo { font-size: 24px; font-weight: bold; font-style: italic; background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.container { max-width: 975px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 300px; gap: 30px; }
.full-container { max-width: 975px; margin: 30px auto; padding: 0 20px; }
.post { background: white; border: 1px solid #dbdbdb; border-radius: 8px; margin-bottom: 20px; }
.post-header { padding: 12px 16px; display: flex; align-items: center; gap: 10px; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(45deg, #f09433, #bc1888); display: flex; align-items: center; justify-content: center; font-size: 18px; }
.avatar-lg { width: 80px; height: 80px; font-size: 40px; }
.username { font-weight: bold; font-size: 14px; }
.post-image { width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 80px; }
.post-actions { padding: 8px 16px; display: flex; gap: 15px; }
.post-actions button, .post-actions a { background: none; border: none; cursor: pointer; font-size: 22px; padding: 4px; text-decoration: none; }
.post-likes { padding: 0 16px; font-weight: bold; font-size: 14px; }
.post-caption { padding: 6px 16px; font-size: 14px; }
.post-caption span { font-weight: bold; margin-right: 5px; }
.yorumlar { padding: 6px 16px 12px; }
.yorum { font-size: 14px; margin-bottom: 4px; }
.yorum span { font-weight: bold; margin-right: 5px; }
.yorum-form { border-top: 1px solid #dbdbdb; padding: 8px 16px; display: flex; gap: 10px; }
.yorum-form input { flex: 1; border: none; outline: none; font-size: 14px; background: transparent; }
.yorum-form button { background: none; border: none; color: #0095f6; font-weight: bold; cursor: pointer; }
.sidebar { }
.profil-ozet { background: white; border: 1px solid #dbdbdb; border-radius: 8px; padding: 20px; margin-bottom: 20px; text-align: center; }
.istatistik { display: flex; justify-content: space-around; margin-top: 15px; }
.istatistik .sayi { font-weight: bold; font-size: 16px; }
.istatistik .label { font-size: 12px; color: #8e8e8e; }
.oneri-kart { background: white; border: 1px solid #dbdbdb; border-radius: 8px; padding: 15px; }
.oneri-item { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.takip-btn { background: none; border: none; color: #0095f6; font-size: 13px; font-weight: bold; cursor: pointer; }
.stories { display: flex; gap: 15px; overflow-x: auto; padding: 15px; background: white; border: 1px solid #dbdbdb; border-radius: 8px; margin-bottom: 20px; }
.story { text-align: center; cursor: pointer; flex-shrink: 0; }
.story-avatar { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(45deg, #f09433, #bc1888); display: flex; align-items: center; justify-content: center; font-size: 28px; outline: 2px solid #bc1888; outline-offset: 2px; }
.story-name { font-size: 11px; margin-top: 5px; }
input, textarea { width: 100%; padding: 10px; border: 1px solid #dbdbdb; border-radius: 6px; font-size: 14px; margin-top: 5px; }
.btn { background: #0095f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; }
.btn-outline { background: white; color: #0095f6; border: 1px solid #0095f6; padding: 6px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px; }
.btn-outline-red { background: white; color: #ed4956; border: 1px solid #ed4956; padding: 6px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px; }
.login-box { max-width: 400px; margin: 60px auto; padding: 0 20px; }
.login-card { background: white; border: 1px solid #dbdbdb; border-radius: 8px; padding: 40px; text-align: center; margin-bottom: 10px; }
.hashtag { color: #00376b; cursor: pointer; }
.dm-container { display: grid; grid-template-columns: 300px 1fr; height: calc(100vh - 120px); background: white; border: 1px solid #dbdbdb; border-radius: 8px; overflow: hidden; }
.dm-liste { border-right: 1px solid #dbdbdb; overflow-y: auto; }
.dm-item { padding: 15px; display: flex; align-items: center; gap: 10px; cursor: pointer; border-bottom: 1px solid #f0f0f0; }
.dm-item:hover, .dm-item.aktif { background: #fafafa; }
.dm-mesajlar { display: flex; flex-direction: column; }
.dm-header { padding: 15px; border-bottom: 1px solid #dbdbdb; font-weight: bold; }
.mesaj-alani { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; max-height: calc(100vh - 250px); }
.mesaj-balonu { max-width: 60%; padding: 10px 14px; border-radius: 18px; font-size: 14px; }
.mesaj-ben { background: #0095f6; color: white; align-self: flex-end; }
.mesaj-diger { background: #efefef; align-self: flex-start; }
.mesaj-form { padding: 15px; border-top: 1px solid #dbdbdb; display: flex; gap: 10px; }
.mesaj-form input { flex: 1; border: 1px solid #dbdbdb; border-radius: 20px; padding: 8px 16px; margin: 0; }
.kesfet-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3px; }
.kesfet-item { aspect-ratio: 1; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 48px; cursor: pointer; position: relative; }
.kesfet-item:hover .overlay { display: flex; }
.overlay { display: none; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); align-items: center; justify-content: center; color: white; gap: 15px; font-size: 14px; font-weight: bold; }
.profil-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3px; margin-top: 20px; }
.profil-post { aspect-ratio: 1; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 40px; }
.nav-link { text-decoration: none; color: #262626; font-size: 22px; }
.mesaj-zaman { font-size: 11px; color: #8e8e8e; text-align: center; margin: 5px 0; }
</style>
"""

def header(aktif="ana"):
    k = session.get("kullanici", "")
    av = kullanicilar.get(k, {}).get("avatar", "👤")
    okunmamis = sum(1 for m in mesajlar if m["alici"] == k)
    return f"""
    <div class="header">
        <div class="header-inner">
            <a href="/" style="text-decoration:none;"><div class="logo">VanGram</div></a>
            <div style="display:flex;gap:5px;align-items:center;">
                <a href="/" class="nav-link" title="Ana Sayfa">🏠</a>
                <a href="/kesفet" class="nav-link" title="Keşfet">🔍</a>
                <a href="/dm" class="nav-link" title="Mesajlar">💬{'<span style="font-size:11px;color:red;vertical-align:top;">●</span>' if okunmamis > 0 else ''}</a>
                <a href="/profil/{k}" class="nav-link" title="Profil">{av}</a>
                <a href="/cikis" style="font-size:13px;color:#8e8e8e;text-decoration:none;margin-left:5px;">Çıkış</a>
            </div>
        </div>
    </div>"""

def gonderi_html(g, aktif_k):
    k = kullanicilar.get(g["kullanici"], {})
    yorumlar = "".join([f'<div class="yorum"><span>{y["kullanici"]}</span>{y["yorum"]}</div>' for y in g["yorumlar"][-3:]])
    begendim = aktif_k in g["begeni"]
    icerik = g["icerik"]
    # Hashtag renklendirme
    kelimeler = icerik.split()
    icerik_html = " ".join([f'<a href="/hashtag/{k[1:]}" class="hashtag">{k}</a>' if k.startswith("#") else k for k in kelimeler])
    return f"""
    <div class="post">
        <div class="post-header">
            <div class="avatar">{k.get("avatar","👤")}</div>
            <div>
                <a href="/profil/{g["kullanici"]}" style="text-decoration:none;color:#262626;">
                    <div class="username">{g["kullanici"]}</div>
                </a>
                <div style="font-size:12px;color:#8e8e8e;">Van, Türkiye</div>
            </div>
            <div style="margin-left:auto;font-size:12px;color:#8e8e8e;">{g["zaman"]}</div>
        </div>
        <div class="post-image">{g["emoji"]}</div>
        <div class="post-actions">
            <form method="POST" action="/begeni/{g["id"]}" style="display:inline;">
                <button type="submit">{"❤️" if begendim else "🤍"}</button>
            </form>
            <button>💬</button>
            <button>📤</button>
            <button style="margin-left:auto;">🔖</button>
        </div>
        <div class="post-likes">{len(g["begeni"])} beğeni</div>
        <div class="post-caption"><span>{g["kullanici"]}</span>{icerik_html}</div>
        <div class="yorumlar">{yorumlar}</div>
        <div class="yorum-form">
            <form method="POST" action="/yorum/{g["id"]}" style="display:flex;flex:1;gap:10px;">
                <input type="text" name="yorum" placeholder="Yorum ekle...">
                <button type="submit">Paylaş</button>
            </form>
        </div>
    </div>"""

ANA = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>VanGram</title>""" + STYLE + """</head><body>
{{ header | safe }}
<div class="container">
    <div>
        <div class="stories">
            {% for k, v in kullanicilar.items() %}
            <div class="story">
                <a href="/profil/{{ k }}" style="text-decoration:none;">
                    <div class="story-avatar">{{ v.avatar }}</div>
                    <div class="story-name">{{ k }}</div>
                </a>
            </div>
            {% endfor %}
        </div>
        <div class="post" style="padding:15px;margin-bottom:20px;">
            <form method="POST" action="/paylasim">
                <div style="display:flex;gap:10px;align-items:flex-start;">
                    <div class="avatar">{{ avatar }}</div>
                    <div style="flex:1;">
                        <textarea name="icerik" placeholder="Ne düşünüyorsun? #hashtag kullanabilirsin" rows="2" style="resize:none;"></textarea>
                        <div style="display:flex;gap:10px;margin-top:8px;">
                            <input type="text" name="emoji" placeholder="🌸" style="width:60px;margin:0;">
                            <button class="btn" type="submit">Paylaş</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
        {{ gonderiler | safe }}
    </div>
    <div class="sidebar">
        <div class="profil-ozet">
            <div style="font-size:50px;">{{ avatar }}</div>
            <div style="font-weight:bold;margin-top:8px;">{{ kullanici }}</div>
            <div style="font-size:13px;color:#8e8e8e;">{{ ad }}</div>
            <div style="font-size:13px;color:#8e8e8e;margin-top:4px;">{{ bio }}</div>
            <div class="istatistik">
                <div><div class="sayi">{{ gonderi_sayisi }}</div><div class="label">gönderi</div></div>
                <div><div class="sayi">{{ takipci }}</div><div class="label">takipçi</div></div>
                <div><div class="sayi">{{ takip }}</div><div class="label">takip</div></div>
            </div>
        </div>
        <div class="oneri-kart">
            <div style="font-size:13px;color:#8e8e8e;margin-bottom:12px;font-weight:bold;">Önerilen Hesaplar</div>
            {% for k, v in oneriler.items() %}
            <div class="oneri-item">
                <div class="avatar">{{ v.avatar }}</div>
                <div style="flex:1;">
                    <div style="font-size:13px;font-weight:bold;">{{ k }}</div>
                    <div style="font-size:12px;color:#8e8e8e;">{{ v.ad }}</div>
                </div>
                <form method="POST" action="/takip/{{ k }}">
                    <button class="takip-btn">Takip Et</button>
                </form>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
</body></html>"""

PROFIL = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>VanGram</title>""" + STYLE + """</head><body>
{{ header | safe }}
<div class="full-container">
    <div style="display:flex;gap:40px;align-items:flex-start;padding:20px 0;border-bottom:1px solid #dbdbdb;">
        <div style="font-size:80px;">{{ profil.avatar }}</div>
        <div style="flex:1;">
            <div style="display:flex;align-items:center;gap:15px;margin-bottom:15px;">
                <h2>{{ profil_k }}</h2>
                {% if profil_k == kullanici %}
                <button class="btn-outline">Profili Düzenle</button>
                {% elif takip_ediyor %}
                <form method="POST" action="/takipten-cik/{{ profil_k }}">
                    <button class="btn-outline-red">Takibi Bırak</button>
                </form>
                {% else %}
                <form method="POST" action="/takip/{{ profil_k }}">
                    <button class="btn">Takip Et</button>
                </form>
                {% endif %}
                {% if profil_k != kullanici %}
                <a href="/dm/{{ profil_k }}" class="btn-outline">Mesaj Gönder</a>
                {% endif %}
            </div>
            <div style="display:flex;gap:30px;margin-bottom:15px;">
                <span><strong>{{ gonderi_sayisi }}</strong> gönderi</span>
                <span><strong>{{ profil.takipci | length }}</strong> takipçi</span>
                <span><strong>{{ profil.takip | length }}</strong> takip</span>
            </div>
            <div style="font-weight:bold;">{{ profil.ad }}</div>
            <div style="font-size:14px;color:#262626;margin-top:4px;">{{ profil.bio }}</div>
        </div>
    </div>
    <div class="profil-grid">
        {% for g in profil_gonderiler %}
        <div class="profil-post">{{ g.emoji }}</div>
        {% endfor %}
    </div>
</div>
</body></html>"""

DM = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>VanGram DM</title>""" + STYLE + """</head><body>
{{ header | safe }}
<div class="full-container">
    <div class="dm-container">
        <div class="dm-liste">
            <div style="padding:15px;font-weight:bold;border-bottom:1px solid #dbdbdb;">Mesajlar</div>
            {% for k, v in kullanicilar.items() %}
            {% if k != kullanici %}
            <a href="/dm/{{ k }}" style="text-decoration:none;color:#262626;">
                <div class="dm-item {{ 'aktif' if aktif_dm == k else '' }}">
                    <div class="avatar">{{ v.avatar }}</div>
                    <div>
                        <div style="font-weight:bold;font-size:14px;">{{ k }}</div>
                        <div style="font-size:12px;color:#8e8e8e;">{{ v.ad }}</div>
                    </div>
                </div>
            </a>
            {% endif %}
            {% endfor %}
        </div>
        <div class="dm-mesajlar">
            {% if aktif_dm %}
            <div class="dm-header">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div class="avatar">{{ kullanicilar[aktif_dm].avatar }}</div>
                    <div>
                        <div>{{ aktif_dm }}</div>
                        <div style="font-size:12px;color:#8e8e8e;">{{ kullanicilar[aktif_dm].ad }}</div>
                    </div>
                </div>
            </div>
            <div class="mesaj-alani">
                {% for m in konusma %}
                <div class="mesaj-balonu {{ 'mesaj-ben' if m.gonderen == kullanici else 'mesaj-diger' }}">
                    {{ m.icerik }}
                    <div style="font-size:10px;opacity:0.7;margin-top:2px;">{{ m.zaman }}</div>
                </div>
                {% endfor %}
            </div>
            <div class="mesaj-form">
                <form method="POST" action="/dm/{{ aktif_dm }}/gonder" style="display:flex;flex:1;gap:10px;">
                    <input type="text" name="icerik" placeholder="Mesaj yaz..." required>
                    <button class="btn" type="submit">Gönder</button>
                </form>
            </div>
            {% else %}
            <div style="display:flex;align-items:center;justify-content:center;flex:1;color:#8e8e8e;">
                Bir konuşma seç
            </div>
            {% endif %}
        </div>
    </div>
</div>
</body></html>"""

KESФET = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>VanGram Keşfet</title>""" + STYLE + """</head><body>
{{ header | safe }}
<div class="full-container">
    <div style="margin-bottom:20px;">
        <form method="GET" action="/ara">
            <div style="display:flex;gap:10px;">
                <input type="text" name="q" placeholder="Kullanıcı veya #hashtag ara..." value="{{ q }}" style="max-width:400px;">
                <button class="btn" type="submit">Ara</button>
            </div>
        </form>
    </div>
    {% if arama_sonuclari %}
    <div style="margin-bottom:20px;">
        <h3 style="margin-bottom:15px;">Arama Sonuçları</h3>
        {% for s in arama_sonuclari %}
        <div style="background:white;border:1px solid #dbdbdb;border-radius:8px;padding:15px;margin-bottom:10px;display:flex;align-items:center;gap:15px;">
            <div class="avatar">{{ s.avatar }}</div>
            <div style="flex:1;">
                <a href="/profil/{{ s.kullanici }}" style="font-weight:bold;text-decoration:none;color:#262626;">{{ s.kullanici }}</a>
                <div style="font-size:13px;color:#8e8e8e;">{{ s.ad }}</div>
            </div>
            <form method="POST" action="/takip/{{ s.kullanici }}">
                <button class="btn-outline">Takip Et</button>
            </form>
        </div>
        {% endfor %}
    </div>
    {% endif %}
    {% if hashtag_gonderiler %}
    <h3 style="margin-bottom:15px;">#{{ aktif_hashtag }}</h3>
    {% endif %}
    <h3 style="margin-bottom:15px;">{{ 'Keşfet' if not hashtag_gonderiler else '' }}</h3>
    <div class="kesfet-grid">
        {% for g in kesfet_gonderiler %}
        <div class="kesfet-item">
            {{ g.emoji }}
            <div class="overlay">
                <span>❤️ {{ g.begeni | length }}</span>
                <span>💬 {{ g.yorumlar | length }}</span>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
</body></html>"""

LOGIN = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>VanGram</title>""" + STYLE + """</head><body>
<div class="login-box">
    <div class="login-card">
        <div style="font-size:40px;">📸</div>
        <div class="logo" style="font-size:36px;margin:15px 0 25px;">VanGram</div>
        <form method="POST" action="/giris">
            <input type="text" name="kullanici" placeholder="Kullanıcı adı" required>
            <input type="password" name="sifre" placeholder="Şifre" style="margin-top:10px;" required>
            <button class="btn" style="width:100%;margin-top:15px;" type="submit">Giriş Yap</button>
        </form>
        {% if hata %}<p style="color:red;margin-top:10px;font-size:13px;">{{ hata }}</p>{% endif %}
        <div style="margin-top:15px;font-size:13px;color:#8e8e8e;">ali/123 | ayse/123 | mehmet/123</div>
    </div>
    <div style="background:white;border:1px solid #dbdbdb;border-radius:8px;padding:20px;text-align:center;">
        <p style="font-size:14px;">Hesabın yok mu? <a href="/kayit" style="color:#0095f6;font-weight:bold;text-decoration:none;">Kaydol</a></p>
    </div>
</div>
</body></html>"""

KAYIT = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>VanGram</title>""" + STYLE + """</head><body>
<div class="login-box">
    <div class="login-card">
        <div class="logo" style="font-size:36px;margin-bottom:25px;">VanGram</div>
        <form method="POST" action="/kayit">
            <input type="text" name="kullanici" placeholder="Kullanıcı adı" required>
            <input type="text" name="ad" placeholder="Ad Soyad" style="margin-top:10px;" required>
            <input type="text" name="bio" placeholder="Bio" style="margin-top:10px;">
            <input type="text" name="avatar" placeholder="Avatar emoji 😊" style="margin-top:10px;" maxlength="2">
            <input type="password" name="sifre" placeholder="Şifre" style="margin-top:10px;" required>
            <button class="btn" style="width:100%;margin-top:15px;" type="submit">Kaydol</button>
        </form>
        {% if hata %}<p style="color:red;margin-top:10px;font-size:13px;">{{ hata }}</p>{% endif %}
    </div>
    <div style="background:white;border:1px solid #dbdbdb;border-radius:8px;padding:20px;text-align:center;">
        <p style="font-size:14px;">Hesabın var mı? <a href="/" style="color:#0095f6;font-weight:bold;text-decoration:none;">Giriş Yap</a></p>
    </div>
</div>
</body></html>"""

@app.route("/")
def anasayfa():
    if "kullanici" not in session:
        return render_template_string(LOGIN, hata=None)
    k = session["kullanici"]
    kb = kullanicilar[k]
    gonderiler_sirali = sorted(gonderiler, key=lambda x: x["id"], reverse=True)
    g_html = "".join([gonderi_html(g, k) for g in gonderiler_sirali])
    oneriler = {u: v for u, v in kullanicilar.items() if u != k and u not in kb["takip"]}
    return render_template_string(ANA,
        header=header(), kullanici=k, avatar=kb["avatar"],
        ad=kb["ad"], bio=kb["bio"],
        takipci=len(kb["takipci"]), takip=len(kb["takip"]),
        gonderi_sayisi=sum(1 for g in gonderiler if g["kullanici"] == k),
        gonderiler=g_html, kullanicilar=kullanicilar, oneriler=oneriler)

@app.route("/giris", methods=["POST"])
def giris():
    k = request.form["kullanici"]
    s = request.form["sifre"]
    if k in kullanicilar and kullanicilar[k]["sifre"] == s:
        session["kullanici"] = k
        return redirect("/")
    return render_template_string(LOGIN, hata="Hatalı kullanıcı adı veya şifre!")

@app.route("/kayit", methods=["GET", "POST"])
def kayit():
    if request.method == "GET":
        return render_template_string(KAYIT, hata=None)
    k = request.form["kullanici"]
    if k in kullanicilar:
        return render_template_string(KAYIT, hata="Bu kullanıcı adı alınmış!")
    kullanicilar[k] = {"sifre": request.form["sifre"], "ad": request.form["ad"],
        "bio": request.form.get("bio",""), "avatar": request.form.get("avatar","😊"),
        "takipci": [], "takip": []}
    session["kullanici"] = k
    return redirect("/")

@app.route("/paylasim", methods=["POST"])
def paylasim():
    global sonId
    if "kullanici" not in session: return redirect("/")
    sonId += 1
    gonderiler.append({"id": sonId, "kullanici": session["kullanici"],
        "icerik": request.form["icerik"], "emoji": request.form.get("emoji","📸"),
        "zaman": "Az önce", "begeni": [], "yorumlar": []})
    return redirect("/")

@app.route("/begeni/<int:id>", methods=["POST"])
def begeni(id):
    if "kullanici" not in session: return redirect("/")
    k = session["kullanici"]
    for g in gonderiler:
        if g["id"] == id:
            if k in g["begeni"]: g["begeni"].remove(k)
            else: g["begeni"].append(k)
    return redirect("/")

@app.route("/yorum/<int:id>", methods=["POST"])
def yorum(id):
    if "kullanici" not in session: return redirect("/")
    for g in gonderiler:
        if g["id"] == id:
            g["yorumlar"].append({"kullanici": session["kullanici"], "yorum": request.form["yorum"]})
    return redirect("/")

@app.route("/takip/<kullanici>", methods=["POST"])
def takip(kullanici):
    if "kullanici" not in session: return redirect("/")
    k = session["kullanici"]
    if kullanici in kullanicilar:
        if kullanici not in kullanicilar[k]["takip"]:
            kullanicilar[k]["takip"].append(kullanici)
        if k not in kullanicilar[kullanici]["takipci"]:
            kullanicilar[kullanici]["takipci"].append(k)
    return redirect(request.referrer or "/")

@app.route("/takipten-cik/<kullanici>", methods=["POST"])
def takipten_cik(kullanici):
    if "kullanici" not in session: return redirect("/")
    k = session["kullanici"]
    if kullanici in kullanicilar[k]["takip"]:
        kullanicilar[k]["takip"].remove(kullanici)
    if k in kullanicilar[kullanici]["takipci"]:
        kullanicilar[kullanici]["takipci"].remove(k)
    return redirect(request.referrer or "/")

@app.route("/profil/<kullanici_adi>")
def profil(kullanici_adi):
    if "kullanici" not in session: return redirect("/")
    if kullanici_adi not in kullanicilar: return redirect("/")
    k = session["kullanici"]
    p = kullanicilar[kullanici_adi]
    profil_gonderiler = [g for g in gonderiler if g["kullanici"] == kullanici_adi]
    takip_ediyor = kullanici_adi in kullanicilar[k]["takip"]
    return render_template_string(PROFIL,
        header=header(), kullanici=k, profil_k=kullanici_adi,
        profil=p, gonderi_sayisi=len(profil_gonderiler),
        profil_gonderiler=profil_gonderiler, takip_ediyor=takip_ediyor,
        kullanicilar=kullanicilar)

@app.route("/dm")
@app.route("/dm/<diger>")
def dm(diger=None):
    if "kullanici" not in session: return redirect("/")
    k = session["kullanici"]
    konusma = []
    if diger:
        konusma = [m for m in mesajlar if
            (m["gonderen"] == k and m["alici"] == diger) or
            (m["gonderen"] == diger and m["alici"] == k)]
    return render_template_string(DM,
        header=header(), kullanici=k, aktif_dm=diger,
        konusma=konusma, kullanicilar=kullanicilar)

@app.route("/dm/<diger>/gonder", methods=["POST"])
def dm_gonder(diger):
    if "kullanici" not in session: return redirect("/")
    k = session["kullanici"]
    mesajlar.append({"gonderen": k, "alici": diger,
        "icerik": request.form["icerik"],
        "zaman": datetime.datetime.now().strftime("%H:%M")})
    return redirect(f"/dm/{diger}")

@app.route("/kesفet")
def kesfet():
    if "kullanici" not in session: return redirect("/")
    k = session["kullanici"]
    return render_template_string(KESФЕТ,
        header=header(), kullanici=k, q="",
        kesfet_gonderiler=sorted(gonderiler, key=lambda x: len(x["begeni"]), reverse=True),
        arama_sonuclari=[], hashtag_gonderiler=[], aktif_hashtag="",
        kullanicilar=kullanicilar)

@app.route("/ara")
def ara():
    if "kullanici" not in session: return redirect("/")
    k = session["kullanici"]
    q = request.args.get("q", "").lower()
    sonuclar = []
    if q:
        for u, v in kullanicilar.items():
            if q in u.lower() or q in v["ad"].lower():
                sonuclar.append({"kullanici": u, "ad": v["ad"], "avatar": v["avatar"]})
    return render_template_string(KESФЕТ,
        header=header(), kullanici=k, q=q,
        kesfet_gonderiler=gonderiler,
        arama_sonuclari=sonuclar,
        hashtag_gonderiler=[], aktif_hashtag="",
        kullanicilar=kullanicilar)

@app.route("/hashtag/<tag>")
def hashtag(tag):
    if "kullanici" not in session: return redirect("/")
    k = session["kullanici"]
    tag_gonderiler = [g for g in gonderiler if f"#{tag}" in g["icerik"]]
    return render_template_string(KESФЕТ,
        header=header(), kullanici=k, q="",
        kesfet_gonderiler=tag_gonderiler,
        arama_sonuclari=[], hashtag_gonderiler=tag_gonderiler,
        aktif_hashtag=tag, kullanicilar=kullanicilar)

@app.route("/cikis")
def cikis():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)