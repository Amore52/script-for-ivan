from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
    Subject,
    Teacher
    )

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


def fix_marks(kid):
    Mark.objects.filter(schoolkid=kid, points__lt=4).update(points=5)
    

def remove_chastisements(kid):
    bad_comment = Chastisement.objects.filter(schoolkid=kid)
    bad_comment.delete()
    

def create_commendation(kid, lesson):
    subject = Subject.objects.filter(title__contains=lesson, year_of_study=kid.year_of_study).first()
    last_lesson = Lesson.objects.filter(year_of_study=kid.year_of_study, group_letter=kid.group_letter,
                                        subject=subject).order_by('-date').first()
    if subject or last_lesson is None:
        print(f'Предмет "{lesson}" не найден для ученика {kid}.')
        return
    Commendation.objects.create(text=random.choice(praise), created=last_lesson.date, schoolkid=kid,
                                subject=last_lesson.subject, teacher=last_lesson.teacher)
                   


def get_schoolkid(func, name_kid, *args, **kwargs):
    kid = Schoolkid.objects.get(full_name__contains=name_kid)
    try:
        return kid, func(*args, **kwargs)
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено много учеников. Введи полное имя.')
    except Schoolkid.DoesNotExist:
        print('Неверное имя')
    raise Exception()