from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

app = Flask(__name__)

adapter_settings = BotFrameworkAdapterSettings("", "")
adapter = BotFrameworkAdapter(adapter_settings)

async def handle_message(context: TurnContext):
    await context.send_activity("Hei! Dette er et testsvar fra Flask-serveren.")

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)

    async def aux_func(turn_context):
        await handle_message(turn_context)

    task = adapter.process_activity(activity, "", aux_func)
    return Response(status=202)
