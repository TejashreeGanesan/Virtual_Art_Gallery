class Gallery:
    def __init__(self, gallery_id = None, name= None, description= None, location= None, curator= None, opening_hours= None):
        self.__gallery_id = gallery_id
        self.__name = name
        self.__description = description
        self.__location = location
        self.__curator = curator
        self.__opening_hours = opening_hours

    @property
    def gallery_id(self):
        return self.__gallery_id
    @gallery_id.setter
    def gallery_id(self, gallery_id):
        self.__gallery_id = gallery_id

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def location(self):
        return self.__location
    @location.setter
    def location(self, location):
        self.__location = location

    @property
    def curator(self):
        return self.__curator
    @curator.setter
    def curator(self, curator):
        self.__curator = curator

    @property
    def opening_hours(self):
        return self.__opening_hours
    @opening_hours.setter
    def opening_hours(self, opening_hours):
        self.__opening_hours = opening_hours

