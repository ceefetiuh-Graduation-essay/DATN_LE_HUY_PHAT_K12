#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from model.naive_bayes_model import NaiveBayesModel
from model.svm_model import SVMModel
import os
import pygame
import speech_recognition as sr
import time
import sys
import wikipedia
import datetime
import webbrowser
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
import serial
import csv
import paho.mqtt.client as mqtt
from dis import dis

wikipedia.set_lang('vi')
language = 'vi'
path = "/usr/lib/chromium-browser/chromedriver"

#======================== Setup MQTT ================================#
hostname = "m16.cloudmqtt.com" # host mqtt
portname = 10823
user = "qozkcyle"
password = "2cL7j6TDnqrF"

def post_text(client, topic, text, Qos=0): # hàm gửi dữ liệu
    client.username_pw_set(username=user, password=password) # set user and pass của mqtt-broker server
    client.connect(host=hostname, port=portname) # HOST MQTT BROKER, PORT
    client.publish(topic=topic, payload=text, qos=Qos) # phương thức gửi dữ liệu

class TextClassificationPredict(object):
    def __init__(self):
        #train data
        train_data = []
        with open('/home/pi/Desktop/NLP_Class/data_assistants.csv','rt', encoding='utf8')as f:
          data_assistant = csv.reader(f)
          for row in data_assistant:
                if(row[0]=="" and row[1]==""):
                    pass
                else:
                    train_data.append({"feature": u"{0}".format(row[0]), "target": u"{0}".format(row[1])}) #training data form file data_assistant.csv

        global df_train
        df_train = pd.DataFrame(train_data)

    def classification(self, text, intent=""):
        self.text = text
        self.intent = intent
        test_data = []
        test_data.append({"feature": f"{self.text}", "target": "{self.intent}"})
        df_test = pd.DataFrame(test_data)

        # init model naive bayes
        model = NaiveBayesModel()

        clf = model.clf.fit(df_train["feature"], df_train.target)

        predicted = clf.predict(df_test["feature"])
        print(predicted,"\n")
        print (clf.predict_proba(df_test["feature"]),"\n")
        return predicted

class lora():
    def __init__(self,ser, client):
        self.ser = ser
        self.client = client

    def lorasend(self, text):
        self.text = text
        try:
            self.ser.write(self.text)
            self.ser.flush()

        except KeyboardInterrupt:
            self.ser.close()

    def lorareceive(self):
        try:
            s = self.ser.readline()
            data = s.decode()           # decode s
            data = data.rstrip()        # cut "\r\n" at last of string
            print(data)
            if data == "dON":
                speak("Đèn đã bật")
            elif data == "dOFF":
                speak("Đèn đã tắt")
            elif data == "bON":
                speak("Bơm đã bật")
            elif data == "bOFF":
                speak("Bơm đã tắt")
            else: speak("Tác vụ chưa được thực hiện.")
            if data != "":
                post_text(client=self.client, topic="Status", text=data, Qos=1) #self.text
            return data

        except KeyboardInterrupt:
            ser.close()

class assistant_control():
    def __init__(self, obj_model, obj_lora):
        self.obj_model = obj_model
        self.obj_lora = obj_lora

    def check(self):
        try:
            text = get_text()
            if(text =="Trợ lý" or text=="trợ lý"):
                speak("Dạ")
                text = get_text()
                if "bật" in text:
                    text = self.obj_model.classification(text,"bat_den")
                elif "tắt" in text:
                    text = self.obj_model.classification(text,"tat_den")
                else:
                    text = self.obj_model.classification(text)
                self.text=text
            else:
                self.text = ""
        except:
            pass

    def main(self):
        if self.text[0] == "bat_den":
            self.obj_lora.lorasend(b"1")
            self.obj_lora.lorareceive()

        elif self.text[0] == "tat_den":
            self.obj_lora.lorasend(b"2")
            self.obj_lora.lorareceive()

        elif self.text[0] == "bat_bom":
            self.obj_lora.lorasend(b"3")
            self.obj_lora.lorareceive()

        elif self.text[0] == "tat_bom":
            self.obj_lora.lorasend(b"4")
            self.obj_lora.lorareceive()

        elif self.text[0] == "hoi_chuc_nang":
            help_me()
        elif self.text[0] == "chao_hoi":
            hello()
        elif self.text[0] == "hoi_gio":
            get_time_h()
        elif self.text[0] == "hoi_ngay":
            get_time_d()
        elif self.text[0] == "hoi_thoi_tiet":
            current_weather()
        elif self.text[0] == "hoi_dinh_nghia":
            tell_me_about()
        else:
            pass

def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.play()
    os.remove("sound.mp3")

def get_audio():
    print("\nBot: \tĐang nghe \t --__-- \n")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=8, snowboy_configuration=None)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            if("Hồ Chí Minh" in text):
                text = "Ho Chi Minh"
            elif("Đồng Nai" in text):
                text = "Dong Nai"
            return str(text.lower())
        except:
            print("...")
            return 0

def stop():
    speak("Hẹn gặp lại bạn sau!")

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
    return 0

def hello():
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn. Chúc bạn một ngày tốt lành.")
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn. Bạn đã dự định gì cho chiều nay chưa.")
    else:
        speak("Chào buổi tối bạn. Bạn đã ăn tối chưa nhỉ.")


def get_time_h():
    now = datetime.datetime.now()
    speak('Bây giờ là %d giờ %d phút %d giây' % (now.hour, now.minute, now.second))

def get_time_d():
    now = datetime.datetime.now()
    speak("Hôm nay là ngày %d tháng %d năm %d" %(now.day, now.month, now.year))

def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute, 
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        speak(content)

    else:
        speak("Không tìm thấy địa chỉ của bạn")

def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        #time.sleep(2)
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0].split(".")[0])
        #time.sleep(10)
        #for content in contents[1:]:
        #    speak("Bạn muốn nghe thêm không")
        #    #time.sleep(2)
        #    ans = get_text()
        #    if "có" not in ans:
        #        break
        #    speak(content)
            #time.sleep(10)

        #speak('Cảm ơn bạn đã lắng nghe!!!')
        #time.sleep(3)
    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")
        #time.sleep(5)

def help_me():
    speak("""Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Hiển thị ngày
    4. Dự báo thời tiết
    5. Kể bạn biết về thế giới
    6. Điều khiển các thiết bị điện trong nhà của bạn.""")

def control(obj_assistant):
    obj_assistant.check()
    obj_assistant.main()

if __name__ == "__main__":
    client = mqtt.Client(protocol=mqtt.MQTTv311) # tạo 1 client mới version MQTTv311
    ser = serial.Serial(
        port = '/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2
    )
    obj_model = TextClassificationPredict() # khởi tạo object
    obj_lora = lora(ser, client)
    obj_assistant = assistant_control(obj_model, obj_lora)
    #=================== Assistant ===================#
    speak("Xin chào, tôi là trợ lý do Huy Phát tạo ra.")
    while True:
        try:
            control(obj_assistant)
            dis(control)
        except:
            pass

