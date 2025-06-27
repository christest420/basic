from flask import Flask, request, Response
import sys

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    print("✅ GET / ble kalt – Bot API kjører OK", file=sys.stderr)
    return "Bot API minimal fungerer!", 200

@app.route("/api/messages", methods=["POST"])
def messages():
    print("📩 Inngående POST til /api/messages", file=sys.stderr)
    print(f"Headers: {dict(request.headers)}", file=sys.stderr)
    
    try:
        json_data = request.get_json(force=True)
        print(f"Body:\n{json_data}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Klarte ikke lese JSON-body: {e}", file=sys.stderr)
        return Response(status=400)
    
    return Response(status=202)
