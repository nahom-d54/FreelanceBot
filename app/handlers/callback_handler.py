from telegram import Update
from .messages import Messages
from ..db.models import CC
from ..helpers.jobPoster import jobPoster


async def callback(update: Update, context: CC):
    query = update.callback_query
    chat_id = update.effective_user.id
    print(chat_id)
    c = query.data.split(":",2)

    
    if c[0] == "conv":
        await context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)
    elif c[0] == "admin":
        # possibly modularize0
        get_job = await context.Job.findJobByJobId(c[2])
        print(c[2], get_job)
        if c[1] == 'approve':
            context.user_data['this_job'] = get_job
            await jobPoster(update, context, c[2])
        else:
            await context.bot.send_message(text=f"Job {get_job[Messages.JOB_TITLE]} Denied !") 
            # maybe add reason


    q = {c[0]: c[1]}
    user = context.User
    await user.updateUser(chat_id, q)
    await query.answer(text="Setting Updated Successfully", show_alert=True)
    await context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)