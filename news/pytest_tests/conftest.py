
import pytest

from django.utils import timezone
from django.test.client import Client

from datetime import timedelta

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='Пользователь')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def user_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        text='Текст комментария',
        news=news,
        author=author,
    )
    return comment


@pytest.fixture
def news_list():
    today = timezone.now()
    news = []
    title = 'Новость'
    text = 'Текст новости'
    for num in range(12):
        date = today - timedelta(days=num)
        news.append(News(title=title + str(num), text=text, date=date))
    News.objects.bulk_create(news)
    return News.objects.all()


@pytest.fixture
def comments_in_news(news, author):
    now = timezone.now()
    text = 'Комментарий'
    comments = []
    for num in range(5):
        created = now - timedelta(hours=num)
        comments.append(
            Comment(
                news=news,
                author=author,
                text=text + str(num),
                created=created)
        )
    Comment.objects.bulk_create(comments)
    return news


@pytest.fixture
def form_data():
    return {
        'text': 'Обновленный текст для комментария'
    }
