from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datacenter.models import Schoolkid, Mark, Teacher, Subject, Lesson, Chastisement, Commendation
import random


def fix_marks(name_kid):
    try:
        one_kid = Schoolkid.objects.get(full_name__contains=name_kid)
        marks = Mark.objects.filter(schoolkid=one_kid, points__lt=4)
        for mark in marks:
            mark.points = 5
            mark.save()
    except MultipleObjectsReturned:
        print(f'Найдено много учеников с именем - {name_kid}. Введи фамилию и имя.')
    except ObjectDoesNotExist:
        print('Неверное имя')


def remove_chastisements(name_kid):
    try:
        one_kid = Schoolkid.objects.get(full_name__contains=name_kid)
        chast = Chastisement.objects.filter(schoolkid=one_kid)
        chast.delete()
    except MultipleObjectsReturned:
        print(f'Найдено много учеников с именем - {name_kid}. Введи фамилию и имя.')
    except ObjectDoesNotExist:
        print('Неверное имя')


def create_commendation(name_kid, lesson):
    try:
        one_kid = Schoolkid.objects.get(full_name__contains=name_kid)
        one_subject = Subject.objects.filter(title__contains=lesson, year_of_study=one_kid.year_of_study).first()
        last_lesson = Lesson.objects.filter(year_of_study=one_kid.year_of_study, group_letter=one_kid.group_letter,
                                        subject=one_subject).order_by('-date').first()
        Commendation.objects.create(text=random.choice(praise_list), created=last_lesson.date, schoolkid=one_kid,
                                subject=last_lesson.subject, teacher=last_lesson.teacher)
    except MultipleObjectsReturned:
        print(f'Найдено много учеников с именем - {name_kid}. Введи фамилию и имя.')
    except ObjectDoesNotExist:
        print('Неверное имя')


praise_list = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
               'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
               'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
               'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
               'Замечательно!',
               'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!',
               'Я тобой горжусь!',
               'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
               'Я вижу, как ты стараешься!',
               'Ты растешь над собой!', 'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']


remove_chastisements('Степан')

