            #*********||IMPORTING MODULES FOR SPEECH RECOGNITION||**************
import speech_recognition as sr
import os 
import pyttsx3
import webbrowser
import datetime
import json
import spacy
import win32com.client

            #*********||IMPORTING MODULES FOR FACE RECOGNITION||**************
import cv2
import dlib
import numpy as np
import csv
import os
import pandas as pd
import time
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

   #************||USER'S QUERY TAKING, PROCESSING, MANIPULATING, AND STORING FUNCTIONS||***********

#Load the spaCy model for NLP
nlp = spacy.load("en_core_web_sm")


#takes the string as input and speak,used to answer queries by speech
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# def pronounce(text):
#     speaker = win32com.client.Dispatch("SAPI.SpVoice")
#     while True:
#         print("Enter the word you want the computer to speak (or type 'exit' to quit):")
#         s = input()
#         if s.lower() == 'exit':
#             break
#         speaker.Speak(s)
#         break


#takes user's queries 
def takeQuery():
    r=sr.Recognizer()
    with sr.Microphone () as source:
        audio =r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print (f"You:{query}")
            return query
        except Exception as e:
            return "Sorry,Can't recognize,try again!"
        

# JSON file to store user data
USER_DATABASE ='user_data.json'


#loads user data in json file
def load_user_data():
    if os.path.exists(USER_DATABASE):
        with open(USER_DATABASE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


#feeds user data in the json file
def save_user_data(data):
    with open("user_data.json", "w") as file:
        json.dump(data, file)


#process name from the text
def process_name(text):
    print(f"JARVIS:Processing name:{text}")
    doc = nlp(text)
    
    # Extract named entities
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            return entity.text
    
    # Manual fallback for names
    proper_nouns = [token.text for token in doc if token.pos_ in ["PROPN", "NOUN"] and token.text[0].upper() == token.text[0]]
    if proper_nouns:
        return " ".join(proper_nouns)
    return None


#store and update data in json file
def store_user_data(name,info):
    user_data = load_user_data()
    if name not in user_data:
        user_data[name] = {'visits': 1,'last_visit': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'information':info}
    else:
        user_data[name]['visits'] += 1
        user_data[name]['last_visit']= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_user_data(user_data)


#checking for visitor's entry
def check_name(name):
    user_data = load_user_data()
    return user_data.get(name,None)


#extract info from the text and store them as entities in json file
def process_info(text):
    doc = nlp(text)
    entities = [(entity.text) for entity in doc.ents]
    say(entities)
    return entities


#calls process info function
def add_info(text):
    info=process_info(text)
    return info

                     #***************QUERY HANDLING FUNCTIONS****************

#Welcoming function:takes,feed and retrieve user data                      
def Welcome():
    say("Hello!What is your name?")
    intro = takeQuery()
    name=process_name(intro)
    if name:
        visitor =check_name(name)
        svm_model,scaler=train_svm_model()
        predicted_name=recognize(svm_model,scaler)
        if visitor:
            if name==predicted_name:
                visitor['visits'] += 1
                print(f"JARVIS:Welcome back,{name}! This is your visit number {visitor['visits']} Your last visit was on {visitor['last_visit']}.")
                say(f"Welcome back,{name}! This is your visit number {visitor['visits']} Your last visit was on {visitor['last_visit']}.")
                if 'information' in visitor:
                    print(f"JARVIS:Information stored is:{visitor['information']}")
                    say(f"Information stored is:{visitor['information']}")
                store_user_data(name,None)
            else:
                # say(f'Welcome back!{predicted_name},i do not have any information stored about you.')
                say("Wrong identity.Please check the name given.Jarvis inactivated.")
                print("SYSTEM:Please check the name given.Jarvis inactivated.")
                exit()
        else:
            print(f"JARVIS:Hello,{name}! Nice to meet you.Would you like to share more information about you..!?")
            say(f"Hello,{name}! Nice to meet you.Would you like to share more information about you..!?")
            text=takeQuery()
            info = add_info(text)
            if info:
                store_user_data(name,info)
                say("information stored")
                extract_features()         
                    
    else:
        print("jARVIS:No name recognized in the speech.")
        say("No name recognized in the speech.")


#function to open sites
def open_sites():
    try:
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],["google", "https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in text.lower():
                say(f"Opening {site[0]},but don't waste your time")
                webbrowser.open(site[1])
    except:
        print("JARVIS:sorry!!I don't have access to it.Contact Akreeti,my owner,if you want to add this functionality.")
        say("sorry!!I don't have access to it.Contact Akreeti,my owner,if you want to add this functionality.")


#chit-chat with jarvis
def chat(query):
    from groq import Groq
    chatStr=""
    print(f'JARVIS:{chatStr}')
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content":text
            },
            {   
                "role":"assistant",
                "content": ""
            }
            ],
        temperature=1,
        max_tokens=50,
        top_p=1,
        stream=True,
        stop=None,
    )
            
    for response in completion:
        if hasattr(response.choices[0].delta, 'content'):
            assistant_response = response.choices[0].delta.content
                    
            if assistant_response is not None:
                print(assistant_response, end='', flush=True)
                        
                chatStr += assistant_response
                      
    say(chatStr)


#extracting the city name from the text 
def city(text):
    words = text.split(" ")
    try:
        index = words.index("in")
        return words[index+1]
    except (ValueError, IndexError):
        return 'Delhi'
    
    
#weather forecasting
import requests
def get_weather(city,key):
    try:
        url = f'https://api.weatherapi.com/v1/current.json?key={key}&q={city}&days=1&aqi=yes&alerts=yes'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except requests.exceptions.JSONDecodeError:
                    print("Error decoding the JSON response")
                    return None
        else:
            print(f"Error: Received response with status code {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error:{e}")
        return None
    

