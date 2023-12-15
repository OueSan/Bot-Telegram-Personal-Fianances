# Imports
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)

import logging
from personal_token import private_token

from google_sheets_api import GoogleSheets

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants responsible for being entry points of a conversation
CHOOSE_OPTION, REGISTER_ENTRY_STEP_1, REGISTER_ENTRY_STEP_2, REGISTER_ENTRY_STEP_3, FINALIZE_ENTRY, REGISTER_EXIT_STEP_1, REGISTER_EXIT_STEP_2, REGISTER_EXIT_STEP_3, REGISTER_EXIT_STEP_4, FINALIZE_EXIT, REGISTER_TRANSFER_STEP_1, REGISTER_TRANSFER_STEP_2, REGISTER_TRANSFER_STEP_3, REGISTER_TRANSFER_STEP_4, FINALIZE_TRANSFER, VISUALIZE_REPORT = range(16)

# State functions (functions responsible for doing something, called by the state controller)
async def initiate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['Inflows', 'Outflows', 'Transfers', 'Reports']]

    await update.message.reply_text('Hello! Please choose an option', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSE_OPTION

async def register_entry_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('What kind of inflow do you want to register?', reply_markup=ReplyKeyboardMarkup([["Salary", "Freelance", "Investments Interest", "Others"]], one_time_keyboard=True))

    return REGISTER_ENTRY_STEP_1

async def register_entry_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['category'] = update.message.text
    await update.message.reply_text('How much of entry?', reply_markup=ReplyKeyboardRemove())

    return REGISTER_ENTRY_STEP_2

async def register_entry_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['value'] = update.message.text
    await update.message.reply_text('Would you like to leave a comment?', reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True))

    return REGISTER_ENTRY_STEP_3

async def register_entry_step_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    response = update.message.text
    if response == "Yes":
        await update.message.reply_text('Enter your comment', reply_markup=ReplyKeyboardRemove())
        return FINALIZE_ENTRY
    else:
        await update.effective_chat.send_message('Ok, proceeding without a comment', reply_markup=ReplyKeyboardRemove())
        return await finalize_entry(update, context)
    
# States controler (define what function will be called, according to user input)

async def finalize_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['comment'] = update.message.text
        print(context.user_data['category'])
        print(context.user_data['value'])
        print(context.user_data['comment'])

        category = context.user_data['category']
        value = context.user_data['value']
        comment = context.user_data['comment']

        google_sheets_api = GoogleSheets()
        google_sheets_api.insert_entry(value, category, comment)
    except Exception as error:
        print(error)

async def register_exit_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Select the type of exit", reply_markup=ReplyKeyboardMarkup([["Fixed", "Variable", "Single"]], one_time_keyboard=True))

    return REGISTER_EXIT_STEP_1

async def register_exit_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['classification'] = update.message.text
    await update.message.reply_text("What is the classification the exit", reply_markup=ReplyKeyboardMarkup([["Bills", "Maintenance", "Investments", "Health", "Other"]], one_time_keyboard=True))

    return REGISTER_EXIT_STEP_2

async def register_exit_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['exit_category'] = update.message.text
    await update.message.reply_text("How much is it?", reply_markup=ReplyKeyboardRemove())

    return REGISTER_EXIT_STEP_3

async def register_exit_step_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['exit_value'] = update.message.text
    await update.message.reply_text("Do you want to add a comment?", reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True))

    return REGISTER_EXIT_STEP_4

async def register_exit_step_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    response = update.message.text
    if response == 'Yes':
        await update.message.reply_text("Enter the comment", reply_markup=ReplyKeyboardRemove())
        return FINALIZE_EXIT
    else:
        await update.effective_chat.send_message("Okay, proceeding without comments", reply_markup=ReplyKeyboardRemove())
        return await finalize_exit(update, context)
    
async def finalize_exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['coment'] = update.message.text
        print(context.user_data['classification'])
        print(context.user_data['exit_category'])
        print(context.user_data['exit_value'])
        print(context.user_data['comment'])
        value = context.user_data['exit_value']
        classification = context.user_data['classification']
        category = context.user_data['exit_category']
        comment = context.user_data['comment']

        google_sheets_api = GoogleSheets()
        google_sheets_api.input_outs(value,classification,category,comment)
        
    except Exception as e:
        print('Okay, proceeding without comments')

    await update.message.reply_text("Exit registry succesfully!", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

async def register_transfer_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Which account are you transferring from?", reply_markup=ReplyKeyboardMarkup([["Account 1", "Account 2", "Account 3"]], one_time_keyboard=True))

    return REGISTER_TRANSFER_STEP_1

async def register_transfer_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['source_account'] = update.message.text
    await update.message.reply_text("To which account are you transferring?", reply_markup=ReplyKeyboardMarkup([["Account 1", "Account 2", "Account 3"]], one_time_keyboard=True))

    return REGISTER_TRANSFER_STEP_2

async def register_transfer_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['destination_account'] = update.message.text
    await update.message.reply_text("What is the transfer amount?", reply_markup=ReplyKeyboardRemove())

    return REGISTER_TRANSFER_STEP_3

async def register_transfer_step_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['transfer_amount'] = update.message.text
    await update.message.reply_text("Would you like to add a comment?", reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True))

    return REGISTER_TRANSFER_STEP_4

