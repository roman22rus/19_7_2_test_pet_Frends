import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': passwd,
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
            со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
            либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
            собственных питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_new_pet(self, auth_key: json, name: str, animal_type:str, age: str, pet_photo:str) -> json:
        """ Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON для добавление питомца на сайт"""
        data = MultipartEncoder(
            fields= {
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')

            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key : json, pet_id: str)-> json:
        """удаление существующего питомца"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url+'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def put_update_information_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Обновление информации о питомце"""
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        headers = {'auth_key': auth_key['key']}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_new_pet_simple(self, auth_key: json, name : str, animal_type: str, age: str) -> json :
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON для добавление питомца на сайт, но без добавдения фото"""
        data ={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        headers = {'auth_key': auth_key['key'],"Content-Type": ""}
        res = requests.put(self.base_url + 'api/pets' , headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_all_my_pets(self, auth_key: json, pet_id: str) -> json:
        """удаление существующего питомца"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result