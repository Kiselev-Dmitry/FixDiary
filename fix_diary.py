import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, EmptyResultSet

from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Subject
from datacenter.models import Lesson
from datacenter.models import Commendation

COMMENDATION_VARIANTS = [
	"Отлично!",
	"Гораздо лучше, чем я ожидал!",
	"Великолепно!",
	"Ты меня очень обрадовал!",
	"Сказано здорово – просто и ясно!",
	"Очень хороший ответ!",
	"Ты сегодня прыгнул выше головы!",
	"Уже существенно лучше!",
	"Замечательно!",
	"Так держать!",
	"Здорово!",
	"Я тобой горжусь!",
	"Мы с тобой не зря поработали!",
	"Ты растешь над собой!",
	"Теперь у тебя точно все получится!"
]


def fix_marks(name):
	child = get_child(name)
	Mark.objects.filter(schoolkid=child, points__lt=4).update(points=5)


def remove_chastisements(name):
	child = get_child(name)
	сhastisements = Chastisement.objects.filter(schoolkid=child)
	сhastisements.delete()


def add_commendation(name, subject_title):
	child = get_child(name)
	try:
		subject_id = Subject.objects.get(title=subject_title, year_of_study=child.year_of_study).id
	except Subject.DoesNotExist:
		raise Subject.DoesNotExist("Такой предмет не найден. Проверьте правильность и повторите ввод")
	except Subject.MultipleObjectsReturned:
		raise Subject.MultipleObjectsReturnedt("Найдено несколько предметов. Проверьте и повторите")
	last_lesson = Lesson.objects.filter(subject__id=subject_id, group_letter=child.group_letter).last()
	Commendation.objects.create(
		text=random.choice(COMMENDATION_VARIANTS),
		created=last_lesson.date,
		schoolkid=child,
		subject=last_lesson.subject,
		teacher=last_lesson.teacher
	)


def get_child(name):
	try:
		child = Schoolkid.objects.get(full_name__contains=name)
	except Schoolkid.DoesNotExist:
		raise Schoolkid.DoesNotExist("Такой ученик не найден. Проверьте и введите полное имя")
	except Schoolkid.MultipleObjectsReturned:
		raise Schoolkid.MultipleObjectsReturnedt("Найдено несколько учеников. Проверьте и введите полное имя")
	return child
