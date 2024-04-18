from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '##############'
BOT_USERNAME: Final = '@mari_tutorial_bot'

#Comandos
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá, eu sou um bot de tutorial. Digite /help para ver os comandos disponíveis.')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Sou o primeiro bot de uma sequência de estudos. Digite /custom para ver uma mensagem personalizada.')
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Essa é uma mensagem personalizada. :)')
    
    
#Mensagens
def handle_response(text: str):
    processed: str = text.lower().strip()
    
    match text:
        case 'oi':
            return 'Olá!'
        case 'tchau':
            return 'Até mais!'
        case _:
            return 'Não entendi o que você quis dizer...'
        
        
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text:str = update.message.text
    
    print(f'Usuário ({update.message.chat.id}) in {message_type} enviou: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print(f'Respondendo: "{response}"')
    await update.message.reply_text(response)
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} resultou em erro {context.error}')    
    
    
if __name__ == '__main__':
    print("Bot iniciado!")
    app = Application.builder().token(TOKEN).build()
    
    #Comandos
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    
    #Mensagens
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    
    #Erros
    app.add_error_handler(error)
    
    #Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=5)
