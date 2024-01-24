from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from ..handlers.messages import Messages
from ..config import Config
async def jobPoster(update: Update , context, job_id):
    # test channal id -1001813665540
    data = context.user_data['this_job']
    bot_username = context.bot.username
    channel_id = Config.CHANNEL_ID

    msg = Messages.JOB_ALL.format(
            title=data[Messages.JOB_TITLE],
            salary=data[Messages.JOB_SALARY],
            desc=data[Messages.JOB_DESCRIPTION],
            res=data[Messages.JOB_RESPONSIBILITIES],
            company=data[Messages.JOB_COMPANY]
            )
    keyboard = [[InlineKeyboardButton(text="Apply",url=f"tg://resolve?domain={bot_username}&start={job_id}")]]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(text=msg, reply_markup = markup, chat_id= channel_id)