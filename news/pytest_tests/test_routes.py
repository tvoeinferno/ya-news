import pytest
from pytest_lazyfixture import lazy_fixture as lf
from http import HTTPStatus

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login',
     'users:signup', 'users:logout')
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    if name == 'users:logout':
        response = client.post(url)
        assert response.status_code == HTTPStatus.OK
    else:
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_news_availability_for_anonymous_user(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    ((pytest.lazy_fixture('user_client'), HTTPStatus.NOT_FOUND),
     (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
     (pytest.lazy_fixture('client'), HTTPStatus.FOUND)),
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_pages_availability_for_different_users(
    parametrized_client, expected_status, name, comment
):
    url = reverse(name, args=(comment.pk,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
