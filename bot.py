from contextlib import asynccontextmanager
from http import HTTPStatus
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, filters
from fastapi import FastAPI, Request, Response
import os
import uvicorn
from app.handlers.command_handler import *
from app.handlers.callback_handler import *
from app.handlers.message_handler import *
from app.handlers.conversations.createJob import conv_handler
from app.handlers.conversations.createCompany import  create_company_conv_handler
from app.handlers.conversations.apply_for_job import  apply_handler
from app.db.models import CC
from telegram.warnings import PTBUserWarning
from warnings import filterwarnings
from app.config import Config

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


token = Config.BOT_TOKEN
context_types = ContextTypes(context=CC)

ptb = (
        Application.builder()
        .updater(None)
        .token(token)
        .context_types(context_types = context_types)
        .read_timeout(7)
        .get_updates_read_timeout(43)
        .build()
    )
@asynccontextmanager
async def lifespan(_):
    ptb.add_handler(apply_handler,0)
    ptb.add_handler(CommandHandler("start", start, filters=filters.Regex(r'^(?!/start [0-9a-fA-F]{24}$).+$')), 1)
    ptb.add_handler(conv_handler)
    ptb.add_handler(create_company_conv_handler)
    ptb.add_handler(CallbackQueryHandler(callback)) #, pattern= r'^(?!conv).*'

    #updater.bot_data['collection'] = connection['MarosetClone']
    

    await ptb.bot.setWebhook(url=Config.WEBHOOK_URL)
    #secret_token=os.environ.get("SECRET_TOKEN")) # replace <your-webhook-url>
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()

app = FastAPI(lifespan=lifespan)
    
@app.post("/")
async def process_update(request: Request):
    # protection
    #headers = request.headers
    #secret_token = headers.get("X-Telegram-Bot-Api-Secret-Token")
    #if secret_token != os.environ.get("SECRET_TOKEN"):
        #return Response(status_code=HTTPStatus.UNAUTHORIZED)
    #protection end
    try:
        req = await request.json()
        update = Update.de_json(req, ptb.bot)
        await ptb.process_update(update)
        return Response(status_code=HTTPStatus.OK)
    except Exception as e:
        pass


if __name__ == '__main__':
    uvicorn.run("bot:app", host="0.0.0.0", port=8000, reload= True)