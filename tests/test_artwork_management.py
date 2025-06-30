import pytest
from datetime import datetime
from dao.IVirtualArtGalleryImp import VirtualArtGalleryImp
from entity.artwork import Artwork

@pytest.fixture
def gallery():
    gallery = VirtualArtGalleryImp()
    return gallery

def test_add_artwork(gallery):
    cursor = gallery.connection.cursor()
    test_artwork_id = 13
    test_title = "Test Art to be added"

    cursor.execute("DELETE FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    gallery.connection.commit()

    artwork = Artwork(
        artwork_id=test_artwork_id,
        title=test_title,
        description="Uploaded for testing",
        creation_date=datetime(2022, 5, 10).date(),
        medium="Oil on Canvas",
        image_url="https://test_art.jpg",
        artist_id=1
    )

    result = gallery.add_artwork(artwork)
    assert result is True

    cursor.execute("SELECT * FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    assert cursor.fetchone() is not None

    cursor.execute("DELETE FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    gallery.connection.commit()


def test_update_artwork(gallery):
    cursor = gallery.connection.cursor()
    test_artwork_id = 15
    test_title = "Artwork to Update"

    cursor.execute("DELETE FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    gallery.connection.commit()

    artwork = Artwork(
        artwork_id=test_artwork_id,
        title=test_title,
        description="Original description",
        creation_date=datetime(2022, 5, 10).date(),
        medium="Watercolor",
        image_url="https://test_art.jpg",
        artist_id=1
    )

    result = gallery.add_artwork(artwork)
    assert result is True

    new_medium = 'Acrylic'
    cursor.execute("UPDATE Artwork SET Medium = %s WHERE Artwork_ID = %s", (new_medium, test_artwork_id))
    gallery.connection.commit()

    cursor.execute("SELECT Medium FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    updated_medium = cursor.fetchone()[0]
    assert updated_medium == new_medium

    cursor.execute("DELETE FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    gallery.connection.commit()

#Delete the artwork from the gallery
def test_delete_artwork(gallery):
    cursor = gallery.connection.cursor()
    test_artwork_id = 17

    artwork = Artwork(
        artwork_id=test_artwork_id,
        title="Test Title",
        description="Original description",
        creation_date=datetime(2022, 5, 10).date(),
        medium="Watercolor",
        image_url="https://test_art.jpg",
        artist_id=1
    )
    result = gallery.add_artwork(artwork)
    assert result is True

    cursor.execute("SELECT * FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    assert cursor.fetchone() is not None

    cursor.execute("DELETE FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    gallery.connection.commit()


#searching for artworks
def test_search_for_artwork(gallery):
    cursor = gallery.connection.cursor()
    test_artwork_id = 18
    test_title = "Artwork to Search"
    test_artist_id = 1
    test_medium = "Watercolor"
    cursor.execute("DELETE FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    gallery.connection.commit()
    artwork = Artwork(
        artwork_id=test_artwork_id,
        title=test_title,
        description="test description",
        creation_date=datetime(2023, 5, 11).date(),
        medium= test_medium,
        image_url="https://test_art.jpg",
        artist_id=test_artist_id
    )
    gallery.add_artwork(artwork)
    search_by = 'medium'
    keyword = "Watercolor"
    field = {
        'title': 'Title',
        'artist_id': 'Artist_ID',
        'medium': 'Medium'
    }
    column = field[search_by]

    if search_by == 'artist':
        if not keyword.strip().isdigit():
            print("Artist ID must be a number.")
            assert False
            return
        artist_id = int(keyword.strip())
        query = "SELECT * FROM Artwork WHERE Artist_ID = %s"
        cursor.execute(query, (artist_id,))
    else:
        like_pattern = f"%{keyword}%"
        query = f"SELECT * FROM Artwork WHERE {column} LIKE %s"
        cursor.execute(query, (like_pattern,))
    results = cursor.fetchall()

    assert any(row[0] == test_artwork_id for row in results)

    cursor.execute("DELETE FROM Artwork WHERE Artwork_ID = %s", (test_artwork_id,))
    gallery.connection.commit()


