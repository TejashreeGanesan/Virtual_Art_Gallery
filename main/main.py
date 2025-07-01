from dao.IVirtualArtGalleryImp import VirtualArtGalleryImp
from entity.artist import Artist
from datetime import datetime
from entity.artwork import Artwork
from entity.gallery import Gallery
from entity.user import User
from exception.exceptions import (InvalidIDException, InvalidArtistNameException, InvalidDateException,
                                  InvalidWebsiteException, InvalidArtworkException, InvalidMediumTypeException,
                                  DuplicateArtworkException, DuplicateGalleryException, InvalidGalleryNameException,
                                  GalleryNotFoundException, GalleryAssignmentException, InvalidOpeningHoursException,
                                  DuplicateUserException, InvalidUsernameException, InvalidPasswordException,
                                  InvalidEmailException, UserNotFoundException, FavoriteAlreadyExistsException,
                                  ArtworkDoesNotExistException, FavoriteNotFoundException)

def clean_input(value):
    return value.strip() if value.strip() != "" else None


class MainModule:
    @staticmethod
    def artist_menu(service):
        while True:
            print("\n ------- Artist Menu -------")
            print("\n 1. Add Artist")
            print("\n 2. Update Artist")
            print("\n 3. Delete Artist")
            print("\n 4. Get Artist By ID")
            print("\n 5. Reactivate Artist")
            print("\n 0. Exit")
            choice = input("Enter you choice:")

            try:
                if choice == "1":
                    artist_id = int(input("Enter Artist ID: "))
                    name = input("Enter Artist Name: ")
                    biography = clean_input(input("Enter Biography: "))
                    birth_date_input = clean_input(input("Enter Birth Date (YYYY-MM-DD): "))
                    birth_date = datetime.strptime(birth_date_input, "%Y-%m-%d").date() if birth_date_input else None
                    nationality = clean_input(input("Enter Nationality: "))
                    website = clean_input(input("Enter Website: "))
                    contact_information = clean_input(input("Enter Contact Information: "))

                    artist = Artist(artist_id=artist_id,name=name,biography=biography or None,birth_date=birth_date or None,nationality=nationality or None,
                                    website=website or None, contact_information=contact_information or None,is_active=True)

                    if service.add_artist(artist):
                        print("Artist Added Successfully!")
                    else:
                        print("Failed to add artist")

                elif choice == "2":
                    artist_id = int(input("Enter Artist ID to update: "))
                    existing_artist = service.get_artist_by_id(artist_id)
                    if not existing_artist:
                        raise InvalidIDException("Artist with this ID does not exist")

                    print("Please leave the field empty to retain existing value")
                    name = input(f"Enter New Artist Name [{existing_artist.name}]: ") or existing_artist.name
                    biography = clean_input(input(f"Enter New Biography [{existing_artist.biography}]: ")) or existing_artist.biography
                    birth_date_input = clean_input(input(f"Enter New Birth Date (YYYY-MM-DD) [{existing_artist.birth_date}]: "))

                    if birth_date_input:
                        birth_date = datetime.strptime(birth_date_input, "%Y-%m-%d").date()
                    else:
                        birth_date = existing_artist.birth_date

                    nationality = clean_input(input(f"Enter New Nationality: [{existing_artist.nationality}]: ")) or existing_artist.nationality
                    website = clean_input(input(f"Enter Website: [{existing_artist.website}]: ")) or existing_artist.website
                    contact_information = clean_input(input(f"Enter Contact Information: [{existing_artist.contact_information}]: ")) or existing_artist.contact_information

                    updated_artist = Artist(artist_id=artist_id,name=name,biography=biography,birth_date=birth_date,nationality=nationality,
                        website=website,contact_information=contact_information,is_active=True)
                    if service.update_artist(updated_artist):
                        print("Artist Updated Successfully")

                elif choice == "3":
                    artist_id = int(input("Enter Artist ID to delete: "))
                    confirm = input(f"Are you sure you want to delete Artist {artist_id}? [y/N] ")
                    if confirm.lower() == "y":
                        if service.remove_artist(artist_id):
                            print("Artist deleted successfully")
                        else:
                            print("Failed to delete artist")
                    else:
                        print("Attempt to Delete the Artist has been cancelled")

                elif choice == "4":
                    artist_id = int(input("Enter Artist ID to fetch: "))
                    artist = service.get_artist_by_id(artist_id)
                    if artist:
                        print("\n--------- Artist Details ---------")
                        print(f"ID: {artist.artist_id}")
                        print(f"Name: {artist.name}")
                        print(f"Biography: {artist.biography or 'N/A'}")
                        print(f"Nationality: {artist.nationality or 'N/A'}")
                        print(f"Website: {artist.website or 'N/A'}")
                        print(f"Contact Information: {artist.contact_information or 'N/A'}")
                        print(f"Active Status: {'Active' if artist.is_active else 'Inactive'}")
                    else:
                        raise InvalidIDException("Artist with this ID does not exist")

                elif choice == "5":
                    artist_id = int(input("Enter Artist ID to reactivate: "))
                    result = service.reactivate_artist(artist_id)
                    if result == 'reactivated':
                        print("Artist account Reactivated Successfully")
                    elif result == 'already_active':
                        print("Artist account Already Active, No Action Needed")
                    elif result == 'not_found':
                        raise InvalidIDException("Artist with this ID does not exist")

                elif choice == "0":
                    print("Exiting... Thank You!")
                    break
                else:
                    print("Invalid Choice. Try again.")

            except (InvalidIDException, InvalidArtistNameException, InvalidDateException, InvalidWebsiteException) as e:
                print(f"Validation Error: {e}")
            except ValueError:
                print("Invalid input type. Please enter numeric value.")
            except Exception as e:
                print(f"Unexpected Error: {e}")

    @staticmethod
    def artwork_menu(service):
        while True:
            print("\n ------- Artwork Menu -------")
            print("\n 1. Add Artwork")
            print("\n 2. Update Artwork")
            print("\n 3. Delete Artwork")
            print("\n 4. Get Artwork By ID")
            print("\n 5. Search Artwork")
            print("\n 0. Exit")
            choice = input("Enter you choice:")
            try:
                if choice == "1":
                    artwork_id = clean_input(input("Enter Artwork ID: "))
                    artist_id = clean_input(input("Enter Artist ID: "))
                    title = clean_input(input("Enter Artwork Title: "))
                    description = clean_input(input("Enter Artwork Description: "))
                    creation_date_input = clean_input(input("Enter Creation Date (YYYY-MM-DD): "))
                    creation_date = datetime.strptime(creation_date_input, "%Y-%m-%d").date() if creation_date_input else None
                    medium = clean_input(input("Enter Medium Type: "))
                    image_url=clean_input(input("Enter Image URL: "))

                    artwork = Artwork(artwork_id = artwork_id, title = title, description = description, creation_date = creation_date, medium = medium, image_url = image_url or None, artist_id = artist_id)
                    success = service.add_artwork(artwork)
                    if success:
                        print("Artwork Added Successfully")
                    else:
                        print("Failed to add Artwork")

                elif choice == "2":
                    artwork_id = int(input("Enter Artwork ID to update: "))
                    existing_artwork = service.get_artwork_by_id(artwork_id)
                    if not existing_artwork:
                        raise InvalidIDException("Artwork with this ID does not exist")

                    print("Please leave the field empty to retain existing value")
                    title = input(f"Enter New Title [{existing_artwork.title}]: ") or existing_artwork.title
                    description = clean_input(
                        input(f"Enter New Description [{existing_artwork.description}]: ")) or existing_artwork.description
                    creation_date_input = clean_input(
                        input(f"Enter New Creation Date (YYYY-MM-DD) [{existing_artwork.creation_date}]: "))

                    if creation_date_input:
                        creation_date = datetime.strptime(creation_date_input, "%Y-%m-%d").date()
                    else:
                        creation_date = existing_artwork.creation_date

                    medium = clean_input(input(
                        f"Enter New Medium: [{existing_artwork.medium}]: ")) or existing_artwork.medium
                    image_url = clean_input(
                        input(f"Enter Image URL: [{existing_artwork.image_url}]: ")) or existing_artwork.image_url
                    artist_id = clean_input(input(
                        f"Enter Artist ID: [{existing_artwork.artist_id}]: ")) or existing_artwork.artist_id

                    updated_artwork = Artwork(artwork_id=artwork_id, title = title, description = description, creation_date=creation_date,
                                              medium = medium, image_url = image_url or None, artist_id = artist_id)

                    if service.update_artwork(updated_artwork):
                        print("Artwork Updated Successfully")

                elif choice == "3":
                    artwork_id = int(input("Enter Artwork ID to delete: "))
                    confirm = input(f"Are you sure you want to delete Artwork {artwork_id}? [y/N] ")
                    if confirm.lower() == "y":
                        if service.remove_artwork(artwork_id):
                            print("Artwork deleted successfully")
                        else:
                            print("Failed to delete artwork")
                    else:
                        print("Attempt to Delete the Artwork has been cancelled")

                elif choice == "4":
                    artwork_id = int(input("Enter Artwork ID to fetch: "))
                    artwork = service.get_artwork_by_id(artwork_id)
                    if artwork:
                        print("\n--------- Artist Details ---------")
                        print(f"ID: {artwork.artwork_id}")
                        print(f"Title: {artwork.title}")
                        print(f"Description: {artwork.description or 'N/A'}")
                        print(f"Creation Date: {artwork.creation_date or 'N/A'}")
                        print(f"Medium {artwork.medium or 'N/A'}")
                        print(f"Image URL: {artwork.image_url or 'N/A'}")
                        print(f"Artist ID: {artwork.artist_id}")
                    else:
                        raise InvalidIDException("Artwork with this ID does not exist")
                elif choice == "5":
                    print("\n Search Artworks By:")
                    print("1. Title")
                    print("2. Artist ID")
                    print("3. Medium")
                    search_choice = input("Enter your choice (1/2/3): ")

                    if search_choice == "1":
                        search_by = "title"
                    elif search_choice == "2":
                        search_by = "artist_id"
                    elif search_choice == "3":
                        search_by = "medium"
                    else:
                        print("Invalid choice. Please select valid option")
                        continue

                    keyword = input(f"Enter keyword to search in {search_by.capitalize()}: ")
                    artworks = service.search_artworks(keyword, search_by)
                    if artworks:
                        print("\n--------- Matching Artworks ---------")
                        for art in artworks:
                            print(f"\nID: {art.artwork_id}")
                            print(f"Title: {art.title}")
                            print(f"Description: {art.description or 'N/A'}")
                            print(f"Creation Date: {art.creation_date or 'N/A'}")
                            print(f"Medium: {art.medium or 'N/A'}")
                            print(f"Image URL: {art.image_url or 'N/A'}")
                            print(f"Artist ID: {art.artist_id}")
                    else:
                        print("No artworks found for the given keyword")

                elif choice == "0":
                    print("Exiting... Thank You!")
                    break
                else:
                    print("Invalid Choice. Try again.")
            except (InvalidIDException,InvalidArtworkException, InvalidDateException, InvalidWebsiteException, InvalidMediumTypeException, DuplicateArtworkException) as e:
                print(f"Validation Error: {e}")
            except ValueError:
                print("Invalid input type. Please enter numeric value..")
            except Exception as e:
                print(f"Unexpected Error: {e}")

    @staticmethod
    def gallery_menu(service):
        while True:
            print("\n ------- Gallery Menu -------")
            print("\n 1. Add Gallery")
            print("\n 2. Update Gallery")
            print("\n 3. Get Gallery By ID")
            print("\n 4. Delete Gallery")
            print("\n 5. Search Gallery")
            print("\n 0. Exit")
            choice = input("Enter you choice:")
            try:
                if choice == "1":
                    gallery_id = clean_input(input("Enter Gallery ID: "))
                    name = clean_input(input("Enter Gallery Name: "))
                    description = clean_input(input("Enter Gallery Description: "))
                    location = clean_input(input("Enter Gallery Location: "))
                    curator = clean_input(input("Enter Gallery Curator: "))
                    opening_hours = clean_input(input("Enter Gallery Opening Hours: "))
                    gallery = Gallery(gallery_id = gallery_id, name = name, description = description or None, location = location or None, curator = curator or None, opening_hours = opening_hours or None)
                    success = service.add_gallery(gallery)
                    if success:
                        print("Gallery Added Successfully")
                    else:
                        print("Failed to add Gallery")

                elif choice == "2":
                    gallery_id = clean_input(input("Enter Gallery ID to update: "))
                    existing = service.get_gallery_by_id(gallery_id)
                    if not existing:
                        print("Gallery not found.")
                        continue

                    name = clean_input(input(f"Enter new name [{existing.name}]: ")) or existing.name
                    description = clean_input(
                        input(f"Enter new description [{existing.description}]: ")) or existing.description
                    location = clean_input(input(f"Enter new location [{existing.location}]: ")) or existing.location
                    curator = clean_input(input(f"Enter new curator ID [{existing.curator}]: ")) or existing.curator
                    opening_hours = clean_input(
                        input(f"Enter new opening hours [{existing.opening_hours}]: ")) or existing.opening_hours

                    updated_gallery = Gallery(
                        gallery_id=gallery_id,
                        name=name,
                        description=description,
                        location=location,
                        curator=curator,
                        opening_hours=opening_hours
                    )
                    if service.update_gallery(updated_gallery):
                        print("Gallery updated successfully")
                    else:
                        print("Update failed")

                elif choice == "3":
                    gallery_id = clean_input(input("Enter Gallery ID to fetch: "))
                    gallery = service.get_gallery_by_id(gallery_id)
                    if gallery:
                        print(f"\nGallery ID: {gallery.gallery_id}")
                        print(f"Name: {gallery.name}")
                        print(f"Description: {gallery.description}")
                        print(f"Location: {gallery.location}")
                        print(f"Curator: {gallery.curator}")
                        print(f"Opening Hours: {gallery.opening_hours}")
                    else:
                        print("Gallery not found.")

                elif choice == "4":
                    gallery_id = int(input("Enter Gallery ID to delete: "))
                    confirm = input(f"Are you sure you want to delete Gallery {gallery_id}? [y/N] ")
                    if confirm.lower() == "y":
                        if service.remove_gallery(gallery_id):
                            print("Gallery deleted successfully")
                        else:
                            print("Failed to delete gallery")
                    else:
                        print("Gallery deletion cancelled.")

                elif choice == "5":
                    print("\n Search Galleries By:")
                    print("1. Name")
                    print("2. Location")
                    print("3. Curator ID")
                    search_choice = input("Enter your choice (1/2/3): ")

                    if search_choice == "1":
                        search_by = "name"
                    elif search_choice == "2":
                        search_by = "location"
                    elif search_choice == "3":
                        search_by = "curator"
                    else:
                        print("Invalid choice. Please select a valid option")
                        return

                    keyword = input(f"Enter keyword to search in {search_by.capitalize()}: ")
                    galleries = service.search_gallery(keyword, search_by)
                    if galleries:
                        print("\n--------- Matching Galleries ---------")
                        for g in galleries:
                            print(f"\nID: {g.gallery_id}")
                            print(f"Name: {g.name}")
                            print(f"Description: {g.description or 'N/A'}")
                            print(f"Location: {g.location or 'N/A'}")
                            print(f"Curator ID: {g.curator or 'N/A'}")
                            print(f"Opening Hours: {g.opening_hours or 'N/A'}")
                    else:
                        print("No galleries found for the given keyword")

                elif choice == "0":
                    print("Exiting... Thank You!")
                    break
                else:
                    print("Invalid Choice. Try again.")

            except (InvalidIDException, DuplicateGalleryException, InvalidGalleryNameException, GalleryNotFoundException, GalleryAssignmentException,InvalidOpeningHoursException) as e:
                print(f"Validation Error: {e}")
            except ValueError:
                print("Invalid input type. Please enter numeric value..")
            except Exception as e:
                print(f"Unexpected Error: {e}")

    """" User Menu """
    @staticmethod
    def user_menu(service):
        while True:
            print("\n ------- User Menu -------")
            print("\n 1. Add User")
            print("\n 2. Update User")
            print("\n 3. Get User By ID")
            print("\n 4. Delete User")
            print("\n 5. Reactivate User")
            print("\n 0. Exit")
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    user_id = int(input("Enter User ID: "))
                    username = input("Enter Username: ")
                    password = input("Enter Password: ")
                    email = clean_input(input("Enter Email: "))
                    first_name = clean_input(input("Enter First Name: "))
                    last_name = clean_input(input("Enter Last Name: "))
                    dob_input = clean_input(input("Enter Date of Birth (YYYY-MM-DD): "))
                    date_of_birth = datetime.strptime(dob_input, "%Y-%m-%d").date() if dob_input else None
                    profile_picture = clean_input(input("Enter Profile Picture URL: "))
                    user = User(user_id = user_id,username=username, password=password, email=email or None, first_name=first_name or None,last_name=last_name or None, date_of_birth=date_of_birth or None, profile_picture=profile_picture or None, user_is_active = True )
                    if service.add_user(user):
                        print("User Added Successfully!")
                    else:
                        print("Failed to add user")

                elif choice == "2":
                    user_id = int(input("Enter User ID to update: "))
                    existing_user = service.get_user_by_id(user_id)
                    if not existing_user:
                        raise InvalidIDException("User with this ID does not exist")

                    print("Leave fields empty to keep existing values.")

                    username = input(f"Enter New Username [{existing_user.username}]: ") or existing_user.username
                    password = input(f"Enter New Password [{existing_user.password}]: ") or existing_user.password
                    email = clean_input(input(f"Enter New Email [{existing_user.email}]: ")) or existing_user.email
                    first_name = clean_input(
                        input(f"Enter New First Name [{existing_user.first_name}]: ")) or existing_user.first_name
                    last_name = clean_input(
                        input(f"Enter New Last Name [{existing_user.last_name}]: ")) or existing_user.last_name
                    dob_input = clean_input(
                        input(f"Enter New Date of Birth (YYYY-MM-DD) [{existing_user.date_of_birth}]: "))

                    if dob_input:
                        date_of_birth = datetime.strptime(dob_input, "%Y-%m-%d").date()
                    else:
                        date_of_birth = existing_user.date_of_birth

                    profile_picture = clean_input(input(
                        f"Enter New Profile Picture URL [{existing_user.profile_picture}]: ")) or existing_user.profile_picture

                    updated_user = User(user_id=user_id,username=username,password=password,email=email,first_name=first_name,last_name=last_name,date_of_birth=date_of_birth,profile_picture=profile_picture,user_is_active=True)
                    if service.update_user(updated_user):
                        print("User updated successfully!")
                    else:
                        print("Failed to update user.")

                elif choice == "3":
                    user_id = int(input("Enter User ID to fetch: "))
                    user = service.get_user_by_id(user_id)
                    if user:
                        print("\n--------- User Details ---------")
                        print(f"ID: {user.user_id}")
                        print(f"Username: {user.username}")
                        print(f"Email: {user.email or 'N/A'}")
                        print(f"First Name: {user.first_name or 'N/A'}")
                        print(f"Last Name: {user.last_name or 'N/A'}")
                        print(f"Date of Birth: {user.date_of_birth or 'N/A'}")
                        print(f"Profile Picture: {user.profile_picture or 'N/A'}")
                        print(f"Active Status: {'Active' if user.user_is_active else 'Inactive'}")
                    else:
                        raise InvalidIDException("User with this ID does not exist")

                elif choice == "4":
                    user_id = int(input("Enter User ID to delete: "))
                    confirm = input(f"Are you sure you want to delete User {user_id}? [y/N] ")
                    if confirm.lower() == "y":
                        if service.remove_user(user_id):
                            print("User deleted successfully")
                        else:
                            print("Failed to delete user")
                    else:
                        print("Attempt to Delete the User has been cancelled")

                elif choice == "5":
                    user_id = int(input("Enter User ID to reactivate: "))
                    password = input("Enter the user's password for verification: ").strip()
                    result = service.reactivate_user(user_id, password)
                    if result == 'reactivated':
                        print("User account Reactivated Successfully")
                    elif result == 'already_active':
                        print("User account Already Active, No Action Needed")
                    elif result == 'invalid_credentials':
                        print("\n Security Alert: Incorrect password - Reactivation denied")
                        print("Please verify credentials with the user.")
                    elif result == 'not_found':
                        raise InvalidIDException("User with this ID does not exist")


                elif choice == "0":
                    print("Exiting... Thank You!")
                    break
                else:
                    print("Invalid Choice. Try again.")

            except (InvalidIDException, DuplicateUserException, InvalidUsernameException, InvalidPasswordException, InvalidEmailException) as e:
                print(f"Validation Error: {e}")
            except ValueError:
                print("Invalid input type. Please enter numeric value.")
            except Exception as e:
                print(f"Unexpected Error: {e}")

    """ User Favorite """

    @staticmethod
    def user_favorite_menu(service):
        while True:
            print("\n ------- User Favorite Menu -------")
            print("\n 1. Add Artwork to Favorite")
            print("\n 2. Remove Artwork from Favorite")
            print("\n 3. Get User favorite Artworks by ID")
            print("\n 0. Exit")
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    user_id = int(input("Enter User ID: "))
                    artwork_id = int(input("Enter Artwork ID to favorite: "))
                    if service.add_artwork_to_favorite(user_id, artwork_id):
                        print("Artwork added to favorites successfully.")
                    else:
                        print("Failed to add artwork to favorites.")
                elif choice == "2":
                    user_id = int(input("Enter User ID: "))
                    artwork_id = int(input("Enter Artwork ID to remove from favorites: "))
                    if service.remove_artwork_from_favorite(user_id, artwork_id):
                        print("Artwork removed from favorites successfully.")
                    else:
                        print("Failed to remove artwork from favorites.")
                elif choice == "3":
                    user_id = int(input("Enter User ID to fetch favorite artworks: "))
                    favorites = service.get_user_favorite_artworks(user_id)
                    if not favorites:
                        print("This user has no favorite artworks.")
                    else:
                        print("\n------ Favorite Artworks ------")
                        for art in favorites:
                            print(f"\nID: {art.artwork_id}")
                            print(f"Title: {art.title}")
                            print(f"Description: {art.description}")
                            print(f"Medium: {art.medium}")
                            print(f"Creation Date: {art.creation_date}")
                            print(f"Artist ID: {art.artist_id}")
                elif choice == "0":
                    print("Exiting... Thank You!")
                    break

            except (UserNotFoundException, ArtworkDoesNotExistException, FavoriteAlreadyExistsException,
                    InvalidIDException, FavoriteNotFoundException) as e:
                print(f"Validation Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")

    @staticmethod
    def artwork_gallery_menu(service):
        while True:
            print("\n ------- Artwork Gallery Menu -------")
            print("\n 1. Add Artwork to Gallery")
            print("\n 2. Remove Artwork from Gallery")
            print("\n 3. Get Artworks by Gallery ID")
            print("\n 0. Exit")
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    artwork_id = int(input("Enter Artwork ID: "))
                    gallery_id = int(input("Enter Gallery ID: "))
                    if service.add_artwork_to_gallery(artwork_id, gallery_id):
                        print("Artwork successfully added to the gallery")
                    else:
                        print("Failed to add artwork")
                elif choice == "2":
                    artwork_id = int(input("Enter Artwork ID: "))
                    gallery_id = int(input("Enter Gallery ID: "))
                    if service.remove_artwork_from_gallery(artwork_id, gallery_id):
                        print("Artwork removed from gallery successfully")
                    else:
                        print("Failed to remove artwork")
                elif choice == "3":
                    gallery_id = int(input("Enter Gallery ID to fetch artworks: "))
                    artworks = service.get_artworks_by_gallery(gallery_id)
                    if artworks:
                        for art in artworks:
                            print(f"\nID: {art.artwork_id}")
                            print(f"Title: {art.title}")
                            print(f"Medium: {art.medium}")
                    else:
                        print("No artworks found for this gallery")
                elif choice == "0":
                    print("Exiting... Thank You!")
                    break

            except (GalleryNotFoundException, DuplicateArtworkException,ArtworkDoesNotExistException,
                    InvalidIDException, GalleryNotFoundException) as e:
                print(f"Validation Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")

    """ Artist Panel Implementation """

    @staticmethod
    def artist_panel(service):
        print("\n-------- Artist Portal --------")
        while True:
            print("\n1. Login")
            print("2. Sign Up")
            print("0. Back to Main Menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                MainModule._artist_login_flow(service)
                break
            elif choice == "2":
                MainModule._artist_signup_flow(service)
            elif choice == "0":
                return
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def _artist_login_flow(service):
        print("\n-------- Artist Login --------")
        while True:
            artist_name = input("Enter your artist name: ").strip()
            password = input("Enter your password: ").strip()

            if not artist_name or not password:
                print("Both artist name and password are required.")
                continue

            try:
                # Authenticate the artist
                artist_info = service.artist_login(artist_name, password)
                print(f"\nWelcome, {artist_info['artist_name']}!")
                MainModule._artist_dashboard(service, artist_info)
                break
            except Exception as e:
                print(f"Login failed: {str(e)}")
                retry = input("Would you like to try again? (y/n): ").lower()
                if retry != 'y':
                    return

    @staticmethod
    def _artist_signup_flow(service):
        print("\n-------- Artist Sign Up --------")
        try:
            artist_id = int(input("Enter your artist ID : ").strip())
            name = input("Enter your artist username: ").strip()
            password = input("Create a password: ").strip()
            confirm_password = input("Confirm password: ").strip()

            if password != confirm_password:
                print("Passwords do not match!")
                return

            if len(password) < 6:
                print("Password must be at least 6 characters long!")
                return

            biography = clean_input(input("Enter your biography (optional): "))

            birth_date_input = clean_input(input("Enter your birth date (YYYY-MM-DD, optional): "))
            birth_date = datetime.strptime(birth_date_input, "%Y-%m-%d").date() if birth_date_input else None

            nationality = clean_input(input("Enter your nationality (optional): "))
            website = clean_input(input("Enter your website URL (optional): "))
            contact_info = input("Enter your contact information: ").strip()

            artist = Artist(
                artist_id=artist_id,
                name=name,
                biography=biography,
                birth_date=birth_date,
                nationality=nationality,
                website=website,
                contact_information=contact_info,
                is_active=True
            )

            if service.artist_signup(artist, password):
                print("\nArtist account created successfully!")
                print("You can now login with your artist name and password.")
            else:
                print("Failed to create artist account.")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def _artist_dashboard(service, artist_info):
        while True:
            print("\n-------- Artist Dashboard --------")
            print(f"Welcome, {artist_info['artist_name']} (ID: {artist_info['artist_id']})")
            print("\n1. View My Artworks")
            print("2. View My Artworks in Galleries")
            print("3. View Favorite Counts of My Artworks")
            print("4. Add New Artwork")
            print("5. Update Existing Artwork")
            print("6. Remove Artwork")
            print("0. Logout")

            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    artworks = artist_info['artworks']
                    if isinstance(artworks, str):
                        print(artworks)
                    else:
                        print("\n--- My Artworks ---")
                        for artwork in artworks:
                            print(f"\nID: {artwork['artwork_id']}")
                            print(f"Title: {artwork['title']}")
                            print(f"Medium: {artwork['medium']}")
                            print(f"Created: {artwork['creation_date']}")

                elif choice == "2":
                    galleries = artist_info['galleries_with_artworks']
                    if isinstance(galleries, str):
                        print(galleries)
                    else:
                        print("\n--- Galleries Featuring My Artworks ---")
                        for gallery in galleries:
                            print(f"\nGallery ID: {gallery['gallery_id']}")
                            print(f"Name: {gallery['name']}")
                            print(f"Location: {gallery['location']}")

                elif choice == "3":
                    favorites = artist_info['artwork_favorites']
                    print("\n--- Favorite Counts for My Artworks ---")
                    for fav in favorites:
                        print(f"\nArtwork ID: {fav['artwork_id']}")
                        print(f"Title: {fav['title']}")
                        print(f"Number of favorites: {fav['favorite_count']}")

                elif choice == "4":
                    print("\n--- Add New Artwork ---")
                    try:
                        artwork_id = int(input("Enter artwork ID: ").strip())
                        title = input("Enter artwork title: ").strip()
                        description = input("Enter artwork description: ").strip()
                        creation_date = input("Enter creation date (YYYY-MM-DD): ").strip()
                        medium = input("Enter medium type: ").strip()
                        image_url = input("Enter image URL (optional): ").strip() or None

                        creation_date = datetime.strptime(creation_date, "%Y-%m-%d").date()
                        artwork = Artwork(
                            artwork_id=artwork_id,
                            title=title,
                            description=description,
                            creation_date=creation_date,
                            medium=medium,
                            image_url=image_url,
                            artist_id=artist_info['artist_id']
                        )
                        if service.add_artwork(artwork):
                            print("Artwork added successfully!")

                            artist_info = service.artist_login(artist_info['artist_name'],
                                                               input("Enter your password to refresh: ").strip())
                        else:
                            print("Failed to add artwork.")
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                    except Exception as e:
                        print(f"Error: {e}")

                elif choice == "5":
                    print("\n--- Update Artwork ---")
                    try:
                        artwork_id = int(input("Enter artwork ID to update: ").strip())
                        artwork = service.get_artwork_by_id(artwork_id)

                        if not artwork:
                            print("Artwork not found.")
                            continue

                        if str(artwork.artist_id) != str(artist_info['artist_id']):
                            print("You can only update your own artworks.")
                            continue

                        print("\nCurrent Artwork Details:")
                        print(f"Title: {artwork.title}")
                        print(f"Description: {artwork.description}")
                        print(f"Creation Date: {artwork.creation_date}")
                        print(f"Medium: {artwork.medium}")
                        print(f"Image URL: {artwork.image_url}")

                        print("\nEnter new values (leave blank to keep current):")
                        title = input(f"Title [{artwork.title}]: ").strip() or artwork.title
                        description = input(f"Description [{artwork.description}]: ").strip() or artwork.description
                        creation_date_input = input(f"Creation Date [{artwork.creation_date}] (YYYY-MM-DD): ").strip()
                        creation_date = datetime.strptime(creation_date_input,
                                                          "%Y-%m-%d").date() if creation_date_input else artwork.creation_date
                        medium = input(f"Medium [{artwork.medium}]: ").strip() or artwork.medium
                        image_url = input(f"Image URL [{artwork.image_url}]: ").strip() or artwork.image_url

                        updated_artwork = Artwork(
                            artwork_id=artwork_id,
                            title=title,
                            description=description,
                            creation_date=creation_date,
                            medium=medium,
                            image_url=image_url,
                            artist_id=artist_info['artist_id']
                        )

                        if service.update_artwork(updated_artwork):
                            print("Artwork updated successfully!")
                            # Refresh artist info
                            artist_info = service.artist_login(artist_info['artist_name'],
                                                               input("Enter your password to refresh: ").strip())
                        else:
                            print("Failed to update artwork.")
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                    except Exception as e:
                        print(f"Error: {e}")

                elif choice == "6":
                    print("\n--- Remove Artwork ---")
                    try:
                        artwork_id = int(input("Enter artwork ID to remove: ").strip())
                        artwork = service.get_artwork_by_id(artwork_id)

                        if not artwork:
                            print("Artwork not found.")
                            continue

                        if str(artwork.artist_id) != str(artist_info['artist_id']):
                            print("You can only remove your own artworks.")
                            continue

                        confirm = input(
                            f"Are you sure you want to permanently delete artwork '{artwork.title}'? (y/n): ").lower()
                        if confirm == 'y':
                            if service.remove_artwork(artwork_id):
                                print("Artwork removed successfully!")
                                # Refresh artist info
                                artist_info = service.artist_login(artist_info['artist_name'],
                                                                   input("Enter your password to refresh: ").strip())
                            else:
                                print("Failed to remove artwork.")
                    except Exception as e:
                        print(f"Error: {e}")

                elif choice == "0":
                    print("Logging out...")
                    break

                else:
                    print("Invalid choice. Please try again.")

            except Exception as e:
                print(f"An error occurred: {e}")

    @staticmethod
    def user_panel(service):
        print("\n-------- User Portal --------")
        while True:
            print("\n1. Login")
            print("2. Sign Up")
            print("0. Back to Main Menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                MainModule._user_login_flow(service)
                break
            elif choice == "2":
                MainModule._user_signup_flow(service)
            elif choice == "0":
                return
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def _user_login_flow(service):
        print("\n-------- User Login --------")
        while True:
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if not username or not password:
                print("Both username and password are required.")
                continue

            try:
                # Authenticate the user
                user_info = service.user_login(username, password)
                print(f"\nWelcome, {user_info['username']}!")
                MainModule._user_dashboard(service, user_info)
                break
            except Exception as e:
                print(f"Login failed: {str(e)}")
                retry = input("Would you like to try again? (y/n): ").lower()
                if retry != 'y':
                    return

    @staticmethod
    def _user_signup_flow(service):
        print("\n-------- User Sign Up --------")
        try:
            user_id = int(input("Enter your user ID (number): ").strip())
            username = input("Choose a username: ").strip()
            password = input("Create a password: ").strip()
            confirm_password = input("Confirm password: ").strip()

            if password != confirm_password:
                print("Passwords do not match!")
                return

            if len(password) < 6:
                print("Password must be at least 6 characters long!")
                return

            email = clean_input(input("Enter your email: "))
            first_name = clean_input(input("Enter your first name: "))
            last_name = clean_input(input("Enter your last name: "))

            dob_input = clean_input(input("Enter your date of birth (YYYY-MM-DD): "))
            date_of_birth = datetime.strptime(dob_input, "%Y-%m-%d").date() if dob_input else None

            profile_picture = clean_input(input("Enter profile picture URL: "))

            user = User(
                user_id=user_id,
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                profile_picture=profile_picture,
                user_is_active=True
            )

            if service.add_user(user):
                print("\nUser account created successfully!")
                print("You can now login with your username and password.")
            else:
                print("Failed to create user account.")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def _user_dashboard(service, user_info):
        while True:
            print("\n-------- User Dashboard --------")
            print(f"Welcome, {user_info['username']} (ID: {user_info['user_id']})")
            print("\n1. View My Favorites")
            print("2. Add Artwork to Favorites")
            print("3. Remove Artwork from Favorites")
            print("0. Logout")

            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    favorites = user_info['favorites']
                    if isinstance(favorites, str):
                        print(favorites)
                    else:
                        print("\n--- My Favorite Artworks ---")
                        for artwork in favorites:
                            print(f"\nID: {artwork.artwork_id}")
                            print(f"Title: {artwork.title}")
                            print(f"Description: {artwork.description}")
                            print(f"Medium: {artwork.medium}")
                            print(f"Created: {artwork.creation_date}")

                elif choice == "2":
                    print("\n--- Add Artwork to Favorites ---")
                    artwork_id = int(input("Enter artwork ID to add to favorites: ").strip())
                    if service.add_artwork_to_favorite(user_info['user_id'], artwork_id):
                        print("Artwork added to favorites successfully!")
                        user_info = service.user_login(user_info['username'],
                                                       input("Enter your password to refresh: ").strip())
                    else:
                        print("Failed to add artwork to favorites.")

                elif choice == "3":
                    print("\n--- Remove Artwork from Favorites ---")
                    artwork_id = int(input("Enter artwork ID to remove from favorites: ").strip())
                    if service.remove_artwork_from_favorite(user_info['user_id'], artwork_id):
                        print("Artwork removed from favorites successfully!")
                        # Refresh user info
                        user_info = service.user_login(user_info['username'],
                                                       input("Enter your password to refresh: ").strip())
                    else:
                        print("Failed to remove artwork from favorites.")

                elif choice == "0":
                    print("Logging out...")
                    break

                else:
                    print("Invalid choice. Please try again.")

            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {e}")
    @staticmethod
    def main():
        service = VirtualArtGalleryImp()
        print("------------------- Welcome Virtual Art Gallery -----------------")
        while True:
            print("\n Main Menu")
            print("1. Artist")
            print("2. Artwork")
            print("3. Gallery")
            print("4. User")
            print("5. User Favorite")
            print("6. Artwork Gallery")
            print("7. Artist Panel")
            print("8. User Panel")
            print("0. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                MainModule.artist_menu(service)
            elif choice == "2":
                MainModule.artwork_menu(service)
            elif choice == "3":
                MainModule.gallery_menu(service)
            elif choice == "4":
                MainModule.user_menu(service)
            elif choice == "5":
                MainModule.user_favorite_menu(service)
            elif choice == "6":
                MainModule.artwork_gallery_menu(service)
            elif choice == "7":
                MainModule.artist_panel(service)
            elif choice == "8":
                MainModule.user_panel(service)
            elif choice == '0':
                print("GoodBye!")
                break
            else:
                print("Invalid Choice. Try again.")

if __name__ == '__main__':
    MainModule.main()



