from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
                          ConversationHandler,
                          CommandHandler, 
                          MessageHandler,
                          CallbackQueryHandler,
                          filters)
from ..messages import Messages


I,II,III,IV,V,VI = range(6)

async def start_step(update, context):
    
    markup = ReplyKeyboardMarkup(Messages.CONVERSATION_START_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text("Company Name", reply_markup = markup)

    return I

async def second_step(update: Update, context):
    company_name = update.message.text
    context.user_data['company_name'] = company_name
    markup = InlineKeyboardMarkup(Messages.CONVERSATION_END_KEYBOARD)
    await update.message.reply_text(f"Company Name : {company_name}", reply_markup=markup)

    return II
async def final_step(update: Update, context):
    query = update.callback_query
    chat_id = update.effective_user.id
    data = query.data.split(":",1)[1]
    company_name = context.user_data['company_name']
    options = ['Submit', 'Cancel']
    if data == options[0]:
        await context.Company.insertCompany({"name": company_name}, chat_id)
        await query.answer("Company created succssfully", show_alert=True)
    else:
        await query.answer("Company creation cancelled succssfully", show_alert=True)
    
    await context.bot.delete_message(chat_id=chat_id,message_id=query.message.message_id)
        
    return ConversationHandler.END

async def cancel(update, context):
    return ConversationHandler.END
async def back(update, context):
    # print(context.user_data.get('current_state'))
    cs = context.user_data.get('current_state')
    match cs:
        case "1":
            return await start_step(update, context)
        case "2":
            return await second_step(update, context)
        # case "3":
        #     return await third_step(update, context)
        # case "4":
        #     return await fourth_step(update, context)

create_company_conv_handler = ConversationHandler(
    entry_points= [CommandHandler('create_company', start_step)],
    states= {
        I: [MessageHandler(
            filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel$") | filters.Regex("^🔙Back$"))
            ,second_step)],
        II: [CallbackQueryHandler(final_step)]
    },
    fallbacks = [MessageHandler(filters.Regex("^Cancel$"), cancel), 
               MessageHandler(filters.Regex("^🔙Back$"), back)]
)