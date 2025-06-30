import pytest
from datetime import datetime
from dao.IVirtualArtGalleryImp import VirtualArtGalleryImp
from entity.gallery import Gallery

@pytest.fixture
def gallery():
    gallery = VirtualArtGalleryImp()
    return gallery

def test_add_gallery(gallery):
    cursor = gallery.connection.cursor()
    test_gallery_id = 12
    cursor.execute("DELETE FROM Gallery where Gallery_ID = %s", (test_gallery_id,))
    gallery.connection.commit()

    gallery_obj = Gallery(
        gallery_id=test_gallery_id,
        name = "Test Gallery Name added",
        description = "Test Gallery Description added",
        location = "Test Gallery Location",
        curator = 1,
        opening_hours = "10 AM - 10 PM"
    )
    result = gallery.add_gallery(gallery_obj)
    assert result is True
    cursor.execute("SELECT * FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    assert cursor.fetchone() is not None

    cursor.execute("DELETE FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    gallery.connection.commit()

def test_update_gallery(gallery):
    cursor = gallery.connection.cursor()
    test_gallery_id = 15
    cursor.execute("DELETE FROM Gallery where Gallery_ID = %s", (test_gallery_id,))
    gallery.connection.commit()

    gallery_obj = Gallery(
        gallery_id=test_gallery_id,
        name="Test Original Title",
        description="Test Original Gallery Description",
        location="Test Original Gallery Location",
        curator=1,
        opening_hours="10 AM - 10 PM"
    )
    result = gallery.add_gallery(gallery_obj)
    assert result is True

    new_opening_hours = "11 AM - 6 PM"
    new_curator = 2
    cursor.execute("UPDATE Gallery SET Opening_hours = %s WHERE Gallery_ID = %s", (new_opening_hours, test_gallery_id,))
    gallery.connection.commit()
    cursor.execute("SELECT Opening_hours FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    updated_opening_hours = cursor.fetchone()[0]
    assert updated_opening_hours == new_opening_hours
    cursor.execute("UPDATE Gallery SET Curator = %s WHERE Gallery_ID = %s", (new_curator, test_gallery_id,))
    gallery.connection.commit()
    cursor.execute("SELECT Curator FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    updated_curator = cursor.fetchone()[0]
    assert updated_curator == new_curator

    cursor.execute("DELETE FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    gallery.connection.commit()

def test_delete_gallery(gallery):
    cursor = gallery.connection.cursor()
    test_gallery_id = 15
    gallery_obj = Gallery(
        gallery_id=test_gallery_id,
        name="Test Original Title",
        description="Test Original Gallery Description",
        location="Test Original Gallery Location",
        curator=1,
        opening_hours="10 AM - 10 PM"
    )
    result = gallery.add_gallery(gallery_obj)
    assert result is True

    cursor.execute("SELECT * FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    assert cursor.fetchone() is not None

    cursor.execute("DELETE FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    gallery.connection.commit()

def test_search_for_artwork(gallery):
    cursor = gallery.connection.cursor()
    test_gallery_id = 15
    test_name = "Gallery to be searched"
    test_location = "Gallery Location"
    test_curator = 1
    cursor.execute("DELETE FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    gallery.connection.commit()

    gallery_obj = Gallery(
        gallery_id=test_gallery_id,
        name= test_name,
        description="Test Original Gallery Description",
        location=test_location,
        curator=test_curator,
        opening_hours="10 AM - 10 PM"
    )
    gallery.add_gallery(gallery_obj)
    search_by = 'curator'
    keyword = "1"
    field_map = {
        'name': 'Name',
        'location': 'Location',
        'curator': 'Curator'
    }

    column = field_map[search_by]

    if search_by == 'curator':
        if not keyword.strip().isdigit():
            print("Curator ID must be a number.")
            assert False
            return
        curator = int(keyword.strip())
        query = "SELECT * FROM Gallery WHERE Curator = %s"
        cursor.execute(query, (curator,))
    else:
        like_pattern = f"%{keyword}%"
        query = f"SELECT * FROM Gallery WHERE {column} LIKE %s"
        cursor.execute(query, (like_pattern,))
    results = cursor.fetchall()
    assert any(row[0] == test_gallery_id for row in results)

    cursor.execute("DELETE FROM Gallery WHERE Gallery_ID = %s", (test_gallery_id,))
    gallery.connection.commit()












