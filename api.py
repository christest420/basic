import os
from flask import Flask, request, Response
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext
)
from botbuilder.schema import Activity

app = Flask(__name__)

# Hent App ID og Secret fra miljøvariabler (fra Azure)
APP_ID = os.environ.get("MicrosoftAppId", "")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Enkel GET-endepunkt for testing
@app.route("/", methods=["GET"])
def root():
    print("📡 GET / - test-endepunkt kalt")
    return "Bot API kjører OK!"

# Bot Framework-endepunkt
@app.route("/api/messages", methods=["POST"])
def messages():
    print("🔔 POST /api/messages mottatt")

    if "application/json" in request.headers.get("Content-Type", ""):
        body = request.json
        print("📥 Innhold mottatt:", body)
    else:
        print("⚠️  Feil Content-Type:", request.headers.get("Content-Type"))
        return Response(status=415)

    try:
        activity = Activity().deserialize(body)
        print(f"🧾 Deserialisert aktivitetstype: {activity.type}")
        print(f"💬 Meldingstekst: {getattr(activity, 'text', '')}")

        async def aux_func(turn_context: TurnContext):
            print("📤 Sender svar tilbake til bruker...")
            await turn_context.send_activity("Hei! Dette er et testsvar fra Flask-serveren.")

        task = adapter.process_activity(activity, "", aux_func)
        return Response(status=202)
    except Exception as e:
        print("🔥 Feil under behandling:", str(e))
        return Response(status=500)
