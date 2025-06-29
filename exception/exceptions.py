
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

class ArtworkDoesNotExistException(Exception):
    def __init__(self, message = "Artwork Does Not Exist"):
        super().__init__(message)

""" Gallery Exceptions """

class DuplicateGalleryException(Exception):
    def __init__(self, message = "Gallery Title already exists"):
        super().__init__(message)

class InvalidGalleryNameException(Exception):
    def __init__(self, message = "Gallery Name cannot be empty or NULL"):
        super().__init__(message)

class GalleryNotFoundException(Exception):
    def __init__(self, message = "Gallery with this ID Does Not Exist"):
        super().__init__(message)

class GalleryAssignmentException(Exception):
    def __init__(self, message="Failed to assign artwork to gallery."):
        super().__init__(message)

class InvalidOpeningHoursException(Exception):
    def __init__(self, message="Opening hours must be in format 'hh:mm AM/PM - hh:mm AM/PM' or 'Closed'."):
        super().__init__(message)

""" User Exceptions """
class DuplicateUserException(Exception):
    def __init__(self, message = "Username already exists"):
        super().__init__(message)

class InvalidUsernameException(Exception):
    def __init__(self, message = "Username cannot be empty or NULL"):
        super().__init__(message)

class InvalidPasswordException(Exception):
    def __init__(self, message = "Password cannot be empty or NULL"):
        super().__init__(message)

class InvalidEmailException(Exception):
    def __init__(self, message = "Email cannot be empty or NULL"):
        super().__init__(message)

class UserNotFoundException(Exception):
    def __init__(self, message="User with the given ID does not exist"):
        super().__init__(message)

""" Common Exceptions """
class InvalidWebsiteException(Exception):
    def __init__(self, message = "Website must be a valid URL (e.g., https://example.com) "):
        super().__init__(message)

class InvalidDateException(Exception):
    def __init__(self, message= "Date cannot be in future"):
        super().__init__(message)

class InvalidIDException(Exception):
    def __init__(self, message = "ID cannot be NULL or Already Exists"):
        super().__init__(message)

""" User Favorite Exceptions """
class FavoriteAlreadyExistsException(Exception):
    def __init__(self, message="This artwork is already in the user's favorites"):
        super().__init__(message)

class FavoriteNotFoundException(Exception):
    def __init__(self, message="This artwork is not in the user's favorites"):
        super().__init__(message)

