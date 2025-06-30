from datetime import date
import re
from dao.IVirtualArtGallery import IVirtualArtGallery
from entity.artwork import Artwork
from entity.artist import Artist
from entity.gallery import Gallery
from entity.user import User
from util.DBConnUtil import DBConnection
from exception.exceptions import (InvalidIDException, InvalidArtistNameException,  # Artist
                                  InvalidDateException, InvalidWebsiteException,
                                  InvalidArtworkException, InvalidMediumTypeException,  # Artwork
                                  DuplicateArtworkException, ArtworkDoesNotExistException,
                                  InvalidGalleryNameException, InvalidOpeningHoursException,  # Gallery
                                  DuplicateGalleryException, GalleryAssignmentException, GalleryNotFoundException,
                                  InvalidUsernameException, InvalidPasswordException, InvalidEmailException,  # User
                                  DuplicateUserException, UserNotFoundException, FavoriteAlreadyExistsException,
                                  FavoriteNotFoundException)  # FavoriteAlreadyExistsException


class VirtualArtGalleryImp(IVirtualArtGallery):
    def __init__(self, connection=None):
        self.connection = connection or DBConnection.get_connection()

    """ Artist Implementation"""

    def validate_artist_fields(self, artist):
        if artist.name is not None and artist.name.strip() == "":
            raise InvalidArtistNameException("Artist Name cannot be empty")

        if artist.birth_date is not None and artist.birth_date > date.today():
            raise InvalidDateException("Birth date cannot be in the future")

        if artist.website is not None and not re.match(r"^https?://[^\s]+$", artist.website):
            raise InvalidWebsiteException("Website must be a valid URL")

    def add_artist(self, artist):
        if artist.artist_id is None:
            raise InvalidIDException("Artist ID is required")
        self.validate_artist_fields(artist)

        cursor = self.connection.cursor()
        cursor.execute("SELECT * from artist where Artist_ID = %s", (artist.artist_id,))
        if cursor.fetchone():
                raise InvalidIDException("Artist ID is already in use")

        query = """
                INSERT INTO Artist
                (Artist_ID, Name, Biography, Birth_Date, Nationality, Website, Contact_Information, IsActive)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
        cursor.execute(query, (artist.artist_id,artist.name,artist.biography or None,artist.birth_date or None,artist.nationality or None,
                               artist.website or None,artist.contact_information or None,artist.is_active))
        self.connection.commit()
        return cursor.rowcount > 0

    def update_artist(self, artist):
        cursor = None
        if artist.artist_id is None:
            raise InvalidIDException("Artist ID is required")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * from artist where Artist_ID = %s", (artist.artist_id,))
        existing = cursor.fetchone()
        if not existing:
            raise InvalidIDException("Artist with this ID does not exist")

        self.validate_artist_fields(artist)
        query = """
        UPDATE Artist SET
            Name = %s,
            Biography = %s,
            Birth_Date = %s,
            Nationality = %s,
            Website = %s,
            Contact_Information = %s
            WHERE Artist_ID = %s
        """
        cursor.execute(query, (artist.name or existing[1],artist.biography or existing[2],artist.birth_date or existing[3],artist.nationality or existing[4],
        artist.website or existing[5],artist.contact_information or existing[6],artist.artist_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_artist_by_id(self, artist_id):
        cursor = None
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from artist where Artist_ID = %s", (artist_id,))
        row = cursor.fetchone()
        if row:
            return Artist(
                artist_id = row[0],
                name = row[1],
                biography = row[2],
                birth_date = row[3],
                nationality = row[4],
                website = row[5],
                contact_information = row[6],
                is_active = row[7]
            )
        else:
            return None

    def remove_artist(self, artist_id):
        if artist_id is None:
            raise InvalidIDException("Artist ID is required for deletion")
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from artist where Artist_ID = %s", (artist_id,))
        if not cursor.fetchone():
            raise InvalidIDException("Artist with this ID does not exist")
        query="UPDATE Artist SET IsActive = FALSE WHERE Artist_ID = %s"
        cursor.execute(query, (artist_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def reactivate_artist(self, artist_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT IsActive from artist where Artist_ID = %s", (artist_id,))
        row = cursor.fetchone()
        if not row:
            return "not_found"
        isActive = row[0]
        if isActive:
            return "already_active"
        cursor.execute("UPDATE Artist SET IsActive = TRUE WHERE Artist_ID = %s", (artist_id,))
        self.connection.commit()
        return 'reactivated'

    """Artwork Implementation"""
    def validate_artwork_fields(self, artwork):
        if artwork.title is not None and artwork.title.strip() == "":
            raise InvalidArtworkException("Title is required")
        if artwork.description is not None and artwork.description == "":
            raise InvalidArtworkException("Description is required")
        if artwork.creation_date is not None and artwork.creation_date > date.today():
            raise InvalidDateException("Creation date cannot be null or in the future")
        if artwork.medium is not None and artwork.medium not in self.valid_mediums:
            raise InvalidMediumTypeException(f"Medium type cannot be none and it should be one of {', '.join(self.valid_mediums)}")
        if artwork.image_url is not None and not re.match(r"^https?://[^\s]+$", artwork.image_url):
            raise InvalidWebsiteException("Website must be a valid URL")

    valid_mediums = ["Oil on Canvas","Watercolor", "Acrylic", "Digital Art", "Sculpture", "Mixed Media"]
    def add_artwork(self, artwork):
        self.validate_artwork_fields(artwork)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from Artwork where Artwork_ID = %s", (artwork.artwork_id,))
        if cursor.fetchone():
            raise InvalidIDException("Artwork ID is already in use")

        cursor.execute("SELECT * FROM Artist WHERE Artist_ID = %s", (artwork.artist_id,))
        if not cursor.fetchone():
            print("Artist ID does not exist.")
            return False

        cursor.execute("SELECT * FROM Artwork WHERE Artist_ID = %s AND title = %s", (artwork.artist_id,artwork.title))
        if cursor.fetchone():
            raise DuplicateArtworkException(f"Artwork with title '{artwork.title}' already exists for this artist.")

        cursor.execute("""INSERT INTO Artwork (Artwork_id, Title, Description, Creation_Date, Artist_ID, Medium, Image_url)
        VALUES (%s, %s, %s, %s, %s, %s,%s)""",
        (artwork.artwork_id, artwork.title, artwork.description,
        artwork.creation_date, artwork.artist_id, artwork.medium, artwork.image_url))
        self.connection.commit()
        return cursor.rowcount > 0

    def update_artwork(self, artwork):
        if artwork.artwork_id is None:
            raise InvalidIDException("Artwork ID is required")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * from artwork where Artwork_ID = %s", (artwork.artwork_id,))
        existing = cursor.fetchone()
        if not existing:
            raise InvalidIDException("Artwork with this ID does not exist")

        self.validate_artwork_fields(artwork)
        query = """
        UPDATE Artwork SET
            Title = %s,
            Description = %s,
            Creation_date = %s,
            Medium = %s,
            Image_URL = %s,
            Artist_ID = %s
        WHERE Artwork_ID = %s
        """
        cursor.execute(query, (artwork.title or existing[1],
            artwork.description or existing[2],
            artwork.creation_date or existing[3],
            artwork.medium or existing[4],
            artwork.image_url or existing[5],
            artwork.artist_id or existing[6],
            artwork.artwork_id ))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_artwork_by_id(self, artwork_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from artwork where Artwork_ID = %s", (artwork_id,))
        row = cursor.fetchone()
        if row:
            return Artwork(
                artwork_id = row[0],
                title = row[1],
                description = row[2],
                creation_date = row[3],
                medium = row[4],
                image_url = row[5],
                artist_id = row[6]
            )
        else:
            raise ArtworkDoesNotExistException(f"Artwork with ID '{artwork_id}' does not exist")

    def remove_artwork(self, artwork_id):
        cursor = None
        if artwork_id is None:
            raise InvalidIDException("Artwork ID is required")
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from artwork where Artwork_ID = %s", (artwork_id,))
        if not cursor.fetchone():
            raise InvalidIDException("Artwork with this ID does not exist")
        cursor.execute("DELETE FROM Artwork WHERE Artwork_ID = %s", (artwork_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def search_artworks(self, keyword, search_by):
        cursor = self.connection.cursor()
        field_map = {
            'title': 'Title',
            'artist_id': 'Artist_ID',
            'medium': 'Medium'
        }
        if search_by not in field_map:
            raise ValueError("Invalid search criteria. Choose from: title, medium, artist_id")

        column = field_map[search_by]
        if search_by == 'artist':
            if not keyword.strip().isdigit():
                print("Artist ID must be a number.")
                return []
            artist_id = int(keyword.strip())
            query = "SELECT * FROM Artwork WHERE Artist_ID = %s"
            cursor.execute(query, (artist_id,))
        else:
            like_pattern = f"%{keyword}%"
            query = f"SELECT * FROM Artwork WHERE {column} LIKE %s"
            cursor.execute(query, (like_pattern,))
        rows = cursor.fetchall()
        artworks = []
        for row in rows:
            artworks.append(Artwork(
                artwork_id = row[0],
                title = row[1],
                description = row[2],
                creation_date = row[3],
                medium = row[4],
                image_url = row[5],
                artist_id = row[6]
            ))
        return artworks

    """ Gallery Implementation """

    def validate_gallery_fields(self, gallery):
        if gallery.gallery_id is None or str(gallery.gallery_id).strip() == "":
            raise InvalidIDException("Gallery ID is required")
        if gallery.name is None or gallery.name.strip() == "":
            raise InvalidGalleryNameException("Gallery Name is required")
        if gallery.curator is None or str(gallery.curator).strip() == "":
            raise GalleryAssignmentException("Curator ID cannot be empty")
        if gallery.opening_hours:
            hours = gallery.opening_hours.strip()
            if hours.lower() == "closed":
                return
            if "-" not in hours or not ("AM" in hours.upper() or "PM" in hours.upper()):
                raise InvalidOpeningHoursException("Invalid format for Opening Hours")
            parts = hours.split("-")
            if len(parts) != 2:
                raise InvalidOpeningHoursException(
                    "Opening Hours format should be 'hh:mm AM/PM - hh:mm AM/PM' or 'Closed'")

    def add_gallery(self,gallery):
        self.validate_gallery_fields(gallery)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Gallery where Gallery_ID = %s", (gallery.gallery_id,))
        if cursor.fetchone():
            raise InvalidIDException("Gallery with this ID already exists")
        cursor.execute("SELECT * FROM Artist WHERE Artist_ID = %s", (gallery.curator,))
        if not cursor.fetchone():
            raise InvalidIDException(f"Curator with ID {gallery.curator} does not exist")
        cursor.execute("SELECT * FROM Gallery where Gallery_ID = %s AND Name = %s", (gallery.gallery_id,gallery.name,))
        if cursor.fetchone():
            raise DuplicateGalleryException(f"Gallery with this name '{gallery.name}' already exists")
        cursor.execute("""INSERT INTO Gallery
        (Gallery_ID, Name,Description, Location, Curator, Opening_Hours)
         VALUES (%s, %s, %s, %s, %s, %s)""",
         (gallery.gallery_id,gallery.name,gallery.description or None,gallery.location or None,gallery.curator or None,gallery.opening_hours or None))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_gallery_by_id(self, gallery_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Gallery WHERE Gallery_ID = %s", (gallery_id,))
        row = cursor.fetchone()
        if row:
            return Gallery(
                gallery_id=row[0],
                name=row[1],
                description=row[2],
                location=row[3],
                curator=row[4],
                opening_hours=row[5]
            )
        else:
            return None

    def update_gallery(self, gallery):
        if gallery.gallery_id is None or str(gallery.gallery_id).strip() == "":
            raise InvalidIDException("Gallery ID is required")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Gallery WHERE Gallery_ID = %s", (gallery.gallery_id,))
        existing = cursor.fetchone()
        if not existing:
            raise GalleryNotFoundException("Gallery with this ID does not exist")

        if gallery.curator:
            cursor.execute("SELECT * FROM Artist WHERE Artist_ID = %s", (gallery.curator,))
            if not cursor.fetchone():
                raise InvalidIDException(f"Curator with ID {gallery.curator} does not exist")

        self.validate_gallery_fields(gallery)

        query = """
            UPDATE Gallery SET
                Name = %s,
                Description = %s,
                Location = %s,
                Curator = %s,
                Opening_Hours = %s
            WHERE Gallery_ID = %s
        """
        cursor.execute(query, (
            gallery.name or existing[1],
            gallery.description or existing[2],
            gallery.location or existing[3],
            gallery.curator or existing[4],
            gallery.opening_hours or existing[5],
            gallery.gallery_id
        ))
        self.connection.commit()
        return cursor.rowcount > 0

    def remove_gallery(self, gallery_id):
        if gallery_id is None or str(gallery_id).strip() == "":
            raise InvalidIDException("Gallery ID is required for deletion")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Gallery WHERE Gallery_ID = %s", (gallery_id,))
        if not cursor.fetchone():
            raise GalleryNotFoundException("Gallery with this ID does not exist")

        query = "DELETE FROM Gallery WHERE Gallery_ID = %s"
        cursor.execute(query, (gallery_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def search_gallery(self, keyword, search_by):
        cursor = self.connection.cursor()
        field_map = {
            'name': 'Name',
            'location': 'Location',
            'curator': 'Curator'
        }
        if search_by not in field_map:
            raise ValueError("Invalid search criteria. Choose from: name, location, curator")

        column = field_map[search_by]

        if search_by == 'curator':
            if not keyword.strip().isdigit():
                print("Curator ID must be a number.")
                return []
            query = "SELECT * FROM Gallery WHERE Curator = %s"
            cursor.execute(query, (int(keyword.strip()),))
        else:
            like_pattern = f"%{keyword}%"
            query = f"SELECT * FROM Gallery WHERE {column} LIKE %s"
            cursor.execute(query, (like_pattern,))

        rows = cursor.fetchall()
        galleries = []
        for row in rows:
            galleries.append(Gallery(
                gallery_id=row[0],
                name=row[1],
                description=row[2],
                location=row[3],
                curator=row[4],
                opening_hours=row[5]
            ))
        return galleries

    """ User Implementation """
    def validate_user_fields(self, user):
        if user.user_id is None or str(user.user_id).strip() == "":
            raise InvalidIDException("User ID is required")
        if user.username is None or user.username.strip() == "":
            raise InvalidUsernameException("Username is required")
        if user.password is None or user.password.strip() == "":
            raise InvalidPasswordException("Password is required")
        if user.email:
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, user.email):
                raise InvalidEmailException("Invalid email format")
        if user.date_of_birth and user.date_of_birth > date.today():
            raise InvalidIDException("Date of birth cannot be in the future")
        if user.profile_picture is not None and not re.match(r"^https?://[^\s]+$", user.profile_picture):
            raise InvalidWebsiteException("Profile Picture must be a valid URL")

    def add_user(self, user):
        self.validate_user_fields(user)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM User WHERE User_ID = %s", (user.user_id,))
        if cursor.fetchone():
            raise InvalidIDException("User ID already exists")

        cursor.execute("SELECT * FROM User WHERE Username = %s OR Email = %s", (user.username, user.email))
        if cursor.fetchone():
            raise DuplicateUserException("Username or Email already in use")

        cursor.execute("""
            INSERT INTO User
            (User_ID, Username, Password, Email, First_Name, Last_Name, Date_of_Birth, Profile_Picture, User_is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user.user_id,
            user.username,
            user.password,
            user.email or None,
            user.first_name or None,
            user.last_name or None,
            user.date_of_birth or None,
            user.profile_picture or None,
            user.user_is_active
        ))

        self.connection.commit()
        return cursor.rowcount > 0

    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM User WHERE User_ID = %s", (user_id,))
        row = cursor.fetchone()

        if row:
            return User(
                user_id=row[0],
                username=row[1],
                password=row[2],
                email=row[3],
                first_name=row[4],
                last_name=row[5],
                date_of_birth=row[6],
                profile_picture=row[7],
                user_is_active=row[8]
            )
        else:
            return None

    def update_user(self, user):
        if user.user_id is None:
            raise InvalidIDException("User ID is required")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM User WHERE User_ID = %s", (user.user_id,))
        existing = cursor.fetchone()

        if not existing:
            raise InvalidIDException("User with this ID does not exist")

        self.validate_user_fields(user)

        query = """
        UPDATE User SET
            Username = %s,
            Password = %s,
            Email = %s,
            First_Name = %s,
            Last_Name = %s,
            Date_of_Birth = %s,
            Profile_Picture = %s,
            User_is_active = %s
        WHERE User_ID = %s
        """

        cursor.execute(query, (
            user.username or existing[1],
            user.password or existing[2],
            user.email or existing[3],
            user.first_name or existing[4],
            user.last_name or existing[5],
            user.date_of_birth or existing[6],
            user.profile_picture or existing[7],
            user.user_is_active if user.user_is_active is not None else existing[8],
            user.user_id
        ))
        self.connection.commit()
        return cursor.rowcount > 0

    def remove_user(self, user_id):
        if user_id is None:
            raise InvalidIDException("User ID is required for deletion")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM User WHERE User_ID = %s", (user_id,))
        if not cursor.fetchone():
            raise InvalidIDException("User with this ID does not exist")

        query = "UPDATE User SET User_is_active = FALSE WHERE User_ID = %s"
        cursor.execute(query, (user_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def reactivate_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT User_is_active FROM User WHERE User_ID = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            return "not_found"
        is_active = row[0]
        if is_active:
            return "already_active"

        cursor.execute("UPDATE User SET User_is_active = TRUE WHERE User_ID = %s", (user_id,))
        self.connection.commit()
        return "reactivated"

    """ User Favorite Implementation """

    def add_artwork_to_favorite(self, user_id, artwork_id):
        if user_id is None or artwork_id is None:
            raise InvalidIDException("User ID and Artwork ID are required")
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM User WHERE User_ID = %s", (user_id,))
        if not cursor.fetchone():
            raise UserNotFoundException("User with this ID does not exist")

        cursor.execute("SELECT * FROM Artwork WHERE Artwork_ID = %s", (artwork_id,))
        if not cursor.fetchone():
            raise ArtworkDoesNotExistException("Artwork with this ID does not exist")

        cursor.execute("SELECT * FROM User_Favorite_Artwork WHERE User_ID = %s AND Artwork_ID = %s",
                       (user_id, artwork_id))
        if cursor.fetchone():
            raise FavoriteAlreadyExistsException("Favorite Already Exists")

        cursor.execute("INSERT INTO User_Favorite_Artwork (User_ID, Artwork_ID) VALUES (%s, %s)", (user_id, artwork_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def remove_artwork_from_favorite(self, user_id, artwork_id):
        if user_id is None or artwork_id is None:
            raise InvalidIDException("User ID and Artwork ID are required")

        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM User_Favorite_Artwork WHERE User_ID = %s AND Artwork_ID = %s",
                       (user_id, artwork_id))
        if not cursor.fetchone():
            raise FavoriteNotFoundException("Favorite Artwork with this ID does not exist")

        cursor.execute("DELETE FROM User_Favorite_Artwork WHERE User_ID = %s AND Artwork_ID = %s",
                       (user_id, artwork_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_user_favorite_artworks(self, user_id):
        if user_id is None:
            raise InvalidIDException("User ID is required")
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM User WHERE User_ID = %s", (user_id,))
        if not cursor.fetchone():
            raise InvalidIDException("User with this ID does not exist")

        query = """
        SELECT a.Artwork_ID, a.Title, a.Description, a.Creation_date, a.Medium, a.Image_URL, a.Artist_ID
        FROM Artwork a
        JOIN User_Favorite_Artwork ufa ON a.Artwork_ID = ufa.Artwork_ID
        WHERE ufa.User_ID = %s
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        if not rows:
            return False

        favorite_artworks = []
        for row in rows:
            favorite_artworks.append(Artwork(
                artwork_id=row[0],
                title=row[1],
                description=row[2],
                creation_date=row[3],
                medium=row[4],
                image_url=row[5],
                artist_id=row[6]
            ))
        return favorite_artworks

    """ Artwork Gallery Implementation """

    def add_artwork_to_gallery(self, artwork_id, gallery_id):
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM Artwork WHERE Artwork_ID = %s", (artwork_id,))
        if not cursor.fetchone():
            raise InvalidIDException("Artwork with this ID does not exist")

        cursor.execute("SELECT * FROM Gallery WHERE Gallery_ID = %s", (gallery_id,))
        if not cursor.fetchone():
            raise GalleryNotFoundException("Gallery with this ID does not exist")

        cursor.execute("SELECT * FROM Artwork_Gallery WHERE Artwork_ID = %s AND Gallery_ID = %s",
                       (artwork_id, gallery_id))
        if cursor.fetchone():
            raise DuplicateArtworkException("This artwork is already assigned to the gallery")

        cursor.execute("INSERT INTO Artwork_Gallery (Artwork_ID, Gallery_ID) VALUES (%s, %s)", (artwork_id, gallery_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def remove_artwork_from_gallery(self, artwork_id, gallery_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Artwork_Gallery WHERE Artwork_ID = %s AND Gallery_ID = %s",
                       (artwork_id, gallery_id))
        if not cursor.fetchone():
            raise ArtworkDoesNotExistException("Artwork not found in this gallery")

        cursor.execute("DELETE FROM Artwork_Gallery WHERE Artwork_ID = %s AND Gallery_ID = %s",
                       (artwork_id, gallery_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_artworks_by_gallery(self, gallery_id):
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM Gallery WHERE Gallery_ID = %s", (gallery_id,))
        if not cursor.fetchone():
            raise GalleryNotFoundException("Gallery with this ID does not exist")

        cursor.execute("""
            SELECT a.Artwork_ID, a.Title, a.Description, a.Creation_Date, a.Medium, a.Image_URL, a.Artist_ID
            FROM Artwork a
            JOIN Artwork_Gallery ag ON a.Artwork_ID = ag.Artwork_ID
            WHERE ag.Gallery_ID = %s
        """, (gallery_id,))
        rows = cursor.fetchall()

        if not rows:
            return False

        artworks = []
        for row in rows:
            artworks.append(Artwork(
                artwork_id=row[0],
                title=row[1],
                description=row[2],
                creation_date=row[3],
                medium=row[4],
                image_url=row[5],
                artist_id=row[6]
            ))
        return artworks






















