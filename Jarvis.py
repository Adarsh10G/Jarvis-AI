import pyttsx3 
import speech_recognition as sr
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import requests
import pyjokes
import pyautogui
import urllib.parse

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me how may I help you")       


def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query


# ---------- CONTACTS for Email ----------
contacts = {
    "Example1": "ex1@gmail.com",
    "Example2": "ex2@gmail.com",
    "Example3": "ex3@gmail.com"
}


# ---------- EXTRA FEATURES ----------
def getWeather(city="Delhi"):
    api_key = "your_openweather_api"  # get from openweathermap.org
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degree Celsius with {desc}")
    else:
        speak("City not found.")

def getNews():
    api_key = "your_newsapi_api"  # get from newsapi.org
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json()["articles"][:5]
    for i, article in enumerate(articles, 1):
        speak(f"News {i}: {article['title']}")

def tellJoke():
    joke = pyjokes.get_joke()
    speak(joke)

def remember(data):
    with open("memory.txt", "w") as f:
        f.write(data)
    speak("I will remember that.")

def recall():
    try:
        with open("memory.txt", "r") as f:
            data = f.read()
        speak(f"You told me to remember that {data}")
    except:
        speak("I don't remember anything yet.")

def takeScreenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.png")
    speak("Screenshot taken and saved.")


def sendEmailGmail():
    try:
        speak("Whom should I send the email to?")
        name = takeCommand().lower()
        to = contacts.get(name)

        if not to:
            speak("I don't have this contact saved. Please say the full email address.")
            to = takeCommand().lower()

        speak("What should I say?")
        content = takeCommand()

        subject = "Message from Jarvis"
        body = content

        # Encode for URL
        subject_encoded = urllib.parse.quote(subject)
        body_encoded = urllib.parse.quote(body)

        url = f"https://mail.google.com/mail/?view=cm&fs=1&to={to}&su={subject_encoded}&body={body_encoded}"
        webbrowser.open(url)

        speak("I have opened Gmail compose window with your message. Please check and send it.")
    except Exception as e:
        print(e)
        speak("Sorry, I was not able to compose the email.")


# ---------- MAIN ----------
if _name_ == "_main_":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

      
        elif 'send email' in query or 'email' in query:
            sendEmailGmail()

        elif 'weather' in query:
            speak("Which city should I check?")
            city = takeCommand()
            getWeather(city)

        elif 'news' in query:
            getNews()

        elif 'joke' in query:
            tellJoke()

        elif 'remember that' in query:
            speak("What should I remember?")
            data = takeCommand()
            remember(data)

        elif 'do you remember' in query:
            recall()

        elif 'screenshot' in query:
            takeScreenshot()

        elif 'shutdown' in query:
            os.system("shutdown /s /t 5")

        elif 'restart' in query:
            os.system("shutdown /r /t 5")

        elif 'sleep' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0"