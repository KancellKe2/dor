# api/index.py
from flask import Flask, request, jsonify
import os
import traceback

# Jika Anda mengekspor fungsi dari main.py, import di sini.
# from main import run_task

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """
    <h1>DOR - Web wrapper</h1>
    <p>Endpoint:</p>
    <ul>
      <li>GET / -> this page</li>
      <li>POST /run -> jalankan fungsi utama (JSON body)</li>
    </ul>
    """

@app.route("/run", methods=["POST"])
def run_action():
    try:
        data = request.json or {}
        # contoh: panggil fungsi yang anda expose dari main.py
        # result = run_task(data)
        # sementara ini kita kembalikan contoh respons
        result = {
            "status": "ok",
            "note": "Ganti bagian ini untuk memanggil fungsi dari main.py",
            "received": data
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "error": str(e), "trace": traceback.format_exc()}), 500

# Untuk Vercel: expose Flask `app` variable
# Vercel's Python runtime will use `app` as WSGI/ASGI entrypoint.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