#News headlines
def news_headlines(url,News_apikey):
    responses = requests.get(url)
    if responses.status_code == 200:
        data = responses.json()
        
        for article in data['articles']:
            print(article['title'])
            say(article['title'])
    else:
        print('JARVIS:Failed to retrieve news:', responses.status_code)


             #***************||FACE RECOGNITION FUNCTIONS||****************

# Initialize dlib's face detector, shape predictor, and face recognition model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

#Extracting 128 facial featuresq
def extract_features(csv_file='live_facial_features.csv', stream_duration=20, num_samples=5):
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    start_time = time.time()

    columns = ['Name'] + [f'Feature_{i+1}' for i in range(128)]
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(columns)

        person_name = input("Enter your name: ")
        descriptors = []
        
        while len(descriptors) < num_samples and (time.time() - start_time) < stream_duration:
            ret, frame = video_capture.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = detector(rgb_frame)

            if faces:
                shape = predictor(rgb_frame, faces[0])
                face_descriptor = face_reco_model.compute_face_descriptor(rgb_frame, shape, num_jitters=1)
                descriptors.append(face_descriptor)

                (x, y, w, h) = (faces[0].left(), faces[0].top(), faces[0].width(), faces[0].height())
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Extracting features', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if descriptors:
            avg_descriptor = np.mean(descriptors, axis=0)
            row = [person_name] + avg_descriptor.tolist()
            writer.writerow(row)

    video_capture.release()
    cv2.destroyAllWindows()


#Training svm model to predict the faces
def train_svm_model(csv_file='live_facial_features.csv'):
    if not os.path.isfile(csv_file):
        print("CSV file not found.Please capture face features first.")
        return None,None
    
    data = pd.read_csv(csv_file)
    X = data.iloc[:, 1:].values
    Y = data.iloc[:, 0].values
    
    # Normalizing features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    #Training KNN model
    svm_model = SVC(kernel='linear', probability=True)
    svm_model.fit(X_scaled, Y)
    return svm_model,scaler


#Taking attendance/Recognizing face using live features
def recognize(svm_model,scaler, csv_file='live_facial_features.csv'):
    if not svm_model:
        print("KNN model and scaler are not initialized.")
        return
    say("Recognizing...")
    print("JARVIS:Recognizing...")
    start_time = time.time()
    stream_duration=10
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector(rgb_frame)
        
        for face in faces:
            shape = predictor(rgb_frame, face)
            face_descriptor = face_reco_model.compute_face_descriptor(rgb_frame, shape, num_jitters=1)
            face_descriptor_np = np.array(face_descriptor).reshape(1, -1)
            face_descriptor_scaled = scaler.transform(face_descriptor_np)
            name = svm_model.predict(face_descriptor_scaled)
            say(f"{name[0]},Recognized")
            print(f"JARVIS:{name[0]},Recognized")
            (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name[0], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or (time.time() - start_time) < stream_duration:
            return name[0]
            
    video_capture.release()
    cv2.destroyAllWindows()



                   #***********||JARVIS ON DUTY||****************
print("Aakruti's programmed JARVIS")
say("Jarvis is sleeping, call 'wake up Jarvis' to wake him up")
print("SYSTEM:Hey there,Jarvis is sleeping.A tip for you:call 'wake up Jarvis' to wake him up")
print("listening...")
wake_up=takeQuery()

if "wake up".lower() in wake_up.lower():
    say("Woke up..!! Hello i am JARVIS A.I. programmed by Akreeti")
    print("JARVIS:Woke up..!! Hello i am JARVIS A.I. programmed by Aakruti")
    count=0
    while True:
        print("I am listening...")
        text=takeQuery()

        if count==0:
            Welcome()
            count+=1

        if "open".lower() in text.lower():
            open_sites()

        elif "your girlfriend".lower() in text.lower():
            say("hehehe,Alexxaa..!!")
 
        elif "the time" in text:
            strfTime=datetime.datetime.now().strftime("%H:%M:%S")
            say(f" the time is {strfTime}")
            print(strfTime)

        elif "capture my facial features".lower() in text.lower():
            extract_features()

        elif "tell me my name".lower() in text.lower():
            svm_model,scaler = train_svm_model()
            recognize(svm_model,scaler)

        elif "Jarvis Quit".lower() in text.lower():
            exit()

        elif "reset chat".lower() in text.lower():
            chatStr=""

        elif  "weather".lower() in text.lower():
            API_KEY = 'd7775f3054284fd6a8a143400242607'
            BASE_URL = 'https://api.weatherapi.com/v1/current.json?key=d7775f3054284fd6a8a143400242607&q=London&days=1&aqi=yes&alerts=yes'
            city =city(text)
            weather_data = get_weather(city,API_KEY)
            if weather_data:
                say(f"temperature there is {weather_data['current']['temp_c']} degree celcius and the weather is {weather_data['current']['condition']['text']}.")
    
        elif "news".lower() in text.lower():
            News_apikey='86195554940c494894989551eea27ecc'  
            url = (f'https://newsapi.org/v2/top-headlines?country=in&apiKey={News_apikey}')
            news_headlines(url,News_apikey)
            
        else:
            chat(text) 

else:
    say("Jarvis is sleeping, call 'wake up Jarvis' to wake him up")           
    print("SYSTEM:You need to say 'wake up Jarvis' to wake him up otherwise you cannot proceed.\n System switched off.Please restart.")
       
    



