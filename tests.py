import requests_func
import random
from string import ascii_letters
import pytest


def list_id_category():
    limit = requests_func.get_category().json()["count"]
    params = {"limit": limit}
    res = requests_func.get_category(params).json()["results"]
    list_id = [i["id"] for i in res]
    return list_id


def list_name_category(delete=None):
    limit = requests_func.get_category().json()["count"]
    params = {"limit": limit}
    res = requests_func.get_category(params).json()["results"]
    list_name = [i["name"] for i in res]
    if delete in list_name:
        del list_name[list_name.index(delete)]
    return list_name


def list_pet_id():
    limit = requests_func.get_pet().json()["count"]
    params = {"limit": limit}
    res = requests_func.get_pet(params).json()["results"]
    list_id = [i["id"] for i in res]
    return list_id


def list_pet_name(delete=None):
    limit = requests_func.get_pet().json()["count"]
    params = {"limit": limit}
    res = requests_func.get_pet(params).json()["results"]
    list_name = [i["name"] for i in res]
    if delete in list_name:
        del list_name[list_name.index(delete)]


def random_name_generator(n):
    name = ""
    for i in range(n):
        name = name + random.choice(ascii_letters)
    return name


def positive_assert_get_category(limit, offset):
    params = {"limit": limit, "offset": offset}
    res = requests_func.get_category(params)
    assert res.status_code == 200
    assert "count" in res.json()
    assert "next" in res.json()
    assert "previous" in res.json()
    assert "results" in res.json()


def negative_assert_get_category(limit=None, offset=None):
    params = {"limit": limit, "offset": offset}
    res = requests_func.get_category(params)
    assert res.status_code == 500


def positive_assert_post_category(name):
    body = {"name": name}
    res = requests_func.post_category(body)
    assert res.status_code == 201
    assert "id" in res.json()
    assert "name" in res.json()
    assert res.json()["name"] == name


def negative_assert_post_category(name=None, name_value=None):
    if name is None:
        res = requests_func.post_category()
    else:
        body = {name: name_value}
        res = requests_func.post_category(body)
    assert res.status_code == 400


def positive_get_category_id(id_cat):
    res = requests_func.get_category_id(id_cat)
    assert res.status_code == 200
    assert "id" in res.json()
    assert "name" in res.json()
    assert res.json()["id"] == id_cat


def negative_get_category_id(id_cat=None):
    res = requests_func.get_category_id(id_cat)
    if id_cat is None:
        assert res.status_code == 200
        assert "count" in res.json()
    elif type(id_cat) is str:
        assert res.status_code == 400
    elif id_cat not in list_id_category():
        assert res.status_code == 404


def positive_put_category_id(name):
    id_cat = random.choice(list_id_category())
    body = {"name": name}
    res = requests_func.put_category_id(id_cat=id_cat, body=body)
    assert res.status_code == 200
    assert "id" in res.json()
    assert "name" in res.json()
    assert res.json()["id"] == id_cat
    assert res.json()["name"] == name


def negative_put_category_id(id_cat=None, name=None, name_value=None):
    if name is None:
        res = requests_func.put_category_id(id_cat=id_cat)
    else:
        res = requests_func.put_category_id(id_cat, {name: name_value})
    if id_cat is None:
        assert res.status_code == 405
    elif id_cat not in list_id_category():
        assert res.status_code == 404
    elif name in list_name_category():
        assert res.status_code == 500
    else:
        assert res.status_code == 400


def positive_delete_category(id_cat):
    res = requests_func.delete_category_id(id_cat)
    assert res.status_code == 204


def negative_delete_category(id_cat=None):
    res = requests_func.delete_category_id(id_cat)
    if id_cat is None:
        assert res.status_code == 405
    elif type(id_cat) == int and id_cat not in list_id_category():
        assert res.status_code == 404
    elif type(id_cat) != int:
        assert res.status_code == 400
    else:
        assert res.status_code == 500


