import os
import json
import re
import ntpath


def is_managed(func):
    def wrapper(*args, **kwargs):
        area = kwargs['area'] if 'area' in kwargs else args[1]
        if os.path.exists(os.path.join(area, '.note_manager', 'settings.json')) and os.path.isfile(os.path.join(area, '.note_manager', 'settings.json')):
            return func(*args, **kwargs)
        else:
            print("This not currently managed area or this area does not exist")
            return
    return wrapper


def is_area(func):
    def wrapper(*args, **kwargs):
        area = kwargs['area'] if 'area' in kwargs else args[1]
        if os.path.exists(area) and os.path.isdir(area):
            return func(*args, **kwargs)
        else:
            print("This area does not exists")
            return
    return wrapper


def is_folder(func):
    def wrapper(*args, **kwargs):
        area = kwargs['area'] if 'area' in kwargs else args[1]
        folder = kwargs['folder'] if 'folder' in kwargs else args[2]
        folder_full = os.path.join(area, folder)
        if os.path.exists(folder_full) and os.path.isdir(folder_full):
            return func(*args, **kwargs)
        else:
            print("This area does not exists")
            return
    return wrapper


class DirectoryManager(object):
    settings_folder = '.note_manager'
    settings_file = 'settings.json'
    settings_template = {
        "folders": {}
    }

    def __init__(self, cli=False):
        self.cli = cli

    @is_managed
    def get_folders(self, area):
        settings = self._get_settings(area)
        return [folder for folder, values in settings["folders"].items()]

    @is_managed
    def move(self, area, file):
        settings = self._get_settings(area)

        with open(file, 'r') as f:
            data = f.read()

        # Regex to count tag occurrences
        totals = {}
        for folders, values in settings["folders"].items():
            count = 0
            for tag in values["tags"]:
                occurrences = re.findall(tag, data)
                count += len(occurrences)
            totals[folders] = count

        # Thing that should draw a cmd line graph of occurrences
        # Tried to normalise the data using the average but i think the equation maybe wrong
        if self.cli:
            average = sum([val for key, val in totals.items()]) / len(totals.items())
            for folders, values in totals.items():
                print(('{0}:' + '#' * round(values / average)).format(folders))

        # Finds the folder with the highest number of matching tags
        highest = (None, None)
        for key, value in totals.items():
            if value > highest[1]:
                highest = (key, value)

        if highest[0] is None:
            print("None of the folders had matching tags, please move file manually")
            return

        # This should move the file
        os.rename(file, os.path.join(area, highest[0], ntpath.basename(file)))

    @is_managed
    def add_folder(self, area, folder, tags):
        if not os.path.exists(os.path.join(area, folder)):
            print("Creating new folder...")
            os.mkdir(area, folder)
            print("Folder created")

        new_folder = {
            'name': folder,
            'tags': tags,
        }
        settings = self._get_settings(area)
        settings["folders"][folder] = new_folder
        self._write_settings(area=area, settings=settings)

    @is_managed
    @is_folder
    def get_folder_info(self, area, folder):
        settings = self._get_settings(area)
        return settings["folders"][folder]

    @is_managed
    @is_folder
    def add_tags(self, area, folder, tags):
        settings = self._get_settings(area=area)
        settings["folders"][folder]["tags"] += tags
        settings["folders"][folder]["tags"] = list(set(settings["folders"][folder]["tags"]))  # Removes duplicates
        self._write_settings(area=area, settings=settings)

    @is_managed
    @is_folder
    def set_tags(self, area, folder, tags):
        settings = self._get_settings(area=area)
        settings["folders"][folder]["tags"] = tags
        settings["folders"][folder]["tags"] = list(set(settings["folders"][folder]["tags"]))  # Removes duplicates
        self._write_settings(area=area, settings=settings)

    @is_managed
    @is_folder
    def get_tags(self, area, folder, tags):
        return self._get_settings(area=area)["folders"][folder]["tags"]

    @is_area
    def new_area(self, area):
        if os.path.exists(os.path.join(area, self.settings_folder, self.settings_file)):
            print("Area is already managed")
            return
        if not (os.path.exists(os.path.join(area, self.settings_folder)) or os.path.isdir(
                os.path.join(area, self.settings_folder))):
            os.mkdir(os.path.join(area, self.settings_folder))
        self._write_settings(area, self.settings_template)

    @is_managed
    def add_all_folders(self, area):
        for dir in os.listdir(area):
            if os.path.isdir(dir):
                self.add_folder(area=area, foldername=dir)

    @is_managed
    def _get_settings(self, area):
        with open(os.path.join(area, self.settings_folder, self.settings_file), 'r') as file:
            settings = json.load(file)
        return settings

    @is_area
    def _write_settings(self, area, settings):
        with open(os.path.join(area, self.settings_folder, self.settings_file), 'w+') as file:
            json.dump(settings, file)
