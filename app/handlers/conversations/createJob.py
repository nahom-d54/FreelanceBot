from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes, 
                          ConversationHandler,
                          CommandHandler, 
                          MessageHandler,
                          CallbackQueryHandler,
                          filters)
from ..messages import Messages
from ...config import Config

I,II,III,IV,V,VI = range(6)

async def start_step(update: Update, context):
    chat_id = update.effective_user.id
    keyboard = [
        ['Cancel']
        ]
    context.user_data['current_state'] = "0"
    context.user_data['job_details'] = {}
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard= True)
    user_companies =  await context.Company.getCompanyByUser(chat_id)
    context.user_data['user_companies'] = user_companies
    #uc = list(user_companies)
    print(user_companies)
    if not user_companies:
        await update.message.reply_text("Create Company First !!!")
        return ConversationHandler.END
    
    await update.message.reply_text(f"{Messages.JOB_TITLE}", reply_markup=markup)
    return I

async def second_step(update: Update, context ):
    context.user_data['current_state'] = "1"

    #query = update.callback_query
    #selection = query.data
    # keyboard = [
    #     ['🔙Back', 'Cancel']
    #     ]
    # markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard= True)
    user_companies = context.user_data['user_companies']
    print(user_companies, 0)
    keyboard = []
    for company in user_companies:
        company_name = company['name']
        company_id = company['_id']
        board = [InlineKeyboardButton(company_name, callback_data=f'conv:{ company_id }')]
        keyboard.append(board)
    
    messageText = update.message.text
    context.user_data['job_details'].update({ Messages.JOB_TITLE: messageText})

    if messageText == "cancel":
        await update.message.reply_text(text = Messages.CONVERSATION_CANCELLED)
        return ConversationHandler.END

    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"{Messages.JOB_COMPANY}", reply_markup=markup)

    return II


async def third_step(update: Update, context):
    context.user_data['current_state'] = "2"
    # messageText = update.message.text
    query = update.callback_query
    user_companies = context.user_data['user_companies']
    data = query.data.split(":",1)[1]
    chat_id = update.effective_user.id
    
    selected_company =  list(filter(lambda x: str(x['_id']) == data ,user_companies))[0]


    #.get({"_id": data})
    await context.bot.edit_message_text(
        text = selected_company['name'], 
        chat_id = chat_id, 
        message_id = query.message.message_id
    )
    context.user_data['job_details'].update({ Messages.JOB_COMPANY : selected_company['name'], 
                                      "company_id": str(selected_company['_id'])
                                      })

    
    keyboard = [
        ['🔙Back', 'Cancel']
        ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard= True)
    
    #markup = InlineKeyboardMarkup(keyboard)

    # if messageText == "cancel":
    #     await update.message.reply_text(text = Messages.CONVERSATION_CANCELLED)
    #     return ConversationHandler.END


    await query.message.reply_text(f"{Messages.JOB_SALARY}", reply_markup=markup)

    return III

async def fourth_step(update: Update, context):
    context.user_data['current_state'] = "3"
    messageText = update.message.text
    context.user_data['job_details'].update({ Messages.JOB_SALARY : messageText})
    keyboard = [
        ['🔙Back', 'Cancel']
        ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard= True)

    if messageText == "cancel":
        await update.message.reply_text(text = Messages.CONVERSATION_CANCELLED)
        return ConversationHandler.END
    

    await update.message.reply_text(f"{Messages.JOB_DESCRIPTION}", reply_markup=markup)

    return IV
    
async def fifth_step(update: Update, context):
    context.user_data['current_state'] = "4"
    messageText = update.message.text
    context.user_data['job_details'].update({ Messages.JOB_DESCRIPTION : messageText})
    keyboard = [
        ['🔙Back', 'Cancel']
        ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard= True)

    if messageText == "cancel":
        await update.message.reply_text(text = Messages.CONVERSATION_CANCELLED)
        return ConversationHandler.END
    
    
    await update.message.reply_text(f"{Messages.JOB_RESPONSIBILITIES}", reply_markup=markup)

    return V

