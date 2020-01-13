# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

from tkinter import *
import locale
import threading
import time
import requests
import json
import traceback
import feedparser
from PIL import Image, ImageTk
from contextlib import contextmanager


your_province = '' # 서울, 전북, 대전. 전남 알아서 설정하면됩니다.
gov_api_key = '' # Type your OpenAPI key for showing microdust
microdust_req_url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=%s&numOfRows=10&pageNo=1&sidoName=%s&searchCondition=DAILY&_returnType=json' % (gov_api_key, your_province)

LOCALE_LOCK = threading.Lock()
ip_req_url = "http://ip-api.com/json"
ip_data = requests.get(ip_req_url).text
ip_data_region = json.loads(ip_data)
city_code = '1842025'
ui_locale = '' #  '' as default
time_format = 12 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
# news_country_code = 'us'
weather_api_token = '' # openweathermap API key
# google_map_api = ''
currentlong = ip_data_region['lon']
currentlat = ip_data_region['lat']
latitude = None # Set this if IP location lookup does not work for you (must be a string)
longitude = None # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 110
large_text_size = 48
medium_text_size = 28
small_text_size = 18
news_text_size = 35

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('HSYeolumMulbit', xlarge_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('HSYeolumMulbit', large_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('HSYeolumMulbit', medium_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)


class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.wind = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('HSYeolumMulbit', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        # self.windLbl = Label(self, font=('HSYeolumMulbit', medium_text_size), fg="white", bg="black")
        # self.windLbl.pack(side=TOP, anchor=W)
        self.currentlyLbl = Label(self, font=('HSYeolumMulbit', large_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        # self.forecastLbl = Label(self, font=('HSYeolumMulbit', small_text_size), fg="white", bg="black")
        # self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('HSYeolumMulbit', medium_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://ip-api.com/json"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:

            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://ip-api.com/json"
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['lat']
                lon = location_obj['lon']

                location2 = "%s, %s" % (location_obj['city'], location_obj['regionName'])

                # get weather
                weather_req_url = "http://api.openweathermap.org/data/2.5/weather?id=%s&APPID=%s" % (city_code, weather_api_token)
            else:
                location2 = ""
                # get weather
                weather_req_url = "http://api.openweathermap.org/data/2.5/weather?id=%s&APPID=%s" % (city_code, weather_api_token)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)
            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['main']['temp']-273)), degree_sign)
            currently2 = weather_obj['weather'][0]['main']
            # forecast2 = weather_obj["weather"][0]["main"]
            # wind2 = weather_obj["wind"]['speed']

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            # if self.wind != wind2:
            #     self.wind = wind2
            #     self.windLbl.config(text=wind2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get weather." % e)

        self.after(600000, self.get_weather)

class Dust(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.pm10 = ''
        self.pm25 = ''
        self.pm10Lbl = Label(self, font=('HSYeolumMulbit', large_text_size), fg="white", bg="black")
        self.pm10Lbl.pack(side=TOP, anchor=N)
        self.pm25Lbl = Label(self, font=('HSYeolumMulbit', large_text_size), fg="white", bg="black")
        self.pm25Lbl.pack(side=BOTTOM, anchor=E)
        self.get_microdust()


    def get_microdust(self):
        try:
            dustdata = requests.get(microdust_req_url).text
            dust_data = json.loads(dustdata)
            my_city = dust_data['list'][1]
            pm10_2 = my_city['pm10Value']
            pm25_2 = my_city['pm25Value']
            pm10_int = int(pm10_2)
            pm25_int = int(pm25_2)
            if pm10_int < 30:
                if self.pm10 != pm10_2:
                    self.pm10 = pm10_2
                    self.pm10Lbl.config(text='미세먼지 좋음')
            elif 30 <= pm10_int < 80:
                if self.pm10 != pm10_2:
                    self.pm10 = pm10_2
                    self.pm10Lbl.config(text='미세먼지 보통')
            elif 80 <= pm10_int < 150:
                if self.pm10 != pm10_2:
                    self.pm10 = pm10_2
                    self.pm10Lbl.config(text="미세먼지 나쁨")
            else:
                if self.pm10 != pm10_2:
                    self.pm10 = pm10_2
                    self.pm10Lbl.config(text="미세먼지 매우 나쁨")
            if pm25_int < 15:
                if self.pm25 != pm25_2:
                    self.pm25 = pm25_2
                    self.pm25Lbl.config(text="초미세먼지 좋음")
            elif 15 <= pm25_int < 35:
                if self.pm25 != pm25_2:
                    self.pm25 = pm25_2
                    self.pm25Lbl.config(text="초미세먼지 보통")
            elif 35 <= pm25_int < 75:
                if self.pm25 != pm25_2:
                    self.pm25 = pm25_2
                    self.pm25Lbl.config(text="초미세먼지 나쁨")
            else:
                if self.pm25 != pm25_2:
                    self.pm25 = pm25_2
                    self.pm25Lbl.config(text="초미세먼지 매우 나쁨")
        except Exception as e:
            traceback.print_exc()
            print("Error: %s. Cannot get microdust." % e)
        self.after(600000, self.get_microdust)

class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'News' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('UhBee MiMi Bold', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        try:

            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()
            if news_country_code == None:
                headlines_url = "http://news.google.co.kr/news?pz=1&cf=all&ned=kr&hl=ko&output=rss"
            else:
                headlines_url = "http://news.google.co.kr/news?pz=1&cf=all&ned=kr&hl=ko&output=rss"

            feed = feedparser.parse(headlines_url)

            for post in feed.entries[0:6]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get news." % e)

        self.after(600000, self.get_headlines)


class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('UhBee MiMi', news_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)


class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.leftFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.leftFrame.pack(side = LEFT, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame) # 기존
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # news
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=S, padx=100, pady=60)

        # microdust


        self.dust = Dust(self.leftFrame)
        self.dust.pack(side=LEFT, anchor=W, padx=100, pady=60)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
