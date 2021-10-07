import pytest
from django.urls import reverse
from rest_framework import status

# проверка получения списка курсов (list-логика)
# аналогично – сначала вызываем фабрики, затем делаем запрос и проверяем результат
@pytest.mark.django_db
def test_courses_list(api_client, student_factory, course_factory):
    course_factory(_quantity=2, students=student_factory(_quantity=3))
    url = reverse('courses-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


# проверка получения 1го курса (retrieve-логика)
# создаем курс через фабрику
# строим урл и делаем запрос через тестовый клиент
# проверяем, что вернулся именно тот курс, который запрашивали
@pytest.mark.django_db
def test_courses_instance(api_client, course_factory):
    course = course_factory()
    course_factory(_quantity=2)
    url = reverse('courses-detail', args=(course.id,))
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


# проверка фильтрации списка курсов по id
# создаем курсы через фабрику, передать id одного курса в фильтр, проверить результат запроса с фильтром
@pytest.mark.django_db
@pytest.mark.parametrize(
    ["quantity", "instance_num", "expected_status"],
    ((3, 1, status.HTTP_200_OK),
     (3, 4, status.HTTP_400_BAD_REQUEST),))
def test_filter_courses_by_id(quantity,
                              instance_num,
                              expected_status,
                              api_client,
                              course_factory):
    courses = course_factory(_quantity=quantity)
    if instance_num < quantity:
        course = courses[instance_num]
        course_id = course.id
    else:
        course_id = 0
    url = reverse('courses-list')
    response = api_client.get(f'{url}?id={course_id}')
    assert response.status_code == expected_status
    if response.status_code == status.HTTP_200_OK:
        assert len(response.data) == 1
        if len(response.data) > 0:
            assert response.data[0]['id'] == course.id
            assert response.data[0]['name'] == course.name


# проверка фильтрации списка курсов по name
@pytest.mark.parametrize(
    ["name", "data_len"],
    (('Python', 1),
     ('Git', 0),))
@pytest.mark.django_db
def test_filter_courses_by_name(name,
                                data_len,
                                api_client,
                                course_factory):
    course = course_factory(name='Python')
    course_factory(name='SQL')
    course_factory(name='R')
    url = reverse('courses-list')
    response = api_client.get(f'{url}?name={name}')
    data = response.data
    print(data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == data_len
    if len(response.data) > 0:
        assert response.data[0]['name'] == course.name

# тест успешного создания курса
# здесь фабрика не нужна, готовим JSON-данные и создаем курс
@pytest.mark.parametrize(
    ["name", "expected_status"],
    (('Python', status.HTTP_201_CREATED),
     ('', status.HTTP_400_BAD_REQUEST),))
@pytest.mark.django_db
def test_create_course(name, expected_status, api_client, student_factory):
    url = reverse('courses-list')
    response = api_client.post(url, {'name': name})
    assert response.status_code == expected_status
    if response.status_code == status.HTTP_201_CREATED:
        assert response.data['name'] == name

# тест успешного обновления курса
# сначала через фабрику создаем, потом обновляем JSON-данными
@pytest.mark.parametrize(
    ["name", "expected_status"],
    (('Git', status.HTTP_200_OK),
     ('', status.HTTP_400_BAD_REQUEST),))
@pytest.mark.django_db
def test_update_course(name, expected_status, api_client, student_factory, course_factory, ):
    course = course_factory(name='Git', students=student_factory(_quantity=2))
    url = reverse('courses-detail', args=(course.id, ))
    response = api_client.patch(url, {'name': name})
    course.name = name
    assert response.status_code == expected_status
    if response.status_code == status.HTTP_201_CREATED:
        assert response.data['id'] == course.id
        assert response.data['name'] == course.name

# тест успешного удаления курса
@pytest.mark.parametrize(
    ["courses_count", "delete_index", "expected_status"],
    ((1, 0, status.HTTP_204_NO_CONTENT),
     (3, 1, status.HTTP_204_NO_CONTENT),
     (2, 3, status.HTTP_404_NOT_FOUND), ))
@pytest.mark.django_db
def test_delete_course(courses_count,
                       delete_index,
                       expected_status,
                       api_client,
                       student_factory,
                       course_factory):
    courses = course_factory(_quantity=courses_count)
    if delete_index < courses_count:
        course = courses[delete_index]
        course_id = course.id
    else:
        course_id = 0
    url = reverse('courses-detail', args=(course_id,))
    response = api_client.delete(url)
    assert response.status_code == expected_status
    if response.status_code == status.HTTP_204_NO_CONTENT:
        url = reverse('courses-list')
        response = api_client.get(url)
        assert len(response.data) == courses_count - 1


