import os
from flask import Flask, request, Response
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext
)
from botbuilder.schema import Activity

app = Flask(__name__)

# Hent App-ID og passord
APP_ID = os.environ.get("MicrosoftAppId", "")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

print(f"🔐 Starter med App ID: {APP_ID[:6]}... (kortet for sikkerhet)")

# Forsøk å opprette adapter
try:
    adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
    adapter = BotFrameworkAdapter(adapter_settings)
except Exception as e:
    print(f"❌ Feil under opprettelse av BotFrameworkAdapter: {str(e)}")
    adapter = None  # Så vi unngår at appen krasjer

@app.route("/", methods=["GET"])
def root():
    return "Bot API med adapter-sjekk OK"

@app.route("/api/messages", methods=["POST"])
def messages():
    if adapter is None:
        print("⚠️ Adapter ikke initialisert – svarer med 503")
        return Response("Adapter-feil", status=503)

    print("🔔 POST /api/messages mottatt")

    if "application/json" in request.headers.get("Content-Type", ""):
        body = request.json
        print("📥 Innhold mottatt:", body)
    else:
        print("⚠️  Feil Content-Type:", request.headers.get("Content-Type"))
        return Response(status=415)

    try:
        activity = Activity().deserialize(body)
        print(f"🧾 Type: {activity.type}, 💬 Tekst: {getattr(activity, 'text', '')}")

        async def aux_func(turn_context: TurnContext):
            await turn_context.send_activity("Hei! Dette er et testsvar fra Flask-serveren.")

        task = adapter.process_activity(activity, "", aux_func)
        return Response(status=202)
    except Exception as e:
        print("🔥 Feil i behandling:", str(e))
        return Response("Intern feil", status=500)
