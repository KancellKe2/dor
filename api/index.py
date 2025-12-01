# api/index.py
from flask import Flask, request, jsonify
import os, traceback

# enable CORS
from flask_cors import CORS

# import run_task dari main.py
try:
    from main import run_task
except Exception as e:
    # fallback: import gagal — beri pesan yang jelas di logs
    def run_task(params):
        return {"status": "error", "note": f"Import main.run_task gagal: {str(e)}"}

app = Flask(__name__)
CORS(app)  # izinkan cross-origin (preflight OPTIONS sudah ditangani)

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
        data = request.get_json(force=False, silent=True) or {}
        # panggil fungsi utama yang diekspor dari main.py
        result = run_task(data)
        # pastikan JSON-serializable — jika bukan, bungkus ke str
        try:
            return jsonify({"status": "ok", "result": result})
        except TypeError:
            return jsonify({"status": "ok", "result": str(result)})
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
