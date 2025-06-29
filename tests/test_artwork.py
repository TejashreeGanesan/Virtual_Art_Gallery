import pytest
from entity.artwork import Artwork
from dao.IVirtualArtGalleryImp import VirtualArtGalleryImp


@pytest.fixture
def artwork_service(mock_connection):
    return VirtualArtGalleryImp(mock_connection)

def test_add_artwork_success(VirtualArtGalleryImp):
    artwork = Artwork(artwork_id=101, title="Sunset", description="Sunset with beautiful view", creation_date="2020-01-01", medium="Oil on Canvas", image_url="https://sunset.com", artist_id=1)
    result = VirtualArtGalleryImp.add_artwork(artwork)
    assert result is True

def test_update_artwork_success(VirtualArtGalleryImp):
    artwork = Artwork(artwork_id=101, title="Sunset 2", description="Colorful oil painted", creation_date="2020-01-01", medium="Oil on Canvas", image_url="https://sunset.com", artist_id=1)
    result = VirtualArtGalleryImp.update_artwork(artwork)
    assert result is True

def test_remove_artwork(VirtualArtGalleryImp):
    result = VirtualArtGalleryImp.remove_artwork(101)
    assert result is True

def test_search_artwork_by_title(VirtualArtGalleryImp):
    result = VirtualArtGalleryImp.search_artworks("Sunset", "title")
    assert isinstance(result, list)

