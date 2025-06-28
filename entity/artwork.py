class Artwork:
    def __init__(self, artwork_id = None, title = None, description= None, creation_date = None,
                 medium=None,image_url = None, artist_id = None):
        self.__artwork_id = artwork_id
        self.__title = title
        self.__description = description
        self.__creation_date = creation_date
        self.__medium = medium
        self.__image_url = image_url
        self.__artist_id = artist_id

    @property
    def artwork_id(self):
        return self.__artwork_id
    @artwork_id.setter
    def artwork_id(self, artwork_id):
        self.__artwork_id = artwork_id

    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def creation_date(self):
        return self.__creation_date
    @creation_date.setter
    def creation_date(self, creation_date):
        self.__creation_date = creation_date

    @property
    def medium(self):
        return self.__medium
    @medium.setter
    def medium(self, medium):
        self.__medium = medium

    @property
    def image_url(self):
        return self.__image_url
    @image_url.setter
    def image_url(self, image_url):
        self.__image_url = image_url

    @property
    def artist_id(self):
        return self.__artist_id
    @artist_id.setter
    def artist_id(self, artist_id):
        self.__artist_id = artist_id