def positive_assert_get_pet(limit=None, offset=None):
    params = {"limit": limit, "offset": offset}
    res = requests_func.get_pet(params)
    assert res.status_code == 200
    assert "count" in res.json()
    assert "next" in res.json()
    assert "previous" in res.json()
    assert "results" in res.json()


def negative_assert_get_pet(limit=None, offset=None):
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    res = requests_func.get_pet(params)
    assert res.status_code == 500


def positive_post_pet(name, photo_url, category_name, status):
    body = {"name": name, "photo_url": photo_url, "category": {"name": category_name}, "status": status}
    list_status = ["available", "pending", "sold"]
    res = requests_func.post_pet(body)
    assert res.status_code == 201
    assert "id" in res.json()
    assert "name" in res.json()
    assert "category" in res.json()
    assert "status" in res.json()
    assert status in list_status
    assert res.json()["status"] == status


def negative_assert_post_pet(name=None, photo_url=None, category_name=None, status=None):
    body = {}
    if name is not None:
        body["name"] = name
    if photo_url is not None:
        body["photo_url"] = photo_url
    if category_name is not None:
        body["category"] = {"name": category_name}
    if status is not None:
        body["status"] = {"status": status}
    res = requests_func.post_pet(body)
    if type(name) != str or type(photo_url) != str or type(category_name) != str or type(status) != str:
        assert res.status_code == 400
    elif 0 == len(name) > 150 or 0 == len(photo_url) > 150:
        assert res.status_code == 400
    else:
        assert res.status_code == 500


def positive_get_id_pet(id_pet):
    res = requests_func.get_pet_id(id_pet)
    assert res.status_code == 200
    assert "id" in res.json()
    assert "name" in res.json()
    assert "photo_url" in res.json()
    assert "category" in res.json()
    assert "status" in res.json()


def negative_assert_get_pet_id(id_pet=None):
    res = requests_func.get_pet_id(id_pet)
    if id_pet is None:
        assert res.status_code == 200
    elif type(id_pet) != int:
        assert res.status_code == 400
    elif id_pet not in list_pet_id():
        assert res.status_code == 404
    else:
        assert res.status_code == 500


def positive_put_pet_id(id_pet, name, photo_url, category_name, status):
    body = {"name": name, "photo_url": photo_url, "category": {"name": category_name}, "status": status}
    list_status = ["available", "pending", "sold"]
    res = requests_func.put_pet_id(id_pet, body)
    assert res.status_code == 200
    assert "id" in res.json()
    assert "name" in res.json()
    assert "photo_url" in res.json()
    assert "category" in res.json()
    assert "status" in res.json()
    assert status in list_status
    assert res.json()["status"] == status


def negative_assert_put_pet_id(id_pet=None, name=None, photo_url=None, category_name=None, status=None):
    body = {}
    if name is not None:
        body["name"] = name
    if photo_url is not None:
        body["photo_url"] = photo_url
    if category_name is not None:
        body["category"] = {"name": category_name}
    if status is not None:
        body["status"] = status
    res = requests_func.put_pet_id(id_pet, body)
    if type(name) != str or type(photo_url) != str or type(category_name) != str or type(status) != str:
        assert res.status_code == 400
    elif id_pet is None:
        assert res.status_code == 405
    else:
        assert res.status_code == 500


def positive_delete_pet(id_pet):
    res = requests_func.delete_pet_id(id_pet)
    res_test = requests_func.get_pet_id(id_pet)
    assert res.status_code == 204
    assert res_test.status_code == 404


def negative_delete_pet(id_pet=None):
    res = requests_func.delete_pet_id(id_pet)
    if id_pet is None:
        assert res.status_code == 405
    elif id_pet not in list_pet_id():
        assert res.status_code == 404
    else:
        assert res.status_code == 500


def positive_assert_auth_token(username, password):
    body = {"username": username, "password": password}
    res = requests_func.post_token_auth(body)
    assert res.status_code == 200
    assert "token" in res.json()
    assert type("token") == str


