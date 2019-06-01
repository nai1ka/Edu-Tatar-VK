import vk_api
import datetime
import random
from datetime import date
import time
from dateutil.relativedelta import relativedelta, MO,WE, TH,TU,SU,FR,SA
import requests
import xml.etree.ElementTree as et
from vk_api.longpoll import VkLongPoll, VkEventType

now = datetime.datetime.now()
today = date.today()
monday = (today + relativedelta(weekday=MO(-1))).day 
tuesday = (today + relativedelta(weekday=TU(-1))).day 
wednesday = (today + relativedelta(weekday=WE(-1))).day 
thursday = (today + relativedelta(weekday=TH(-1))).day 
friday = (today + relativedelta(weekday=FR(-1))).day 
saturday = (today + relativedelta(weekday=SA(-1))).day
mon = now.month
moth = ""
user_login={}
user_password={}
if mon == 1:
    moth = "Январь"
if mon == 2:
    moth = "Феварль"
if mon == 3:
    moth = "Март"
if mon == 4:
    moth = "Апрель"  
if mon == 5:
    moth = "Май"    
if mon == 6:
    moth = "Июнь" 
if mon == 7:
    moth = "Июль"
if mon == 8:
    moth = "Август"
if mon == 9:
    moth = "Сентябрь"  
if mon == 10:
    moth = "Октябрь"     
if mon == 11:
    moth = "Ноябрь"    
if mon == 12:
    moth = "Декабрь"  
answer = 0
# API-ключ созданный ранее
token = "aa667c4ff815059e1c6b6ce214783767d28fe947af19dbbcd0d5a00ec22742ad70a20841a96534ddcda4d"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
print((datetime.date.today()+datetime.timedelta(days=1)).day)
# Работа с сообщениями
longpoll = VkLongPoll(vk)
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,"random_id":random.randint(0, 999999) })


def auth(login,password,user_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
        'referer' : 'https://edu.tatar.ru/logon'
        }  
    print(login[user_id])
    print(password[user_id])
    params = {
          'main_login':str(login[user_id]["login"]),
          'main_password':str(password[user_id]["password"])
       }  
    session = requests.Session()
    session.get("https://edu.tatar.ru/logon")
    session.post("https://edu.tatar.ru/logon",params,headers=headers)
    
    return session

def collect(login,passwd,user_id,dayforcol):
    r = auth(login,passwd,user_id).get("https://edu.tatar.ru/user/diary.xml")
    print(r.text)
    data = dict.fromkeys(['Lesson', 'Homework', 'Mark'])
    finish_lesson = []
    homework = []
    mark = []     
    root = et.XML(r.text)
    for elem in root:
        for day1 in elem:
            if(day1.attrib["date"]==str(dayforcol)) and (elem.attrib["month"]=="Май"):
                for lesson in day1.find("classes"):
                    if lesson.text!=None:
                        
                        finish_lesson.append(lesson.text)#УРОК
                    else:
                        finish_lesson.append("None")
                    
                for task in day1.find("tasks"):
                    
                    if task.text != None and task.text !="  " and task.text !=" " :
                        homework.append(task.text)#Задание   
                    else:
                        homework.append("Нет ДЗ")
                for marks in day1.find("marks"):
                    if marks.text!=None:
                        mark.append(marks.text)#Домашка  
                    else:
                        mark.append("Нет оценки")
    data["Lesson"]=finish_lesson
    data["Homewrok"]=homework
    data["Mark"]=mark
    return data
    
    
def main():
    input_login=False
    input_passwd=False
    for event in longpoll.listen():
            
        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:
            
                # Если оно имеет метку для меня( то есть бота)
            if event.to_me:
                
                    # Сообщение от пользователя
                request = event.text
                    
                if request == "Логин":
                    write_msg(event.user_id, "Введите Ваш логин от EduTatar")
                    input_login=True
                elif len(request)==10 and input_login==True:
                    user_login[event.user_id]={"login":request}
                    
                    input_login=False
                    write_msg(event.user_id, "Введите Ваш пароль от EduTatar")
                    input_passwd=True
                elif input_passwd==True:
                    user_password[event.user_id]={"password":request}
                   
                    write_msg(event.user_id, "Авторизация прошла успешно. Введите день для получения оценок.")
                    input_passwd=False
  

                elif request == "Завтра":
                    data=collect(user_login,user_password,event.user_id,(datetime.date.today()+datetime.timedelta(days=1)).day)
                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            write_msg(event.user_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: :"+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])    
                elif request == "Сегодня":
                    data=collect(user_login,user_password,event.user_id,(datetime.date.today()).day)
                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            write_msg(event.user_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])
                elif request == "Понедельник":
                    data=collect(user_login,user_password,event.user_id,monday)
                    print(data)
                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            write_msg(event.user_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])     
                elif request == "Вторник":
                    data=collect(user_login,user_password,event.user_id,tuesday)
                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            write_msg(event.user_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])        
                elif request == "Среда":
                    data=collect(user_login,user_password,event.user_id,wednesday)
                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            write_msg(event.user_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])       
                elif request == "Четверг":
                    data=collect(user_login,user_password,event.user_id,thursday)
                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            write_msg(event.user_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])    
                elif request == "Пятница":
                    data=collect(user_login,user_password,event.user_id,friday)
                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            write_msg(event.user_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i])  
                elif request == "Суббота":
                    data=collect(user_login,user_password,event.user_id,saturday)
                    for i in range(len(data["Lesson"])):
                        if(data["Lesson"][i]!="None"):
                            write_msg(event.user_id, "["+str(i+1)+"]"+"Урок: "+data["Lesson"][i]+"\nДомашняя работа: "+ data["Homewrok"][i]+"\nОценка: "+ data["Mark"][i]) 
                elif request == "Тест":
                    write_msg(event.user_id, "dfgdsfgsdfg\nsfg")
                            

                        
                else:
                    write_msg(event.user_id, "Не понял вашего ответа...")
                     


main()
#aa667c4ff815059e1c6b6ce214783767d28fe947af19dbbcd0d5a00ec22742ad70a20841a96534ddcda4d
    
