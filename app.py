from flask import Flask, render_template, request, jsonify, session
import uuid
from chat import get_response
from database import get_db_connection
import pymysql

app = Flask(__name__)
app.secret_key = "d60ed56c-0cdf-4a2d-a629-581283660b5d"

print("Flask app created!")

def save_user(user_id, name, phone=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, name, phone) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, phone=%s",
                   (user_id, name, phone, name, phone))
    conn.commit()
    cursor.close()
    conn.close()

def save_chat(user_id, message, response):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)",
                   (user_id, message, response))
    conn.commit()
    cursor.close()
    conn.close()

def save_user_activity(user_id, activity):
    """Menyimpan aktivitas user ke dalam tabel user_activity"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_activity (user_id, activity, timestamp) VALUES (%s, %s, NOW())",
                   (user_id, activity))
    conn.commit()
    cursor.close()
    conn.close()

@app.get("/")
def index_get():
    session.clear()
    return render_template("base.html", request=request)

@app.post("/predict")
def predict():
    text = request.get_json().get("message")

    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
        session["stage"] = "ASK_NAME"
        return jsonify({"answer": "Halo! Sebelum kita mulai, siapa namamu?"})

    user_id = session["user_id"]
    stage = session["stage"]

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT name, phone FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if stage == "ASK_NAME":
        save_user(user_id, text)
        session["stage"] = "ASK_PHONE"
        session["name"] = text
        return jsonify({"answer": f"Terima kasih {text}! Sekarang, bolehkah aku tahu nomor WhatsApp kamu?"})

    if stage == "ASK_PHONE":
        save_user(user_id, user["name"], text)
        session["stage"] = "CHAT"
        response = {
            "answer": "Berikut adalah beberapa FAQ yang mungkin membantu:",
            "faq_buttons": [
                {"text": "Bagaimana cara mengajukan pengajuan pendanaan?", "value": "Bagaimana cara mengajukan pengajuan pendanaan?"},
                {"text": "Bagaimana cara memberikan pendanaan?", "value": "Bagaimana cara memberikan pendanaan?"},
                {"text": "Progress pengajuan pendanaan sudah sampai mana?", "value": "Progress pengajuan pendanaan sudah sampai mana?"},
                {"text": "Apa saja produk/layanan yang tersedia?", "value": "Apa saja produk/layanan yang tersedia?"},
                {"text": "Berapa besar margin atau bunga pendanaan?", "value": "Berapa besar margin/bunga pendanaan?"},
                {"text": "Berapa lama tenor/waktu pendanaan?", "value": "Berapa lama tenor/waktu pendanaan?"},
                {"text": "Bagaimana cara pembayarannya?", "value": "Bagaimana cara pembayarannya?"},
                {"text": "Apa syarat pengajuan pendanaan?", "value": "Apa syarat pengajuan pendanaan?"},
                {"text": "Apa saja dokumen yang harus dilengkapi saat pengajuan pendanaan?", "value": "Apa saja dokumen yang harus dilengkapi saat pengajuan pendanaan?"},
                {"text": "Lain-lain", "value": "Lain-lain"},
                {"text": "Mengalami kendala", "value": "Mengalami kendala"},
                {"text": "Bagaimana cara menghubungi CS?", "value": "Bagaimana cara menghubungi CS?"}
            ]
        }
        return jsonify(response)

    response = get_response(text, stage)

    # Simpan aktivitas user jika memilih FAQ
    if text in ["Bagaimana cara mengajukan pengajuan pendanaan?", "Bagaimana cara memberikan pendanaan?", "Progress pengajuan pendanaan sudah sampai mana?", 
                "Apa saja produk/layanan yang tersedia?", "Berapa besar margin atau bunga pendanaan?", "Berapa lama tenor/waktu pendanaan?", "Bagaimana cara pembayarannya?", "Apa syarat pengajuan pendanaan?", "Apa saja dokumen yang harus dilengkapi saat pengajuan pendanaan?", "Lain-lain", "Mengalami kendala", "Bagaimana cara menghubungi CS?"]:
        save_user_activity(user_id, f"Klik FAQ: {text}")

    save_chat(user_id, text, response if isinstance(response, str) else response["answer"])

    return jsonify(response)

@app.post("/log_activity")
def log_activity():
    """Menyimpan aktivitas user saat mengklik link WhatsApp/email"""
    data = request.get_json()
    activity = data.get("activity")

    if "user_id" in session:
        user_id = session["user_id"]
        save_user_activity(user_id, activity)
        return jsonify({"status": "success", "message": "Activity logged"}), 200
    else:
        return jsonify({"status": "error", "message": "User ID not found"}), 400

if __name__ == "__main__":
    print("Running Flask...")
    app.run(debug=True)
