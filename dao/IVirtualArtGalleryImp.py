from datetime import date
import re
import mysql.connector
from dao.IVirtualArtGallery import IVirtualArtGallery
from entity.artwork import Artwork
from entity.artist import Artist
from util.DBConnUtil import DBConnection
from exception.exceptions import (InvalidIDException, InvalidArtistNameException, #Artist
                                  InvalidDateException, InvalidWebsiteException,
                                  InvalidArtworkException, InvalidMediumTypeException, #Artwork
                                  DuplicateArtworkException)

class VirtualArtGalleryImp(IVirtualArtGallery):
    def __init__(self):
        self.connection = DBConnection.get_connection()

    """ Artist Implementation"""

    def validate_artist_fields(self, artist):
        if artist.name is not None and artist.name.strip() == "":
            raise InvalidArtistNameException("Artist Name cannot be empty")

        if artist.birth_date is not None and artist.birth_date > date.today():
            raise InvalidDateException("Birth date cannot be in the future")

        if artist.website is not None and not re.match(r"^https?://[^\s]+$", artist.website):
            raise InvalidWebsiteException("Website must be a valid URL")

    def add_artist(self, artist):
        cursor = None
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
        cursor = None
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
        cursor = None
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
        cursor = None
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
        cursor = None
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
        cursor = None
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
            return None

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













