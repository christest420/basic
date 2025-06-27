from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

app = Flask(__name__)

# Konfigurer adapter
adapter_settings = BotFrameworkAdapterSettings("", "")
adapter = BotFrameworkAdapter(adapter_settings)

# Standard GET-endepunkt for enkel testing i nettleser
@app.route("/", methods=["GET"])
def root():
    return "Bot API kjører OK!"

# Bot-endepunkt for meldinger
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
