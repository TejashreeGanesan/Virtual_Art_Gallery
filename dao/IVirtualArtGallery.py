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

    '''
    @abstractmethod
    def get_artwork_by_id(self, artwork_id):
        pass

    @abstractmethod
    def get_artwork_by_name(self, artwork_name):
        pass
'''
