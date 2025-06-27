from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity, ActivityTypes
import asyncio
import logging
import os

app = FastAPI()

# Konfigurer logging
logging.basicConfig(level=logging.INFO)

# Miljøvariabler for Bot Framework
APP_ID = os.environ.get("MicrosoftAppId", "")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

# Sett opp adapter med App ID og passord
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Echo handler – svarer med det samme som ble sendt inn
async def handle_turn(context: TurnContext):
    if context.activity.type == ActivityTypes.message:
        user_text = context.activity.text
        logging.info(f"🔁 Inngående melding: {user_text}")
        await context.send_activity(Activity(type=ActivityTypes.message, text=f"Du sa: {user_text}"))
    else:
        logging.info(f"⚠️ Annen aktivitetstype: {context.activity.type}")

# Endepunkt for /api/messages
@app.post("/api/messages")
async def messages(request: Request):
    body = await request.body()
    activity = Activity().deserialize(body.decode("utf-8"))

    auth_header = request.headers.get("Authorization", "")

    try:
        await adapter.process_activity(activity, auth_header, handle_turn)
        return JSONResponse(status_code=202, content={})
    except Exception as e:
        logging.error(f"🚨 Feil under prosessering av melding: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# Valgfritt: Endepunkt for å sjekke at API-et er oppe
@app.get("/")
def root():
    return {"message": "Bot API minimal fungerer!"}
