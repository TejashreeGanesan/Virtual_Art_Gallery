from dao.IVirtualArtGalleryImp import VirtualArtGalleryImp
from entity.artist import Artist
from datetime import datetime
from entity.artwork import Artwork
from exception.exceptions import (InvalidIDException, InvalidArtistNameException, InvalidDateException,
                                  InvalidWebsiteException, InvalidArtworkException, InvalidMediumTypeException,
                                  DuplicateArtworkException)

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
            #print("\n 3. Delete Artwork")
            #print("\n 4. Get Artist By ID")
            #print("\n 5. Reactivate Artist")
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
                    existing_artwork = service.get_artist_by_id(artwork_id)
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
                        input(f"Enter Website: [{existing_artwork.image_url}]: ")) or existing_artwork.image_url
                    artist_id = clean_input(input(
                        f"Enter Contact Information: [{existing_artwork.artist_id}]: ")) or existing_artwork.artist_id

                    updated_artwork = Artwork(artwork_id=artwork_id, title = title, description = description, creation_date=creation_date,
                                              medium = medium, image_url = image_url or None, artist_id = artist_id)

                    if service.update_artwork(updated_artwork):
                        print("Artwork Updated Successfully")

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
    def main():
        service = VirtualArtGalleryImp()
        print("------------------- Welcome Virtual Art Gallery -----------------")
        while True:
            print("\n Main Menu")
            print("1. Artist")
            print("2. Artwork")
            print("0. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                MainModule.artist_menu(service)
            if choice == "2":
                MainModule.artwork_menu(service)
            elif choice == '0':
                print("GoodBye!")
                break
            else:
                print("Invalid Choice. Try again.")

if __name__ == '__main__':
    MainModule.main()



