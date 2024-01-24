import os
class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
    CHANNEL_ID = os.environ.get("CHANNEL_ID")
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    ADMIN_ID = os.environ.get("ADMIN_ID")
