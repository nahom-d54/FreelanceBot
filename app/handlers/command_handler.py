from telegram import Update
from .messages import Messages, ErrorMessages
#from bot import CC
from ..db.models import CC
from ..helpers.jobPoster import jobPoster

async def start(update: Update, context:CC ):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(f"Hello { update.message.chat.first_name }\n{Messages.START_MESSAGE}")
    chat_id = update.effective_user.id
    bot = context.bot
    user = context.User
    start_parameter = context.args[0] if len(context.args) > 0 else None
    #print(start_parameter)
    
    await user.insertUser(update)
    this = await user.getUser(chat_id)
    if not this.get("user_type"):
        await bot.send_message(
            chat_id=update.message.chat_id,
            text=Messages.START_MESSAGE_QUESTION,
            reply_markup=Messages.START_MESSAGE_QUESTION_BUTTON
        )
    
    #await jobPoster(update, context, "5f8c6e1e2f7a3e1c4d2b1a0f")
    

"""
async def create_job(update, context):
    await update.message.reply_text("Create A Job Listing ?")
    return createJob.start_step
"""

# async def create_Company(update: Update , context: CC):
    


    # get job fro db

    # then continue