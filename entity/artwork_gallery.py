class ArtworkGallery:

    def __init__(self, artwork_id: int = None, gallery_id: int = None):
        self.__artwork_id = artwork_id
        self.__gallery_id = gallery_id

    @property
    def artwork_id(self) -> int:
        return self.__artwork_id

    @artwork_id.setter
    def artwork_id(self, artwork_id: int):
        self.__artwork_id = artwork_id

    @property
    def gallery_id(self) -> int:
        return self.__gallery_id

    @gallery_id.setter
    def gallery_id(self, gallery_id: int):
        self.__gallery_id = gallery_id
