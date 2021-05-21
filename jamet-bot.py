from tweepy import (Stream, OAuthHandler)
from tweepy.streaming import StreamListener
import time
from os import environ
import tweepy
from urllib3.exceptions import ProtocolError
import random
import datetime
from PIL import Image, ImageFont, ImageDraw 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from datetime import datetime, timedelta, timezone



#sekarang lagi make piku
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

print("connected to twitter")

class StreamListener(tweepy.StreamListener):
    tweet_counter = 0
    nkata = 0
    total_predict = 0

    titel_sebelum = ""
    
    
    
    def on_status(self, status):
        # Static variable
        maks = 10
        print('starting prediction')
        
        
        #Dynamic Variabel
        target_user_id = status.user.id
        target_user = api.get_user(target_user_id)
        
        user = api.me()
        
        user_a = user.id
        user_b = target_user_id
        
        #to check apakah dah follow apa belum
        stats = api.show_friendship(source_id=user_a, source_screen_name=user.screen_name, target_id=user_b, target_screen_name=target_user.screen_name)
        
        #ngecek jumlah followers
        nfolls = status.user.followers_count    
               
        
        
        
        #jika jumlah tweet yang di reply < 5
        
        if StreamListener.tweet_counter < maks:
            
            #jika dia follow akun
            if stats[0].followed_by == True:

                if status.is_quote_status == True:
                    
                    print("> (is quoted)" + status.user.screen_name +
                               ": " + status.text + " ( skipped )")

                elif 'RT' in status.text:
                    
                    print("> (is retweeted)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                elif status.in_reply_to_status_id != None:
                    
                    print("> (is replyied)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")
                    
                

                #kalo followers kurang dari 40
                elif nfolls < 10:
                    
                    time.sleep(10)
                    api.update_status('Maaf followers harus di atas 10 untuk menggunakan bot ini.', in_reply_to_status_id=status.id)
                    print(str(StreamListener.tweet_counter) + ". (less than 10 followers)" + status.user.screen_name +
                                  ": " + status.text + " ( replied )")

                else:
                    #taro sini
                    #import foto
                    newbie = Image.open("./asset/newbie.jpg")
                    junior = Image.open("./asset/junior.jpg")
                    senior = Image.open("./asset/senior.jpg")
                    expert = Image.open("./asset/expert.jpg")
                    tothebone = Image.open("./asset/tothebone.jpg")



                    #font declaration
                    title_font = ImageFont.truetype("./asset/Montserrat-Bold.ttf", 72)
                    date_font = ImageFont.truetype("./asset/Montserrat-Bold.ttf", 12)
                    
                    
                    angka = random.randint(1,100)

                    if StreamListener.titel_sebelum == "newbie":
                        angka = random.randint(31,100)
                    elif StreamListener.titel_sebelum == "junior":
                        angka = random.randint(51,100)
                    elif StreamListener.titel_sebelum == "senior":
                        angka = random.randint(81,100)
                    elif StreamListener.titel_sebelum == "expert":
                        angka = random.randint(96,100)
                    elif StreamListener.titel_sebelum == "tothebone":
                        angka = random.randint(0,30)
                    else:
                        angka = angka                
                        

                    ang = str(angka) + "%"
                    kata2 = ""
                    username = status.user.screen_name
                    x = datetime.now()

                    
                    tz = timezone(timedelta(hours=7))
                    x = x.astimezone(tz)                  

                    tahun = x.year
                    bulan = x.strftime("%B")
                    tanggal = x.strftime("%d")
                    titel = ""

                    date = str(tanggal) + ' ' + bulan + ' ' + str(tahun)
                    

                    if angka > 0 and angka < 31:
                        kata2 = "Selamat! skor kejametan kamu...,,, " + ang + "! Kamu mendapatkan title JAMET NEWBIE, selamat yaa. :)"
                        my_image = newbie
                        titel = "newbie"

                    elif angka > 30 and angka < 51:
                        kata2 = "Widih, skor kak " + username + " " + ang + "! Selamat mendapat title sebagai JAMET JUNIOR."
                        my_image = junior
                        titel = "junior"

                    elif angka > 50 and angka < 81:
                        kata2 = "Hai kak "+ username + ", SELAMATT SKOR KAMU " + ang + "! Selamat menjadi JAMET SENIOR, semoga bisa menjadi panutan juniornya ya!."
                        my_image = senior
                        titel = "senior"

                    elif angka > 80 and angka < 96:
                        kata2 = "Skor kejametan kamu: " + ang + ", cie,,, JAMET EXPERT.. bisa nie dipajang di rumah dan dipamerin ke mamah! selamat!."
                        my_image = expert
                        titel = "expert"

                    elif angka > 95 and angka < 101:
                        kata2 = "BEUH GAK MAIN-MAIN, skor kejametan kak " + username + " " + ang + "! KAMU PANTAS MENDAPAT TITEL INI, SEMOGA SEGERA TOBAT YAH"
                        my_image = tothebone
                        titel = "tothebone"
                    
                    StreamListener.titel_sebelum = titel
                    
                                        
                    image_editable = ImageDraw.Draw(my_image)
                    
                    #settingan biar nengah
                    W, H = (1080,620)
                    w, h = image_editable.textsize(username, font=title_font)
                    h += int(h*0.21)

                    #nama orangnye
                    image_editable.text(((W-w)/2, (H-h)/2), username , font=title_font,  fill="white")


                    #tanggal
                    W, H = (1080,80)
                    w, h = image_editable.textsize(date, font=date_font)
                    h += int(h*0.21)

                    image_editable.text(((W-w)/2, (H-h)/2), date , font=date_font,  fill="white")
                    
                    my_image.save("./asset/result.jpg")
                    
                    #load hasil
                    hasil = "./asset/result.jpg"
                    
                    
                    
                    time.sleep(30)
                    # posting the tweet
                    api.update_with_media(hasil,  kata2 , in_reply_to_status_id = status.id)
                    
                    
                    

                    StreamListener.tweet_counter += 1
                    StreamListener.total_predict += 1

                    #logs
                    print(str(StreamListener.tweet_counter) + ".  " +
                    status.user.screen_name + ": " + status.text + " ( replied )")

            #Jika dia belom follow akun
            else:

                if status.is_quote_status == True:
                    
                    print("> (is quoted)" + status.user.screen_name +
                               ": " + status.text + " ( skipped )")

                elif 'RT' in status.text:
                    
                    print("> (is retweeted)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                elif status.in_reply_to_status_id != None:
                    
                    print("> (is replyied)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                #reply suruh follow dulu
                else:
                    time.sleep(30)
                    api.update_status('Follow dulu ngab, terus coba lagi', in_reply_to_status_id=status.id)
                   
                    print(">"  +
                        status.user.screen_name + ": must follow first"  + " ( replied )") 
            
            
            
        #jika jumlah tweet yang di reply > 5
        else:
            
                      
            print('Max num reached = ' +
                              str(StreamListener.tweet_counter))
            StreamListener.tweet_counter = 0
            print('Istirahat 5 Menit')
            time.sleep(60)
            print ("starting prediction again")
            
        
        print('============================')
        print('max number: ' + str(StreamListener.tweet_counter))
        print('total jamet today: ' + str(StreamListener.total_predict))
        print('============================')       
        
             
        
                      
                      
        
            
    def on_limit(self,track):
        print ("Horrors, we lost %d tweets!" % track)
        
    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

while True:
    try:
        stream.filter(track=["@jametcounter"], stall_warnings=True)

    except Exception as e:
        print (e)
        time.sleep(1)  # to avoid craziness with Twitter
        continue

