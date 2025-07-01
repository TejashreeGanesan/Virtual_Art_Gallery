import pytest
from datetime import datetime

from twisted.python.formmethod import Password

from dao.IVirtualArtGalleryImp import VirtualArtGalleryImp
from entity.artist import Artist

@pytest.fixture
def artists():
   artists= VirtualArtGalleryImp()
   return artists

def test_add_artist(artists):
    cursor = artists.connection.cursor()
    test_artist_id = 16
    test_artist_name = 'test name'

    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()

    artist_obj = Artist(artist_id = test_artist_id,
                        name = test_artist_name,
                        biography = "Test Bio for artist",
                        birth_date=datetime.strptime("2002-03-03", "%Y-%m-%d").date(),
                        nationality="Test Nationality",
                        website="https://tests.com",
                        contact_information="Test Contact Information",
                        is_active=True,
                        password = "Nameee@")
    results = artists.add_artist(artist_obj)
    assert results is True
    cursor.execute("SELECT * FROM Artist WHERE artist_id = %s", (test_artist_id,))
    assert cursor.fetchone() is not None
    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()

def test_update_artist(artists):
    cursor = artists.connection.cursor()
    test_artist_id = 16
    test_artist_name = 'test name'
    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()

    artist_obj = Artist(artist_id=test_artist_id,
                        name=test_artist_name,
                        biography="Test Bio for artist",
                        birth_date=datetime.strptime("2002-03-03", "%Y-%m-%d").date(),
                        nationality="Test Nationality",
                        website="https://tests.com",
                        contact_information="Test Contact Information",
                        is_active=True,
                        password = "Nameee@")
    results = artists.add_artist(artist_obj)
    assert results is True

    new_birth_date = datetime.strptime("2003-03-16", "%Y-%m-%d").date()
    cursor.execute("UPDATE Artist SET birth_date = %s WHERE artist_id = %s", (new_birth_date,test_artist_id,))
    artists.connection.commit()
    cursor.execute("SELECT Birth_Date FROM Artist WHERE artist_id = %s", (test_artist_id,))
    updated_birth_date = cursor.fetchone()[0]
    assert updated_birth_date == new_birth_date

def test_delete_artist(artists):
    cursor = artists.connection.cursor()
    test_artist_id = 16
    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()
    artist_obj = Artist(artist_id=test_artist_id,
                        name="Test Artist",
                        biography="Test Bio for artist",
                        birth_date=datetime.strptime("2002-03-03", "%Y-%m-%d").date(),
                        nationality="Test Nationality",
                        website="https://tests.com",
                        contact_information="Test Contact Information",
                        is_active=True,
                        password = "Nameee@")
    results = artists.add_artist(artist_obj)
    assert results is True
    cursor.execute("SELECT * FROM Artist WHERE artist_id = %s", (test_artist_id,))
    assert cursor.fetchone() is not None
    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()

def test_get_artist_by_id(artists):
    cursor = artists.connection.cursor()
    test_artist_id = 16
    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()
    artist_obj = Artist(artist_id=test_artist_id,
                        name="Test Artist",
                        biography="Test Bio for artist",
                        birth_date=datetime.strptime("2002-03-03", "%Y-%m-%d").date(),
                        nationality="Test Nationality",
                        website="https://tests.com",
                        contact_information="Test Contact Information",
                        is_active=True,
                        password = "Nameee@")
    results = artists.add_artist(artist_obj)
    assert results is True
    fetched_artist = artists.get_artist_by_id(test_artist_id)
    assert fetched_artist is not None
    assert fetched_artist.artist_id == test_artist_id
    assert fetched_artist.name == "Test Artist"
    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()

def test_reactivate_artist(artists):
    cursor = artists.connection.cursor()
    test_artist_id = 16
    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()

    #case 1: artist not found
    result = artists.reactivate_artist(test_artist_id)
    assert result == "not_found"

    #adding inactive artist
    artist_obj = Artist(artist_id=test_artist_id,
                        name="Inactive artist",
                        biography="Test Bio for artist",
                        birth_date=datetime.strptime("2002-03-03", "%Y-%m-%d").date(),
                        nationality="Test Nationality",
                        website="https://tests.com",
                        contact_information="Test Contact Information",
                        is_active=False,
                        password = "Nameee@")
    assert artists.add_artist(artist_obj) is True

    #case 2: reactivate artist
    result = artists.reactivate_artist(test_artist_id)
    assert result == "reactivated"

    #case 3: artist already active
    result = artists.reactivate_artist(test_artist_id)
    assert result == "already_active"
    cursor.execute("DELETE FROM Artist WHERE artist_id = %s", (test_artist_id,))
    artists.connection.commit()