def negative_assert_auth_token(username=None, password=None):
    body = {}
    if username is not None:
        body["username"] = username
    if password is not None:
        body["password"] = password
    res = requests_func.post_token_auth(body)
    if type(username) != str or type(password) != str or username == "" or password == "":
        assert res.status_code == 400
    else:
        assert res.status_code == 500


def test_get_category_limit_0_offset_0():
    positive_assert_get_category(0, 0)


def test_get_category_limit_2_offset_5():
    positive_assert_get_category(2, 5)


def test_get_category_limit_5_offset_2():
    positive_assert_get_category(5, 2)


def test_get_category_limit_4999_offset_4999():
    positive_assert_get_category(4999, 4999)


def test_get_category_negative_limit_1_offset_txt():
    negative_assert_get_category(limit=1, offset="SELECT")


def test_get_category_negative_limit_txt_offset_1():
    negative_assert_get_category(limit="SELECT", offset=1)


def test_positive_post_category_name_5_symbols():
    name = random_name_generator(5)
    positive_assert_post_category(name)


def test_positive_post_category_name_1_symbol():
    name = random_name_generator(1)
    positive_assert_post_category(name)


def test_positive_post_category_name_149_symbols():
    name = random_name_generator(149)
    positive_assert_post_category(name)


def test_positive_post_category_150_symbols():
    name = random_name_generator(150)
    positive_assert_post_category(name)


def test_negative_post_category_body_none():
    negative_assert_post_category()


def test_negative_post_category_nameValue_none():
    negative_assert_post_category(name="name")


def test_negative_post_category_nameValue_151_symbols():
    negative_assert_post_category(name="name", name_value=random_name_generator(151))


def test_negative_post_category_nameValue_empty():
    negative_assert_post_category(name="name", name_value="")


def test_positive_get_category_id_real_idCategory():
    id_cat = random.choice(list_id_category())
    positive_get_category_id(id_cat)


def test_negative_category_id_none_idCategory():
    negative_get_category_id()


def test_negative_category_id_notReal_idCategory():
    negative_get_category_id(29093)


def test_negative_category_id_txt_idCategory():
    negative_get_category_id("one")


def test_positive_put_category_nameValue_5symbols():
    name = random_name_generator(5)
    if name in list_name_category(delete=name):
        while name in list_name_category(delete=name):
            name = random_name_generator(5)
    positive_put_category_id(name)


def test_positive_put_category_nameValue_1symbol():
    name = random_name_generator(1)
    if name in list_name_category(delete=name):
        while name in list_name_category(delete=name):
            name = random_name_generator(1)
    positive_put_category_id(name)


def test_positive_put_category_nameValue_149symbols():
    name = random_name_generator(149)
    if name in list_name_category(delete=name):
        while name in list_name_category(delete=name):
            name = random_name_generator(149)
    positive_put_category_id(name)


def test_positive_put_category_nameValue_150symbols():
    name = random_name_generator(150)
    if name in list_name_category(delete=name):
        while name in list_name_category(delete=name):
            name = random_name_generator(150)
    positive_put_category_id(name)


def test_negative_put_category_no_params():
    negative_put_category_id()


def test_negative_put_category_notReal_id():
    negative_put_category_id(id_cat=999999)


def test_negative_put_category_name_none():
    id_cat = random.choice(list_id_category())
    negative_put_category_id(id_cat=id_cat)


def test_negative_put_category_nameValue_none():
    id_cat = random.choice(list_id_category())
    negative_put_category_id(id_cat=id_cat, name="name")


def test_negative_put_category_nameValue_empty():
    id_cat = random.choice(list_id_category())
    negative_put_category_id(id_cat=id_cat, name="name", name_value="")


def test_negative_put_category_nameValue_not_uniq():
    id_cat = random.choice(list_id_category())
    name = random.choice(list_name_category())
    negative_put_category_id(id_cat=id_cat, name="name", name_value=name)


def test_negative_put_category_nameValue_151symbols():
    id_cat = random.choice(list_id_category())
    name = random_name_generator(151)
    negative_put_category_id(id_cat=id_cat, name="name", name_value=name)


