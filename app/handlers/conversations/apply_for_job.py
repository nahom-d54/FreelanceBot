from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
                          ConversationHandler,
                          CommandHandler, 
                          MessageHandler,
                          CallbackQueryHandler,
                          filters)
from ..messages import Messages,ErrorMessages
from ...db.models import CC



I,II,III,IV,V = range(5)

async def apply_for_job(update: Update, context: CC):
    start_parameter = context.args[0] if len(context.args) > 0 else None
    chat_id = update.effective_user.id
    # send job details then 
    # this 

    # then this ->  yes or no option -> then this -> After reviewing your application, the job owner will contact you.
    get_user = await context.User.getUser(chat_id)
    if get_user.get("user_type") != "Employee":
        await update.message.reply_text(ErrorMessages.EMPLOYER_APPLY)
        return ConversationHandler.END
    data = await context.Job.findJobByJobId(start_parameter)

    msg = Messages.JOB_ALL.format(
            title=data[Messages.JOB_TITLE],
            salary=data[Messages.JOB_SALARY],
            desc=data[Messages.JOB_DESCRIPTION],
            res=data[Messages.JOB_RESPONSIBILITIES],
            company=data[Messages.JOB_COMPANY]
            )
    context.user_data['msg'] = msg

    if not data:
        await update.message.reply_text("No job found with id")
        return ConversationHandler.END
    
    context.user_data['job'] = data
    await update.message.reply_text(msg)
    await update.message.reply_text(Messages.APPLY_FOR_JOB)

    return I

async def step_two(update: Update, context: CC):
    context.user_data['application_letter'] = update.message.text
    keyboard = [
        #['Yes', 'No']
        [InlineKeyboardButton('✅Yes', callback_data='conv:Yes'), InlineKeyboardButton('❌No', callback_data='conv:No')]
    ]
    #markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(Messages.APPLY_STEP_TWO, reply_markup=markup, reply_to_message_id=update.message.message_id)

    return II


async def step_three(update: Update, context: CC):
    query = update.callback_query
    chat_id = update.effective_user.id
    username = update.effective_user.username
    data = query.data.split(':',1)[1]

    if data == 'Yes':
        # Send appplication to employer and save applied to job to db
        await query.message.reply_text(Messages.APPLY_FINAL)
        await query.answer("Applied Successfully", True)
        job = context.user_data['job']
        await context.bot.send_message(text="Application For \n\n" + context.user_data['msg'], chat_id=job['user'])

        markup = InlineKeyboardMarkup([[InlineKeyboardButton("Contact", url=f"tg://resolve?domain={username}")]])
        await context.bot.send_message(text=context.user_data['application_letter'], chat_id=job['user'], reply_markup = markup)
        
    if data == "No":
        await query.answer("Application process cancelled",True)
        await query.message.reply_text("Application cancelled!!!")

    await context.bot.delete_message(chat_id=chat_id, message_id = query.message.message_id)
    return ConversationHandler.END


apply_handler = ConversationHandler(
    entry_points=[CommandHandler('start', apply_for_job, filters=filters.Regex(r'^/start [0-9a-fA-F]{24}$'))],#
    states={
        I: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel$") | filters.Regex("^🔙Back$")), step_two)],
        II: [CallbackQueryHandler(step_three)]
    },
    fallbacks=[]
)



    
