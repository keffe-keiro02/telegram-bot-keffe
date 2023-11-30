from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
from youtubesearchpython import VideosSearch


key_token = "6656238596:AAEyeY5zt-fWH1HWK1T8k5vbkI2zMs54cAE" #Masukkan KEY-TOKEN BOT 
user_bot = "KeffeBot" #Masukkan @user bot


async def  start_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gunakan /help untuk menampilkan apa yang dapat saya berikan..")
    
async def  help_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim pesan, bot akan membalas pesan..")


async def  text_massage(update: Update, context:ContextTypes.DEFAULT_TYPE):
    text_diterima : str = update.message.text
    print(f"Pesan diterima : {text_diterima}")
    text_lwr_diterima = text_diterima.lower()
    if 'halo' in text_lwr_diterima:
        await update.message.reply_text("Hallo juga")
    elif 'hi' in text_lwr_diterima:
        await update.message.reply_text("Hi")
    elif 'selamat malam' in text_lwr_diterima:
        await update.message.reply_text("Selamat malam..., jangan lupa istirahat 😊")
    elif 'selamat siang' in text_lwr_diterima:
        await update.message.reply_text("Selamat siang..., Semangat menjalankan aktivitas😊")
    elif 'selamat pagi' in text_lwr_diterima:
        await update.message.reply_text("Selamat pagi..., jangan lupa Sarapan 😊")
    elif 'siapa kamu ?' in text_lwr_diterima:
        await update.message.reply_text(f"bot adalah : {user_bot}")
    else:
        await update.message.reply_text("bot tidak mengerti")


async def photo_message(update: Update, context:ContextTypes.DEFAULT_TYPE):
    return await update.message.reply_text("Gambar kamu bagus")
        
async def  error(update: Update, context:ContextTypes.DEFAULT_TYPE):
    print(f"error... : {context.error}")

async def youtube_search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Command '/youtube' triggered")

    if context.args:
        query = ' '.join(context.args)
        print(f"Search query: {query}")
    else:
        await update.message.reply_text("Please provide a search query.")
        return

    num_results = 5

    try:
        if len(context.args) > 1 and context.args[-1].isdigit():
            num_results = int(context.args[-1])
            query = ' '.join(context.args[:-1])

        print(f"Number of results to fetch: {num_results}")

        video_search = VideosSearch(query, limit=num_results)
        results = video_search.result()

        if results and 'result' in results and results['result']:
            response_text = f'Here are the top {num_results} results for "{query}" on YouTube:\n'
            for video in results['result']:
                response_text += f"{video['title']}\n{video['link']}\n\n"
            await update.message.reply_text(response_text)
        else:
            await update.message.reply_text("No results found.")
    except Exception as e:
        print(f"Error searching YouTube: {e}")



if __name__ == '__main__':
    print("Mulai")
    app = Application.builder().token(key_token).build()
    #COMMAND :
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('youtube', youtube_search_command))
    #MESSAGE:
    app.add_handler(MessageHandler(filters.TEXT, text_massage))
    app.add_handler(MessageHandler(filters.PHOTO, photo_message))
    #error :
    app.add_error_handler(error)
    #polling :
    app.run_polling(poll_interval=1)
