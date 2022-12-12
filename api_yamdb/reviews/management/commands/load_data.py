import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Genre, Category, Title, Review, Comment, GenreTitle, User
)
# сюда вставить путь до папки с csv
path = f'{settings.BASE_DIR}/static/data/'
os.chdir(path)  # changes the directory

"""
Для создания базы:
python manage.py migrate --run-syncdb
Для наполнения базы:
python manage.py load_data
Я так и не разобрался как разрулить вопрос с id,
поэтому расписал в ручную для каждой модели
P.S. возможно стоит сделать более цивилизовано
"""


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open('users.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                p.save()

        with open('category.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                p.save()

        with open('genre.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                p.save()

        with open('titles.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )
                p.save()

        with open('genre_title.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = GenreTitle(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    genre=Genre.objects.get(id=row['genre_id'])
                )
                p.save()

        with open('review.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Review(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'], pub_date=row['pub_date']
                )
                p.save()

        with open('comments.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Comment(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )
                p.save()
