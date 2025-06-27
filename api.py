import os
from flask import Flask, request, Response
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext
)
from botbuilder.schema import Activity

app = Flask(__name__)

# Hent App ID og Password fra miljøvariabler (satt i Azure)
APP_ID = os.environ.get("MicrosoftAppId", "")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# GET-endepunkt for enkel testing
@app.route("/", methods=["GET"])
def root():
    return "Bot API kjører OK!"

# POST-endepunkt for Bot Framework
@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)

    async def aux_func(turn_context: TurnContext):
        await turn_context.send_activity("Hei! Dette er et testsvar fra Flask-serveren.")

    task = adapter.process_activity(activity, "", aux_func)
    return Response(status=202)
