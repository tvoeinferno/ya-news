import pytest
from http import HTTPStatus

from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, ability_to_comment',
    [(pytest.lazy_fixture('user_client'), True),
     (pytest.lazy_fixture('client'), False)]
)
def test_create_comment_for_anon_and_user(
        parametrized_client, ability_to_comment, news):
    url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.post(url, data={'text': 'Комментарий'})
    assert response.status_code == HTTPStatus.FOUND
    if ability_to_comment:
        assert Comment.objects.count() == 1
        comment = Comment.objects.first()
        assert comment.text == 'Комментарий'
    else:
        assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_comment_with_bad_words(author_client, news):
    url = reverse('news:detail', args=(news.pk,))
    bad_text = f'Текст со словом {BAD_WORDS[0]}'
    response = author_client.post(url, data={'text': bad_text})
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    form = response.context['form']
    assert 'text' in form.errors
    assert WARNING in form.errors['text']
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment, form_data):
    url = reverse('news:edit', args=(comment.pk,))
    response = author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.FOUND
    comment.refresh_from_db()
    assert comment.text == form_data['text']


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, comment):
    url = reverse('news:delete', args=(comment.pk,))
    response = author_client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_other_user_cant_edit_comment(user_client, comment, form_data):
    url = reverse('news:edit', args=(comment.pk,))
    response = user_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != form_data['text']


@pytest.mark.django_db
def test_other_user_cant_delete_comment(user_client, comment):
    url = reverse('news:delete', args=(comment.pk,))
    response = user_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
