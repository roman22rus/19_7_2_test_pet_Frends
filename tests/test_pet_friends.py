from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert isinstance(result,)
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_add_new_pets_with_valid_data(name = 'игорь', animal_type='ящерица', age= '10',pet_photo = 'ggg.jpg' ):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet_from_database():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets= pf.get_list_of_pets(auth_key, "my_pets")
    pet_id=my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_information_about_pet(name = 'вася', animal_type= 'кот', age = 3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_information_about_pet(auth_key, my_pets['pets'][0]['id'],name,animal_type,age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Здесь нет моего питомца")

def test_post_add_new_pet_simple(name = 'вася', animal_type= 'кот', age = '3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_delete_all_my_pets():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets= pf.get_list_of_pets(auth_key,'my_pets')

    while True:
        if len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, _ = pf.delete_all_my_pets(auth_key, pet_id)
            _, my_pets = pf.get_list_of_pets(auth_key, "my_pets ")
            assert status == 200
            assert pet_id not in my_pets.values()
        break
    status,result = pf.get_list_of_pets(auth_key, " my_pets")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets ")

    assert status == 200
    assert len(result['pets']) == 0



