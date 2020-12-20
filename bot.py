# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ftransc.core as ft
import logging
import os
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, load_model

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
SAMPLING_RATE = 16000



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

def path_to_audio(path):
    """Reads and decodes an audio file."""
    audio = tf.io.read_file(path)
    audio, _ = tf.audio.decode_wav(audio, 1, SAMPLING_RATE)
    return audio

def audio_to_fft(audio):
    # Since tf.signal.fft applies FFT on the innermost dimension,
    # we need to squeeze the dimensions and then expand them again
    # after FFT
    audio = tf.reshape(audio, [-1, 16000, 1])
    audio = tf.squeeze(audio, axis=-1)
    fft = tf.signal.fft(
        tf.cast(tf.complex(real=audio, imag=tf.zeros_like(audio)), tf.complex64)
    )
    fft = tf.expand_dims(fft, axis=-1)

    # Return the absolute value of the first half of the FFT
    # which represents the positive frequencies
    return tf.math.abs(fft[:, : (audio.shape[1] // 2), :])

def predict_model(pathAudio):
    audio = path_to_audio(pathAudio) 
    ffts = audio_to_fft(audio)
    # Predict
    y_pred = new_model.predict(ffts)
    return y_pred[0]



def voice_signal(bot,context):
    voice =context.bot.getFile(bot.message.voice.file_id)
    id = str(bot.effective_user.id)
    # Transcode the voice message from audio/x-opus+ogg to audio/x-wav
    ft.transcode(voice.download(id+'.ogg'), 'wav')
    os.remove(id+".ogg")
    predict=predict_model("/home/dani/Covid-Cough-Challenge/Data/"+id+".wav")
    neg = predict[0]*100
    posAsymp= predict[1]*100
    pos = predict[2]*100
    bot.message.reply_text(text="You are:\n *"+ str("%.2f" % neg)+ "% negative*, \n*"+
        str("%.2f" % posAsymp)+ "% positive asymptomatic* and\n*" +
        str("%.2f" % pos)+ "% positive* of Covid\n \n Check your local authorities if you have a bad score on negative covid",parse_mode='Markdown')

if __name__ == "__main__":
    os.chdir("Data")
    # Instantiate Updater
    updater = Updater('1449154018:AAG2DCk6up1LYpwujG9aPhU6V-AQ__Bcd5Q',use_context=True)
    
    new_model = tf.keras.models.load_model('/home/dani/Covid-Cough-Challenge/models/model/')


    # Attach command handlers to dispatcher
    updater.dispatcher.add_handler(CommandHandler('author', author))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Attach voiemessage handler to dispatcher. Note the filter as we ovly want the voice mesages to be transcribed
    updater.dispatcher.add_handler(MessageHandler(Filters.voice, voice_signal))

    # Start polling for events from the message queue.
    updater.start_polling()


