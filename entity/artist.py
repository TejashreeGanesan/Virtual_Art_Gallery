class Artist:
    def __init__(self, artist_id = None, name=None, biography=None, birth_date = None, nationality = None, website = None, contact_information = None, is_active = None):
        self.__artist_id = artist_id
        self.__name = name
        self.__biography = biography
        self.__birth_date = birth_date
        self.__nationality = nationality
        self.__website = website
        self.__contact_information = contact_information
        self.__is_active = is_active

    @property
    def artist_id(self):
        return self.__artist_id
    @artist_id.setter
    def artist_id(self, artist_id):
        self.__artist_id = artist_id

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def biography(self):
        return self.__biography
    @biography.setter
    def biography(self, biography):
        self.__biography = biography

    @property
    def birth_date(self):
        return self.__birth_date
    @birth_date.setter
    def birth_date(self, birth_date):
        self.__birth_date = birth_date

    @property
    def nationality(self):
        return self.__nationality
    @nationality.setter
    def nationality(self, nationality):
        self.__nationality = nationality

    @property
    def website(self):
        return self.__website
    @website.setter
    def website(self, website):
        self.__website = website

    @property
    def contact_information(self):
        return self.__contact_information
    @contact_information.setter
    def contact_information(self, contact_information):
        self.__contact_information = contact_information

    @property
    def is_active(self):
        return self.__is_active
    @is_active.setter
    def is_active(self, is_active):
        self.__is_active = is_active