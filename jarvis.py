import pyttsx3 # pip install pyttsx3
import datetime
import speech_recognition as sr # pip install SpeechRecognition
import wikipedia # pip install wikipedia
import smtplib
import webbrowser as wb
import lock # Arquivo para guardar email e senha
import os
import pyautogui # pip install pyautogui
import psutil # pip install psutil
import pyowm
from urllib.request import urlopen
from contextlib import closing
import json 

engine = pyttsx3.init()

# Definições - Nomeando o significado de cada palavra
# O que o programa deve fazer quando identificar tal palavra
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    time = datetime.datetime.now().strftime("%I:%M")
    speak("São")
    speak(time)
    
def weather():
    owm = pyowm.OWM('2f1c9f675b11136d213525dd72476a12')
    speak("Qual é a sua cidade?")
    cidade = takeCommand()
    if cidade == 'None':
        print("Não foi possível pesquisar")
        speak("Não foi possível pesquisar")
    else:
        city = cidade
        loc = owm.weather_manager().weather_at_place(city)
        speak("A temperatura mínima, máxima e sensação térmica é de:")
        weather = loc.weather
        temp = weather.temperature(unit='celsius')
        for _, val in temp.items():  
            speak(f'{val}')       
def wishme():
    speak ("Senhor, bem-vindo de volta!")
    time() 
    weather()
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour<12:
        speak ("Bom dia.")
    elif hour >= 12 and hour<18:
        speak ("Boa tarde.")
    elif hour >= 18 and hour<24:
        speak ("Boa noite.")
    else: 
        speak ("Boa madrugada.")
    
    speak("Como posso ajudá-lo?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Reconhecendo...")
        query = r.recognize_google(audio, language="pt-br")
        print(query)
    
    except Exception as e:
        print(e)
        return "None"
    return query  

def send_email(subject, msg): 
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        # Para enviar um email, é preciso preencher os dados na file lock.py, 
        #  que funciona como medida de segurança
        server.login(lock.EMAIL_ADDRESS, lock.PASSWORD) 
        message = 'subject: {}\n\n{}'.format(subject, msg)
        # Em ordem, correspondente, destinatário, conteúdo
        server.sendmail(lock.EMAIL_ADDRESS, lock.EMAIL_ADDRESS_SEND, message)
        server.quit()
        speak("E-mail enviado com sucesso!")
        print("E-mail enviado com sucesso!")
    except:
        speak("Falha no envio do E-mail.")

def screenshot():
    img = pyautogui.screenshot()
    img.save("C:/Users/Teste/Pictures/ss.png")

def cpu():
    usage = str(psutil.cpu_percent())
    speak("O desempenho da CPU está em:" +usage)
    battery = psutil.sensors_battery()
    speak("O nível da bateria está em:")
    speak(battery.percent)

# Coração do código - Se ele escutar, 
#  por aqui ele responde
if __name__ == "__main__": 
    wishme()
    while True:
        query = takeCommand().lower()
        # Se ele identificar que o usuário disse "horas",
        #  será ativada a def "time", 
        #  do mesmo jeito funciona para todas as outras funções seguintes
        if 'horas' in query:
             time()
        elif 'temperatura' in query:
            weather()                    
        elif 'wikipédia' in query:
               speak("O que o senhor deseja pesquisar?")
               conteudo = takeCommand()
               # Se não identificar nenhuma fala do usuário,
               #  será cancelada a execução do código,
               #  funcionando do mesmo modo para todos os próximos "if" e "else"
               if conteudo == "None":
                   print("Não foi possível pesquisar")
                   speak("Não foi possível pesquisar")
               else:   
                   query = query.replace("wikipedia","")
                   wikipedia.set_lang("pt")
                   result = wikipedia.summary(conteudo, sentences=2)
                   print(result)
                   speak(result)
        elif 'e-mail' in query:
                speak("Qual o título do e-mail?")
                subject = takeCommand()
                if subject == "None":
                    print("Falha no envio do e-mail.")
                    speak("Falha no envio do e-mail.")
                else:    
                    speak("Qual o conteúdo do e-mail?")
                    msg = takeCommand()
                    if msg == "None":
                        print("Falha no envio do e-mail.")
                        speak("Falha no envio do e-mail.")
                    else:    
                       speak("O senhor disse:"+subject+msg)
                       speak("Você realmente deseja enviar este e-mail?")
                       confirm = takeCommand().lower()
                       if confirm == "sim":
                           send_email(subject, msg)               
                       else: 
                           speak("E-mail cancelado.") 
                           print("E-mail cancelado.")         
        # É preciso verificar se o caminho dos navegadores está correto                         
        elif 'ópera' in query:
                speak("Qual página o senhor deseja abrir?")
                operapath = 'C:/Program Files (x86)/Opera/launcher.exe %s'
                search = takeCommand()
                if search == "None":
                    print("Não foi possível realizar a pesquisa.")
                    speak("Não foi possível realizar a pesquisa.")
                else:    
                     wb.get(operapath).open_new_tab(search+'.com')
        elif 'chrome' in query: 
            speak("Qual página o senhor deseja abrir?")
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search = takeCommand()
            if search == "None":
                print("Não foi possível realizar a pesquisa.")
                speak("Não foi possível realizar a pesquisa.")
            else:    
               wb.get(chromepath).open_new_tab(search+'.com')
        elif 'agenda' in query:
            speak("O que o senhor deseja anotar?")
            data = takeCommand()
            if data == "None":
                print("Não foi possível anotar.")
                speak("Não foi possível anotar.")
            else:
               speak("O senhor realmente deseja que eu anote?"+data)
               confirm = takeCommand().lower()
               if confirm == "sim":
                   # Nesta data.txt ficará salva a anotação.
                   file = open('data.txt', 'w+')
                   file.write(data)
                   file.close()
                   print("Anotado com sucesso!")
                   speak("Anotado com sucesso!")
               else:
                    print("Nota cancelada.")
                    speak("Nota cancelada.")   
        elif 'anotações' in query:
            file = open('data.txt', 'r')
            speak("O senhor pediu para eu anotar:" +file.read())
        elif 'print' in query:
            screenshot()
            speak("Captura de tela salva com sucesso!")
        elif 'cpu' in query:
            cpu()    
        elif 'desativar' in query:
               speak("Desativando...")
               quit()
        # Estas funções, em ordem, reinicia o Windows, desliga o computador
        #  é preciso salvar todo tipo de informação que possa ser afetada antes de realizar algum teste       
        elif 'reiniciar o sistema' in query:
            os.system("shutdown /r /t 1")
        elif 'desligar o sistema' in query:
            os.system("shutdown /s /t 1")