async def sixth_step(update, context):
    context.user_data['current_state'] = "5"
    messageText = update.message.text
    context.user_data['job_details'].update({ Messages.JOB_RESPONSIBILITIES : messageText})

    data = context.user_data['job_details']

    keyboard = [
        #['Post the job', 'Cancel'],
        [
            InlineKeyboardButton('Submit', callback_data='conv:Submit'),
            InlineKeyboardButton('Cancel', callback_data='conv:Cancel')
        ]   
    ]
    #markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard= True)
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text = Messages.JOB_ALL.format(
            title=data[Messages.JOB_TITLE],
            salary=data[Messages.JOB_SALARY],
            desc=data[Messages.JOB_DESCRIPTION],
            res=data[Messages.JOB_RESPONSIBILITIES],
            company=data[Messages.JOB_COMPANY]
            ),
        reply_markup=markup
        )
    return VI

async def final_step(update: Update, context):
    options = ['Submit', 'Cancel']
    query = update.callback_query
    chat_id = update.effective_user.id
    data = context.user_data['job_details']

    ###################
    msg = Messages.JOB_ALL.format(
            title=data[Messages.JOB_TITLE],
            salary=data[Messages.JOB_SALARY],
            desc=data[Messages.JOB_DESCRIPTION],
            res=data[Messages.JOB_RESPONSIBILITIES],
            company=data[Messages.JOB_COMPANY]
            )
    

    ##################
     #todo: move this to new file
    if query.data.split(':')[1] == options[0]:
        this = await context.Job.createJobListing(context.user_data['job_details'], chat_id)
        admin_id = Config.ADMIN_ID
        this_id = this['_id']
        msg_keyboard = [[InlineKeyboardButton("Approve", callback_data=f'admin:approve:{ this_id }'),
                     InlineKeyboardButton("Deny", callback_data=f'admin:deny:{ this_id }')]]
        msg_markup = InlineKeyboardMarkup(msg_keyboard)
        # forward to admin to approve
        await query.answer("Job Sent for admin approval!", show_alert=True)
        await context.bot.delete_message(chat_id = chat_id, message_id = query.message.message_id)
       # send job to admin for approval
        await context.bot.send_message(chat_id = admin_id, text = msg, reply_markup = msg_markup) # replace the number with admin from env
        
    else:
        #update.message.reply_text()
        await query.answer("Job canceled Successfully !", show_alert=True)
    del context.user_data['job_details']
    del context.user_data['current_state']

    return ConversationHandler.END

async def cancel(update, context):
    return ConversationHandler.END
async def back(update, context):
    print(context.user_data.get('current_state'))
    cs = context.user_data.get('current_state')
    match cs:
        case "1":
            return await start_step(update, context)
        case "2":
            return await second_step(update, context)
        case "3":
            return await third_step(update, context)
        case "4":
            return await fourth_step(update, context)
        
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("create_job",start_step)],
    states={
        I: [MessageHandler(
            filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel$") | filters.Regex("^🔙Back$"))
            ,second_step)],
        # II: [MessageHandler(
        #     filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel$") | filters.Regex("^🔙Back$"))
        #     ,third_step)],
        II: [CallbackQueryHandler(third_step)],
        III: [MessageHandler(
            filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel$") | filters.Regex("^🔙Back$"))
            , fourth_step)],
        IV: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel$") | filters.Regex("^🔙Back$"))
            , fifth_step)],
        V: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel$") | filters.Regex("^🔙Back$"))
            , sixth_step)],
        #VI: [MessageHandler((filters.Regex('Post the job') | filters.Regex('Cancel')), final_step)],
        VI: [CallbackQueryHandler(final_step)]
            
    },
    fallbacks=[MessageHandler(filters.Regex("^Cancel$"), cancel), 
               MessageHandler(filters.Regex("^🔙Back$"), back)]
)


