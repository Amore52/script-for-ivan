# Скрипт для жкольного дневника.

Этот скрипт, позволяет изменить плохие оценки на хорошие, удалить все замечания, и добавить похвалу от учителей.

## Установка

Для запуска необходимо перенести файл ```script.py``` в папку с проектом, подключиться к базе с помощью терминала Shell. Далее необходимо скопировать строки ниже, вставить в терминал и нажать Enter:

```commandline
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datacenter.models import Schoolkid, Mark, Teacher, Subject, Lesson, Chastisement, Commendation
import random



praise = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
               'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
               'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
               'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
               'Замечательно!',
               'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!',
               'Я тобой горжусь!',
               'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
               'Я вижу, как ты стараешься!',
               'Ты растешь над собой!', 'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']                            


def fix_marks(name_kid):   
    kid = Schoolkid.objects.get(full_name__contains=name_kid)    
    marks = Mark.objects.filter(schoolkid=kid, points__lt=4).update(points=5)
    

def remove_chastisements(name_kid):  
    kid = Schoolkid.objects.get(full_name__contains=name_kid)
    bad_comment = Chastisement.objects.filter(schoolkid=kid)
    bad_comment.delete()
    

def create_commendation(name_kid, lesson):   
    
    subject = Subject.objects.filter(title__contains=lesson, year_of_study=kid.year_of_study).first()
    if subject is None:
        print(f'Предмет "{lesson}" не найден для ученика {name_kid}.')
        return
    last_lesson = Lesson.objects.filter(year_of_study=kid.year_of_study, group_letter=kid.group_letter,
                                        subject=subject).order_by('-date').first()
    Commendation.objects.create(text=random.choice(praise), created=last_lesson.date, schoolkid=kid,
                                subject=last_lesson.subject, teacher=last_lesson.teacher)
                   
kid = Schoolkid.objects.get(full_name__contains=name_kid)

def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено много учеников. Введи полное имя.')
    except Schoolkid.DoesNotExist:
        print('Неверное имя')
```
---

## Использование
Ввести в терминал соответствующие команды ниже:<br>
### ```safe_execute(fix_marks, name_kid):```
- функция позволит изменить все двойки и тройки на пятерки. Вместо ```name kid``` вписать фамилию и имя. <br>
### ```safe_execute(remove_chastisements, name_kid)``` ### 
- функция позволит удалить все замечания учителя. Вместо ```name kid``` вписать фамилию и имя. <br>
### ```safe_execute(create_commendation, name_kid, lesson)``` ### 
- функция оставит похвалу на последнем уроке. Вместо ```name_kid``` вписать фамилию и имя, вместо ```lesson``` вписать урок.
