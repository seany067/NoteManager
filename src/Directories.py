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

    @is_folder
    def check_save(self, area, folder, file, data):
        with open(os.path.join(area, folder, file), 'r') as f:
            read = f.read()
            suc = read.rstrip("\n") == data.rstrip("\n")
        return suc

    @is_folder
    def get_file_content(self, area, folder, file):
        with open(os.path.join(area, folder, file), "r+") as f:
            data = f.read()
        return data

    @is_managed
    def get_folders(self, area):
        settings = self._get_settings(area)
        return [folder for folder, values in settings["folders"].items()]

    @is_managed
    def find_folder(self, area, data):
        settings = self._get_settings(area)

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
        highest = (None, 0)
        for key, value in totals.items():
            if value > highest[1]:
                highest = (key, value)

        if highest[0] is None:
            print("None of the folders had matching tags, please move file manually")
            return None
        return highest[0]

    @is_managed
    def check_file_collision(self, area, folder, filename):
        return os.path.exists(os.path.join(area, folder, filename)) and os.path.isfile(os.path.join(area, folder, filename))

    @is_managed
    def check_folder_collision(self, area, folder):
        return os.path.exists(os.path.join(area, folder)) and os.path.isdir(os.path.join(area, folder))

    @is_managed
    def new_save_file(self, area, filename, filecontent):
        folder = self.find_folder(area=area, data=filecontent)
        if folder is None:
            return False, "No associated folders, please manually save"
        if self.check_file_collision(area=area, folder=folder, filename=filename):
            return False, "File already exists"
        with open(os.path.join(area, folder, filename), 'w+') as f:
            f.write(filecontent.strip())
        return True, "Successfully saved", filename, folder

    @is_managed
    def save_file(self, area, folder, filename, filecontent):
        with open(os.path.join(area, folder, filename), 'w+') as f:
            f.write(filecontent.strip())
        return True, "Successfully updated", filename, folder

    @is_managed
    def move(self, area, file):
        with open(file, 'r') as f:
            data = f.read()

        folder = self.find_folder(area=area, data=data)
        filename = ntpath.basename(file)
        outcome = self.check_file_collision(area=area, folder=folder, filename=filename)

        # This should move the file
        if outcome:
            print("A file with this name already exists\n Please rename the file")
            return outcome
        else:
            os.rename(file, os.path.join(area, folder, filename))
            return outcome

    @is_managed
    def add_folder(self, area, folder, tags=[]):
        print(area, folder)
        if not self.check_folder_collision(area=area, folder=folder):
            print("Creating new folder...")
            os.mkdir(os.path.join(area, folder))
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
    def get_files(self, area, folder):
        path = os.path.join(area, folder)
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    @is_managed
    @is_folder
    def get_folder_info(self, area, folder):
        settings = self._get_settings(area)
        return settings["folders"][folder]

    @is_managed
    @is_folder
    def add_tags(self, area, folder, tags):
        settings = self._get_settings(area=area)
        settings["folders"][folder]["tags"] += [tags]
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
    def get_tags(self, area, folder):
        return self._get_settings(area=area)["folders"][folder]["tags"]

    @is_managed
    @is_folder
    def remove_tag(self, area, folder, tag):
        tags = set(self.get_tags(area=area, folder=folder))
        tags.remove(tag)
        self.set_tags(area=area, folder=folder, tags=list(tags))

    @is_area
    def new_area(self, area):
        if os.path.exists(os.path.join(area, self.settings_folder, self.settings_file)):
            print("Area is already managed")
            return
        if not (os.path.exists(os.path.join(area, self.settings_folder)) or os.path.isdir(
                os.path.join(area, self.settings_folder))):
            os.mkdir(os.path.join(area, self.settings_folder))
        new_settings = self.settings_template
        for dir in os.listdir(area):
            if dir == ".note_manager":
                return
            folder = os.path.join(area, dir)
            if os.path.isdir(folder):
                if not (os.path.exists(os.path.join(area, dir)) and os.path.isdir(os.path.join(area, dir))):
                    print("Creating new folder...")
                    os.mkdir(folder)
                    print("Folder created")
                new_folder = {
                    'name': dir,
                    'tags': [],
                }
                new_settings["folders"][dir] = new_folder
        self._write_settings(area, new_settings)

    @is_managed
    def add_all_folders(self, area):
        for dir in os.listdir(area):
            if os.path.isdir(dir):
                if not (os.path.exists(os.path.join(area, dir)) and os.path.isdir(os.path.join(area, dir))):
                    print("Creating new folder...")
                    os.mkdir(os.path.join(area, dir))
                    print("Folder created")
                new_folder = {
                    'name': dir,
                    'tags': [],
                }
                settings = self._get_settings(area)
                settings["folders"][dir] = new_folder
                self._write_settings(area=area, settings=settings)

    @is_managed
    def _get_settings(self, area):
        with open(os.path.join(area, self.settings_folder, self.settings_file), 'r') as file:
            settings = json.load(file)
        return settings

    @is_area
    def _write_settings(self, area, settings):
        with open(os.path.join(area, self.settings_folder, self.settings_file), 'w+') as file:
            json.dump(settings, file)
