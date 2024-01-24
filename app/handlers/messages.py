from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Messages:
    APPLY_FOR_JOB = "To ensure a smooth and efficient application process, please write a brief cover letter introducing yourself and explaining why you are interested in the remote job opportunity. Highlight your relevant skills, experiences, and what makes you a strong candidate. Feel free to mention any remote work experience or your ability to work independently."
    APPLY_STEP_TWO = "Would you like to send this?"
    APPLY_FINAL = "After reviewing your application, the job owner will contact you."
    
    START_MESSAGE = "This bot allows employers to submit their remote job vacancies and employees to apply for the job.\nUse /language to change the language"

    START_MESSAGE_QUESTION = "Are you Employee or Employer ?"
    START_MESSAGE_QUESTION_BUTTON = InlineKeyboardMarkup([[
        InlineKeyboardButton("Employer",callback_data="user_type:Employer"),
        InlineKeyboardButton("Employee",callback_data="user_type:Employee")
    ]])

    # If employer register company name
    COMPANY_NAME = "What is your company name ?" #Force reply


    POST_A_JOB = "Post a job"
    JOB_TITLE = "Job Title"
    JOB_TITLE_SET = "Job title set"
    JOB_DESCRIPTION = "Description"
    JOB_COMPANY = "Company"
    JOB_SALARY = "Salary"
    JOB_RESPONSIBILITIES = "Responsibilities"

    CREATE_JOB_LISTING = "Create a job listing"

    CONVERSATION_CANCELLED = "You cancelled the process successfully"

    #Job Type: On-site - Permanent (Full-time)

    #Job Sector: #Accounting_and_finance

    #Work Location: Addis Ababa, Ethiopia

    JOB_ALL = """
Job Title: {title}

Salary/Compensation: {salary}

Description:

{desc}
Responsibilities:

{res}
__________________
Company: {company}
"""
    
    USER_TYPES = ["Employer", "Employee"]

    CONVERSATION_START_KEYBOARD = [ ['Cancel'] ]
    CONVERSATION_STEP_KEYBOARD = [ ['🔙Back', 'Cancel'] ]
    CONVERSATION_END_KEYBOARD = [
                                [
                                    InlineKeyboardButton('Submit', callback_data='conv:Submit'),
                                    InlineKeyboardButton('Cancel', callback_data='conv:Cancel')
                                ]   
                                ]

class ErrorMessages:
    EMPLOYER_APPLY = "Employer can not apply for a job!!"
    

    