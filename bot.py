# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ftransc.core as ft
import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



def start(update, context):
    first_Name = update.message.from_user['first_name']
    update.message.reply_text(
        text="Welcome *"+first_Name+"😊\n" +
        "*Here you can cough and test for Covid.\nSend us an audio and we will check if you have Covid", parse_mode='Markdown')

def help(update, context):
    update.message.reply_text(
        text="Here you can find a complete list of the available bot commands:\n" +
        "🔷 /start - welcome message\n" +
        "🔷 /help - show this message\n" +
        "🔷 /author - info about author\n",
        parse_mode='Markdown')

def author(update, context):
    update.message.reply_text(
        text="\n📧 Contact us at:\n[Diego Delgado](diego.delgado.diaz@estudiantat.upc.edu)"+
        "\n[Daniel Gomez](daniel.gomez.bellido@estudiantat.upc.edu)",
        parse_mode='Markdown')

def transcribe_voice(bot,context):
    #duration = context.message.voice.duration
    #logger.info('transcribe_voice. Message duration: '+duration)
    
    # Fetch voice message
    voice =context.bot.getFile(bot.message.voice.file_id)
    id = str(bot.effective_user.id)
    # Transcode the voice message from audio/x-opus+ogg to audio/x-wav
    # One should use a unique in-memory file, but I went for a quick solution for demo purposes

    ft.transcode(voice.download(id+'.ogg'), 'wav')
    os.remove(id+".ogg")

    bot.message.reply_text("You have Covid")   

if __name__ == "__main__":
    os.chdir("Data")
    # Instantiate Updater
    updater = Updater('1449154018:AAG2DCk6up1LYpwujG9aPhU6V-AQ__Bcd5Q',use_context=True)

    # Attach command handlers to dispatcher
    updater.dispatcher.add_handler(CommandHandler('author', author))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Attach voiemessage handler to dispatcher. Note the filter as we ovly want the voice mesages to be transcribed
    updater.dispatcher.add_handler(MessageHandler(Filters.voice, transcribe_voice))

    # Start polling for events from the message queue.
    updater.start_polling()


