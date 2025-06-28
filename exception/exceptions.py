
""" Artist Exceptions """
class InvalidArtistNameException(Exception):
    def __init__(self, message = "Artist Name cannot be empty or NULL"):
        super().__init__(message)

""" Artwork Exceptions """
class InvalidArtworkException(Exception):
    def __init__(self, message = "Artwork Title/ Description / Creation Date cannot be Null"):
        super().__init__(message)

class InvalidMediumTypeException(Exception):
    def __init__(self, message   = "Medium Type should be from the medium types"):
        super().__init__(message)

class DuplicateArtworkException(Exception):
    def __init__(self, message = "Artwork Title already exists"):
        super().__init__(message)

""" Common Exceptions """
class InvalidWebsiteException(Exception):
    def __init__(self, message = "Website must be a valid URL (e.g., https://example.com) "):
        super().__init__(message)

class InvalidDateException(Exception):
    def __init__(self, message= "Date cannot be in future"):
        super().__init__(message)

class InvalidIDException(Exception):
    def __init__(self, message = "Artwork ID cannot be NULL or Already Exists"):
        super().__init__(message)

