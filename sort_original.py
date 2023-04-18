import argparse
import logging
import re
import shutil
import sys
import time
from pathlib import Path
from threading import Thread, Event

from rename import normalize


ARCHIVES = "archives"
SORTING_DICT = {
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "music": [".mp3", ".ogg", ".wav", ".amr"],
    ARCHIVES: [".zip", ".gz", ".tar"],
    "other": [],
}


def get_directory():
    try:
        directory = Path(sys.argv[1])
    except IndexError:
        raise IndexError("You didn't enter the path")
    if not directory.exists():
        raise TypeError("Sorry, such directory doesn't exist")

    return directory


def create_sorted_dict(sorting_dictionary: dict) -> dict:
    """Function creates a dictionary for sorted files."""
    sorted_dict = {}
    for key in sorting_dictionary.keys():
        sorted_dict.update({key: ([], set())})
    return sorted_dict


def remove_empty_folders(directory: Path, sorting_dictionary: dict) -> None:
    """Removes any folders left after sorting (because they are empty).

    Ignores the hidden files.
    """
    exclude = "|".join(key for key in sorting_dictionary.keys())
    for dir in directory.glob("*"):
        if dir.is_dir() and not re.search(exclude, str(dir)):
            shutil.rmtree(dir)


def rename_path(file, directory, category, i=0):
    category_folder = directory / category

    if not category_folder.exists():
        category_folder.mkdir()
    file_stem = normalize(file.stem)
    new_file_path = category_folder / f"{file_stem}{file.suffix}"

    while new_file_path.exists():
        if file_stem[-1].isdigit():
            file_stem = file_stem[:-1] + str(int(file_stem[-1]) + 1)

        else:
            file_stem = file_stem + "1"

        new_file_path = category_folder / f"{file_stem}{file.suffix}"

    file.rename(new_file_path)

    return new_file_path


def sort_and_move_files(directory: Path, sorting_dictionary: dict) -> None:
    """Function checks if a file belongs to any category in a sorting_dictionary and moves it to the sorting folder.

    If the file isn't in any category, moves to "other"
    Returns a dictionary of sorted files and extentions.
    """

    sorted_dict = create_sorted_dict(sorting_dictionary)
    exclude = "|".join(key for key in sorting_dictionary.keys())

    for file in directory.rglob("?*.*"):
        if not re.search(exclude, str(file)):
            transfer = False

            for category, extentions in sorting_dictionary.items():
                if file.suffix in extentions:
                    file = rename_path(file, directory, category)
                    stats(sorted_dict, category, file)
                    transfer = True

            if transfer == False:
                file = rename_path(file, directory, "other")
                stats(sorted_dict, "other", file)

    return sorted_dict


def stats(sorted_dict, category, file_name):
    sorted_dict[category][0].append(file_name.name)
    sorted_dict[category][1].add(file_name.suffix)


def unpack_archive_to_subfolder(
    directory: Path, archive_name: Path, extention: str
) -> None:
    folder_to_unpack = directory / archive_name.stem
    folder_to_unpack.mkdir()
    shutil.unpack_archive(archive_name, folder_to_unpack, extention)


def unpack_archives_in_dir(archive_folder: Path, sorting_dictionary: dict) -> None:
    for obj in archive_folder.glob("?*.*"):
        extention = obj.suffix

        if extention in sorting_dictionary[archive_folder.name]:
            extention = extention.split(".")[1]

            try:
                unpack_archive_to_subfolder(archive_folder, obj, extention)

            except FileExistsError:
                print(f"This {obj} folder already exists")

            except shutil.ReadError:
                print("This archive couldn't be unpacked.")


def main():
    """Script renames the files, sorts the files in the given directory to folders specified as keys in a sorting dictionary, removes empty folders and prints the found files and their extentions by categories.

    By default it ignores the sorting folders.
    """

    directory = Path('/Users/inna/Documents/Test-folder')

    # try:
    #     directory = get_directory()

    # except IndexError as error:
    #     return error

    # except TypeError as error:
    #     return error

    sorted_dict = sort_and_move_files(directory, SORTING_DICT)
    remove_empty_folders(directory, SORTING_DICT)
    archive_folder = directory / ARCHIVES
    unpack_archives_in_dir(archive_folder, SORTING_DICT)

    print(sorted_dict)


if __name__ == "__main__":
    start_time = time.time()
    print(main())
    print("My program took", time.time() - start_time, "to run")
