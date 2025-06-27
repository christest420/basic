from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot API minimal fungerer!", 200

@app.route("/api/messages", methods=["POST"])
def messages():
    print("⏺️ Inngående forespørsel mottatt på /api/messages")
    return Response(status=202)
