from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity, ActivityTypes
import asyncio
import logging
import os
import json

# Konfigurer FastAPI og logging
app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Hent AppId og Passord fra miljøvariabler
APP_ID = os.environ.get("MicrosoftAppId", "")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

# Konfigurer adapter
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Echo-handler
async def handle_turn(context: TurnContext):
    if context.activity.type == ActivityTypes.message:
        user_text = context.activity.text.strip()
        logging.info(f"📨 Melding mottatt: {user_text}")
        await context.send_activity(Activity(type=ActivityTypes.message, text=f"Du sa: {user_text}"))
    else:
        logging.info(f"⚠️ Ikke-støttet aktivitetstype: {context.activity.type}")

# Endepunkt for å motta meldinger fra Bot Framework
@app.post("/api/messages")
async def messages(request: Request):
    try:
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8")
        activity = Activity().deserialize(json.loads(body_str))

        auth_header = request.headers.get("Authorization", "")
        await adapter.process_activity(activity, auth_header, handle_turn)
        return JSONResponse(status_code=202, content={})

    except Exception as e:
        logging.error(f"🚨 Feil under behandling av melding: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# Helse-endepunkt for å teste deploy
@app.get("/")
def root():
    return {"message": "Bot API minimal fungerer!"}