def test_positive_delete_category_real_id():
    id_cat = random.choice(list_id_category())
    positive_delete_category(id_cat)


def test_negative_delete_category_not_real_id():
    id_cat = next(filter(lambda x: x not in list_id_category(), range(1, 10000)))
    negative_delete_category(id_cat)


def test_negative_delete_category_txt_id():
    id_cat = random_name_generator(3)
    negative_delete_category(id_cat)


def test_negative_delete_category_none_id():
    negative_delete_category()


def test_positive_get_pet_limit_1_offset_0():
    positive_assert_get_pet(0, 0)


def test_positive_get_pet_limit_2_offset_5():
    positive_assert_get_pet(2, 5)


def test_positive_get_pet_limit_5_offset_2():
    positive_assert_get_pet(5, 2)


def test_positive_get_pet_limit_5000_offset_5000():
    positive_assert_get_pet(5000, 5000)


def test_negative_get_pet_limit_1_offset_txt():
    negative_assert_get_pet(limit=1, offset="string")


def test_negative_get_pet_limit_txt_offset_1():
    negative_assert_get_pet(limit='string', offset=1)


def test_positive_assert_post_pet_photoUrl_150symbols():
    name = random_name_generator(1)
    photo_url = random_name_generator(150)
    category_name = random.choice(list_name_category())
    status = "available"
    positive_post_pet(name, photo_url, category_name, status)


def test_positive_assert_post_pet_name_150symbols():
    name = random_name_generator(150)
    photo_url = random_name_generator(1)
    category_name = random.choice(list_name_category())
    status = "pending"
    positive_post_pet(name, photo_url, category_name, status)


def test_positive_assert_post_pet_valid_value():
    name = random_name_generator(5)
    photo_url = random_name_generator(30)
    category_name = random.choice(list_name_category())
    status = "sold"
    positive_post_pet(name, photo_url, category_name, status)


def test_negative_assert_post_pet_name_151symbols():
    name = random_name_generator(151)
    photo_url = random_name_generator(10)
    category_name = random.choice(list_name_category())
    status = "pending"
    negative_assert_post_pet(name, photo_url, category_name, status)


def test_negative_assert_post_pet_photoUrl_151symbols():
    name = random_name_generator(7)
    photo_url = random_name_generator(151)
    category_name = random.choice(list_name_category())
    status = "pending"
    negative_assert_post_pet(name, photo_url, category_name, status)


def test_negative_assert_post_pet_not_real_category():
    name = random_name_generator(5)
    photo_url = random_name_generator(5)
    category_name = random_name_generator(10)
    status = "pending"
    negative_assert_post_pet(name, photo_url, category_name, status)


def test_negative_assert_post_pet_not_real_status():
    name = random_name_generator(10)
    photo_url = random_name_generator(10)
    category_name = random.choice(list_name_category())
    status = random_name_generator(10)
    negative_assert_post_pet(name, photo_url, category_name, status)


def test_negative_assert_post_pet_name_none():
    photo_url = random_name_generator(10)
    category_name = random.choice(list_name_category())
    status = "pending"
    negative_assert_post_pet(name=None, photo_url=photo_url, category_name=category_name, status=status)


def test_negative_assert_post_pet_photo_none():
    name = random_name_generator(10)
    category_name = random.choice(list_name_category())
    status = "pending"
    negative_assert_post_pet(name=name, photo_url=None, category_name=category_name, status=status)


def test_negative_assert_post_pet_categoryName_none():
    name = random_name_generator(12)
    photo_url = random_name_generator(10)
    status = "pending"
    negative_assert_post_pet(name=name, photo_url=photo_url, category_name=None, status=status)


def test_negative_assert_post_pet_status_none():
    name = random_name_generator(15)
    photo_url = random_name_generator(10)
    category_name = random.choice(list_name_category())
    negative_assert_post_pet(name=name, photo_url=photo_url, category_name=category_name, status=None)


