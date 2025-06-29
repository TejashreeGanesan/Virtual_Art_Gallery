from abc import ABC, abstractmethod

class IVirtualArtGallery(ABC):
    """ Artist Interface """
    @abstractmethod
    def add_artist(self, artist):
        pass

    @abstractmethod
    def update_artist(self, artist):
        pass

    @abstractmethod
    def get_artist_by_id(self, artist_id):
        pass
    @abstractmethod
    def remove_artist(self, artist):
        pass

    @abstractmethod
    def reactivate_artist(self, artist):
        pass

    """ Artwork Interface """
    @abstractmethod
    def add_artwork(self, artwork):
        pass

    @abstractmethod
    def update_artwork(self, artwork):
        pass

    @abstractmethod
    def get_artwork_by_id(self, artwork_id):
        pass

    @abstractmethod
    def remove_artwork(self, artwork):
        pass

    @abstractmethod
    def search_artworks(self, artwork):
        pass

    """ Gallery Interface """
    @abstractmethod
    def add_gallery(self,gallery):
        pass

    @abstractmethod
    def update_gallery(self, gallery):
        pass
    
    @abstractmethod
    def get_gallery_by_id(self, gallery_id):
        pass

    @abstractmethod
    def remove_gallery(self, gallery):
        pass
  
    @abstractmethod
    def search_gallery(self, gallery):
        pass

    """ User Interface """
    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def update_user(self, user):
        pass
    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def remove_user(self, user):
        pass

    @abstractmethod
    def reactivate_user(self, user):
        pass

    """ User Favorites Interface"""
    @abstractmethod
    def add_artwork_to_favorite(self, user_id, artwork_id):
        pass
    def remove_artwork_from_favorite(self, user_id, artwork_id):
        pass
    def get_user_favorite_artworks(self, favorite_id):
        pass

    """ Artwork Gallery """

    @abstractmethod
    def add_artwork_to_gallery(self, artwork_id, gallery_id):
        pass

    @abstractmethod
    def remove_artwork_from_gallery(self, artwork_id, gallery_id):
        pass

    @abstractmethod
    def get_artworks_by_gallery(self, gallery_id):
        pass