async def register_transfer_step_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    response = update.message.text
    if response == 'Yes':
        await update.message.reply_text("Enter the comment", reply_markup=ReplyKeyboardRemove())
        return FINALIZE_TRANSFER
    else:
        await update.effective_chat.send_message("Ok, proceeding without comments", reply_markup=ReplyKeyboardRemove())
        
        return await complete_transfer(update, context)

async def complete_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['comment'] = update.message.text
        print(context.user_data['source_account'])
        print(context.user_data['destination_account'])
        print(context.user_data['transfer_amount'])
        print(context.user_data['comment'])

        source = context.user_data['source_account']
        destination = context.user_data['destination_account']
        amount = context.user_data['transfer_amount']
        comment = context.user_data['comment']

        google_sheets_api = GoogleSheets()
        google_sheets_api.input_transfers(amount, source, destination, comment)

        
    except Exception as e:
        print('no coments was infomerd')

    await update.message.reply_text("The transfer was successfully completed.",reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

async def view_report_step_1(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Select the time", reply_markup=ReplyKeyboardMarkup([["Option 1", "Option 2"]], one_time_keyboard=True))


    return VISUALIZE_REPORT

async def view_report_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['period'] = update.message.text
    await update.effective_chat.send_message('Ok, proceeding with the report',reply_markup=ReplyKeyboardRemove())
    
    return await show_report(update, context)

async def show_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    google_sheet_api = GoogleSheets()
    column = update.message.text
    values = google_sheet_api.show_report(column)
    await update.effective_chat.send_message(f"Your {column} was {values}!",reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def input_invalid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('It is not possible to type at this moment, open the keyboard on the right (button 4 dots) and choose an option!')
   

def main():
    application = Application.builder().token(private_token).build()
    # Building conversations routes
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start',initiate),
            CommandHandler('initiate',initiate)
        ],
        states={  
            CHOOSE_OPTION: [
                MessageHandler(filters.Regex("^(Inflows)$"),register_entry_step_1),
                MessageHandler(filters.Regex("^(Outflows)$"),register_exit_step_1),
                MessageHandler(filters.Regex("^(Transfers)$"),register_transfer_step_1),
                MessageHandler(filters.Regex("^(Reports)$"),view_report_step_1)
            ],
            REGISTER_ENTRY_STEP_1:[ 
                MessageHandler(filters.Regex("^(Salary|Freelance|Investmentes Interest|Others)$"),register_entry_step_2),
                MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)
            ],
            REGISTER_ENTRY_STEP_2:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,register_entry_step_3)
            ],
            REGISTER_ENTRY_STEP_3: [
                MessageHandler(filters.Regex("^(Yes|No)$"),register_entry_step_4),
                MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)
            ],
            FINALIZE_ENTRY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, finalize_entry)
            ],
            REGISTER_EXIT_STEP_1:[ 
                    MessageHandler(filters.Regex("^(Fixed|Variable|Single)$"), register_exit_step_2),
                    MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)
            ],
            REGISTER_EXIT_STEP_2:[ 
                MessageHandler(filters.Regex("^(Bills|Maintenance|Investments|Health|Other)$"),register_exit_step_3),
                MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)
            ],
            REGISTER_EXIT_STEP_3:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,register_exit_step_4),
            ],
            REGISTER_EXIT_STEP_4:[
                MessageHandler(filters.Regex("^(Yes|No)$"), register_exit_step_5),
                MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)
            ],
            FINALIZE_EXIT:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, finalize_exit),
            ],
            REGISTER_TRANSFER_STEP_1:[
                    MessageHandler(filters.Regex("^(Account 1|Account 2|Account 3)$"), register_transfer_step_2),
                    MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)
            ],
            REGISTER_TRANSFER_STEP_2:[
                MessageHandler(filters.Regex("^(Account 1|Account 2|Account 3)$"), register_transfer_step_3),
                MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)
            ],
            REGISTER_TRANSFER_STEP_3:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,register_transfer_step_4)
            ],
            REGISTER_TRANSFER_STEP_4:[
                MessageHandler(filters.Regex("^(Yes|No)$"),register_transfer_step_5),
                MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)
            ],
            FINALIZE_TRANSFER:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, finalize_exit),
            ],
            VISUALIZE_REPORT:[
                    MessageHandler(filters.Regex("^(Total Entries|Total Outs|Total Transfers)$"), view_report_step_1),
                    MessageHandler(filters.TEXT & ~filters.COMMAND,input_invalid)

            ],
        
        },
        fallbacks=[
            CommandHandler('start',initiate),
            CommandHandler('initiate',initiate)
        ]
    )

    application.add_handler(conversation_handler)
    application.run_polling()

if __name__ == '__main__':
    main()