def test_positive_assert_get_pet_id_real_id():
    id_pet = random.choice(list_pet_id())
    positive_get_id_pet(id_pet)


def test_negative_assert_get_pet_id_none_id():
    negative_assert_get_pet_id()


def test_negative_assert_get_pet_id_not_real_id():
    id_pet = next(filter(lambda x: x not in list_pet_id(), range(1, 5000)))
    negative_assert_get_pet_id(id_pet)


def test_negative_assert_get_pet_id_txt_id():
    id_pet = "Select *"
    negative_assert_get_pet_id(id_pet)


def test_positive_put_pet_id_photo_150symbols():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(1)
    photo_url = random_name_generator(150)
    category_name = random.choice(list_name_category())
    status = "available"
    positive_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_positive_put_pet_id_name_150symbols():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(150)
    photo_url = random_name_generator(1)
    category_name = random.choice(list_name_category())
    status = "pending"
    positive_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_positive_put_pet_id_not_real_categoryName():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(8)
    photo_url = random_name_generator(15)
    category_name = random.choice(list_name_category())
    status = "sold"
    positive_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_not_real_id():
    id_pet = next(filter(lambda x: x not in list_pet_id(), range(1, 9999)))
    name = random_name_generator(8)
    photo_url = random_name_generator(15)
    category_name = random.choice(list_name_category())
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_not_uniq_name():
    id_pet = random.choice(list_pet_id())
    name = random.choice(list_name_category())
    photo_url = random_name_generator(15)
    category_name = random.choice(list_name_category())
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_photo_151symbols():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(9)
    photo_url = random_name_generator(151)
    category_name = random.choice(list_name_category())
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_not_real_category_name():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(8)
    photo_url = random_name_generator(15)
    category_name = random_name_generator(24)
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_not_real_status():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(8)
    photo_url = random_name_generator(15)
    category_name = random.choice(list_name_category())
    status = random_name_generator(7)
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_none_id():
    id_pet = None
    name = random_name_generator(8)
    photo_url = random_name_generator(15)
    category_name = random_name_generator(24)
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_none_name():
    id_pet = random.choice(list_pet_id())
    name = None
    photo_url = random_name_generator(150)
    category_name = random.choice(list_name_category())
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_none_photo():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(11)
    photo_url = None
    category_name = random.choice(list_name_category())
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_none_category():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(5)
    photo_url = random_name_generator(150)
    category_name = None
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_status_none():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(9)
    photo_url = random_name_generator(150)
    category_name = random.choice(list_name_category())
    status = None
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_negative_put_pet_id_name_151symbols():
    id_pet = random.choice(list_pet_id())
    name = random_name_generator(151)
    photo_url = random_name_generator(15)
    category_name = random.choice(list_name_category())
    status = "available"
    negative_assert_put_pet_id(id_pet, name, photo_url, category_name, status)


def test_positive_delete_pet_id_ok_id():
    id_pet = random.choice(list_pet_id())
    positive_delete_pet(id_pet)


def test_negative_delete_pet_id_not_real_id():
    id_pet = next(filter(lambda x: x not in list_pet_id(), range(1, 9999)))
    negative_delete_pet(id_pet)


def test_negative_delete_pet_id_none_id():
    negative_delete_pet()


def test_negative_delete_pet_id_txt_id():
    negative_delete_pet("string")


def test_positive_post_token_auth_ok_params():
    positive_assert_auth_token("admin", "admin")


def test_negative_post_token_auth_1():
    negative_assert_auth_token()


def test_negative_post_token_auth_password_none():
    negative_assert_auth_token(username="admin")


def test_negative_post_token_auth_username_none():
    negative_assert_auth_token(password="admin")


def test_negative_post_token_auth_username_int():
    negative_assert_auth_token(username=2, password="admin")


def test_negative_post_token_auth_password_int():
    negative_assert_auth_token(username="admin", password=3)


def test_negative_post_token_auth_params_empty():
    negative_assert_auth_token("", "")



