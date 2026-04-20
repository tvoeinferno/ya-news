import pytest

from django.urls import reverse
from http import HTTPStatus


@pytest.mark.django_db
def test_news_count_on_home_page(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) == 10


@pytest.mark.django_db
def test_order_news(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    dates = [news.date for news in object_list]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.django_db
def test_comments_order(client, comments_in_news):
    url = reverse('news:detail', args=(comments_in_news.id,))
    response = client.get(url)
    news = response.context['news']
    comments = news.comment_set.all()
    created_times = [comment.created for comment in comments]
    assert created_times == sorted(created_times)


@pytest.mark.django_db
def test_comment_form_availability(client, user_client, comments_in_news):
    url = reverse('news:detail', args=(comments_in_news.pk,))
    response_anon = client.get(url)
    assert 'form' not in response_anon.context
    response_auth = user_client.get(url)
    assert 'form' in response_auth.context
