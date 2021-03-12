""""Control by voice with PYTHON3"""

import datetime
import time
import os
import random
import urllib.parse
import webbrowser

import pytz
import playsound
from gtts import gTTS
import speech_recognition as sr
import wikipedia
from IPython import embed;

from constants import CONSTANT_ACTION

r = sr.Recognizer()

def record_audio(lang = 'ja', ask = False):
    """
        Get input of audio
    """
    if ask:
        assistant_speak(ask, lang)
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio, language=lang)
            print(voice_data)
        except sr.UnknownValueError:
            return ''
        except sr.RequestError:
            assistant_speak('すみません、私の声をダウンします。')
        return voice_data.lower()


def assistant_speak(audio_string, language='ja'):
    tts = gTTS(text=audio_string, lang=language, slow=False)
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def get_time_zone_vi(flag):
    date = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
    output = ''
    if flag == 'date':
        output = f"Hôm này là ngày {date.day} tháng {date.month} năm {date.year}"
    else:
        output = f"Bây giờ là {date.hour} giờ {date.minute} phút"
    return output


def get_time_zone(flag):
    date = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
    output = ''
    if flag == 'date':
        output = f"{date.year}年{date.month}月{date.day}日です"
    else:
        output = f"{date.hour}時{date.minute}分です"
    return output


def respond(lang, voice_input):
    if CONSTANT_ACTION[lang]['error'][0] == voice_input:
        assistant_speak(CONSTANT_ACTION[lang]['error'][1], lang)
    if CONSTANT_ACTION[lang]['name'][0] in voice_input:
        assistant_speak(CONSTANT_ACTION[lang]['name'][1], lang)
    if CONSTANT_ACTION[lang]['date'] in voice_input:
        today = get_time_zone_vi('date') if lang == 'vi' else get_time_zone('date')
        assistant_speak(today, lang)
    if CONSTANT_ACTION[lang]['time'] in voice_input:
        time_info = get_time_zone_vi('time') if lang == 'vi' else get_time_zone('time')
        assistant_speak(time_info, lang)
    if CONSTANT_ACTION[lang]['search'][0] in voice_input:
        search = record_audio(lang, CONSTANT_ACTION[lang]['search'][1])
        url = "https://google.com/search?" + urllib.parse.urlencode({'q': search}, encoding='utf-8')
        print(url)
        webbrowser.get().open(url)
        out_inf = CONSTANT_ACTION[lang]['search'][2].format(search)
        assistant_speak(out_inf, lang)
    if CONSTANT_ACTION[lang]['location'][0] in voice_input:
        location = record_audio(lang, CONSTANT_ACTION[lang]['location'][1])
        url = 'https://google.nl/maps/place/' + urllib.parse.urlencode({'': location}, encoding='utf-8')[1:] + '/&amp;'
        print(url)
        webbrowser.get().open(url)
        out_inf = CONSTANT_ACTION[lang]['location'][2].format(location)
        assistant_speak(out_inf, lang)
    if CONSTANT_ACTION[lang]['exit'][0] in voice_input:
        assistant_speak(CONSTANT_ACTION[lang]['exit'][1], lang)
        exit()
    if CONSTANT_ACTION[lang]['wiki'][0] in voice_input:
        search = record_audio(lang, CONSTANT_ACTION[lang]['wiki'][1])
        wikipedia.set_lang(lang)
        results = wikipedia.summary(search, sentences=1)
        print(results)
        assistant_speak(results, lang)
    if CONSTANT_ACTION[lang]['change_lang'][0] in voice_input:
        search = record_audio(lang, CONSTANT_ACTION[lang]['change_lang'][1])
        language = lang
        if lang == 'ja':
            if search == 'ベトナム語':
                language = 'vi'
            elif search == '日本語':
                language = 'ja'
            return language
        elif lang == 'vi':
            if search == 'tiếng việt':
                language = 'vi'
            else:
                language = 'ja'
            return language

time.sleep(1)
assistant_speak('こんにちは。何かお手伝いしましょうか?', 'ja')

lang = []
val = ''
while 1:
    if val:
        if lang[-1:] == ['vi']:
            end_lang = 'vi'
            lang = [end_lang]
            assistant_speak('Chuyển đổi ngôn ngữ thành công. Tôi có thể giúp gì cho bạn không', end_lang)
        elif lang[-1:] == ['ja']:
            end_lang = 'ja'
            lang = [end_lang]
            assistant_speak('日本語に変更しました。何かお手伝いしましょうか?', end_lang)
    language = lang[0] if len(lang) > 0 else 'ja'
    voice_data = record_audio(language)
    val = respond(language, voice_data)
    if val:
        lang.append(val)
