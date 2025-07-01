import pytest
from datetime import datetime
from dao.IVirtualArtGalleryImp import VirtualArtGalleryImp
from entity.user import User

@pytest.fixture
def users():
  users= VirtualArtGalleryImp()
  return users

def test_add_user(users):
    cursor = users.connection.cursor()
    test_user_id = 22
    test_user_name = "Test User Name"
    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()

    user_obj = User(user_id = test_user_id,
                    username=test_user_name,
                    password="Test password",
                    email="testemail@gmail.com",
                    first_name="Test First Name",
                    last_name="Test Last Name",
                    date_of_birth=datetime.strptime("1970-01-01", "%Y-%m-%d").date(),
                    profile_picture="https://testimg.png")
    results = users.add_user(user_obj)
    assert results is True
    cursor.execute("SELECT * FROM User WHERE user_id = %s", (test_user_id,))
    assert cursor.fetchone() is not None
    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()

def test_update_user(users):
    cursor = users.connection.cursor()
    test_user_id = 22
    test_user_name = "Test User Name"
    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()
    user_obj = User(user_id=test_user_id,
                    username=test_user_name,
                    password="Test password",
                    email="testemail@gmail.com",
                    first_name="Test First Name",
                    last_name="Test Last Name",
                    date_of_birth=datetime.strptime("1970-01-01", "%Y-%m-%d").date(),
                    profile_picture="https://testimg.png")
    results = users.add_user(user_obj)
    assert results is True

    new_email = "testemail_updated@gmail.com"
    cursor.execute("UPDATE User SET email = %s WHERE User_ID = %s", (new_email,test_user_id,))
    users.connection.commit()
    cursor.execute("SELECT Email FROM User WHERE user_id = %s", (test_user_id,))
    updated_new_email = cursor.fetchone()[0]
    assert updated_new_email == new_email

def test_delete_user(users):
    cursor = users.connection.cursor()
    test_user_id = 22
    test_user_name = "Test User Name"
    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()
    user_obj = User(user_id=test_user_id,
                    username=test_user_name,
                    password="Test password",
                    email="testemail@gmail.com",
                    first_name="Test First Name",
                    last_name="Test Last Name",
                    date_of_birth=datetime.strptime("1970-01-01", "%Y-%m-%d").date(),
                    profile_picture="https://testimg.png")
    results = users.add_user(user_obj)
    assert results is True
    cursor.execute("SELECT * FROM User WHERE user_id = %s", (test_user_id,))
    assert cursor.fetchone() is not None
    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()

def test_get_user_by_id(users):
    cursor = users.connection.cursor()
    test_user_id = 22
    test_user_name = "Test User Name"
    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()
    user_obj = User(user_id=test_user_id,
                    username=test_user_name,
                    password="Test password",
                    email="testemail@gmail.com",
                    first_name="Test First Name",
                    last_name="Test Last Name",
                    date_of_birth=datetime.strptime("1970-01-01", "%Y-%m-%d").date(),
                    profile_picture="https://testimg.png")
    results = users.add_user(user_obj)
    assert results is True

    fetched_user = users.get_user_by_id(test_user_id)
    assert fetched_user is not None
    assert fetched_user.user_id == test_user_id
    assert fetched_user.username == test_user_name
    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()

def test_reactivate_user(users):
    cursor = users.connection.cursor()
    test_user_id = 22
    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()

    #case 1: user not found
    result = users.reactivate_user(test_user_id, "Test password")
    assert result == "not_found"

    #adding inactive user
    user_obj = User(user_id=test_user_id,
                    username="Active User name",
                    password="Test password",
                    email="testemail@gmail.com",
                    first_name="Test First Name",
                    last_name="Test Last Name",
                    date_of_birth=datetime.strptime("1970-01-01", "%Y-%m-%d").date(),
                    profile_picture="https://testimg.png")
    users.add_user(user_obj)

    #case 2: reactivate user
    results = users.reactivate_user(test_user_id,"Test password")
    assert results == "reactivated"

    #case 3: user already active
    result = users.reactivate_user(test_user_id, "Test password")
    assert result == "already_active"

    cursor.execute("DELETE FROM User WHERE user_id = %s", (test_user_id,))
    users.connection.commit()







