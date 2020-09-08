import os
import json


def is_managed(func):
    def wrapper(*args, **kwargs):
        area = kwargs['area'] if 'area' in kwargs else args[0]
        if os.path.exists(os.path.join(area, '.note_manager',  'settings.json')) and \
                os.path.isfile(os.path.join(area, '.note_manager',  'settings.json')):
            return func(*args, **kwargs)
        else:
            print("This not currently managed area")
            return
    return wrapper


def is_area(func):
    def wrapper(*args, **kwargs):
        area = kwargs['area'] if 'area' in kwargs else args[0]
        if os.path.exists(area)and os.path.isdir(area):
            return func(*args, **kwargs)
        else:
            print("This area does not exists")
            return
    return wrapper


class DirectoryManager(object):
    settings_folder = '.note_manager'
    settings_file = 'settings.json'
    settings_template = {
        "folders": []
    }

    @is_area
    @is_managed
    def move(self, area, file):
        settings = self._get_settings(area)

    @is_area
    @is_managed
    def add_folder(self, area, foldername):
        if not os.path.exists(os.path.join(area, foldername)):
            print("Creating new folder...")
            os.mkdir(area, foldername)
            print("Folder created")

        new_folder = {
            'name': foldername,
            'tags': []
        }

        self._write_settings(area, self._get_settings(area)["folder"].append(new_folder))

    @is_area
    @is_managed
    def add_tags(self, area, folder, tags):
        if not os.path.exists(os.path.join(area, folder)):
            raise FileNotFoundError
        settings = self._get_settings(area=area)
        # TODO: Add tags to folder in setting file

    @is_area
    def new_area(self, area):
        if os.path.exists(os.path.join(area, self.settings_folder, self.settings_file)):
            print("Area is already managed")
            return
        if not (os.path.exists(os.path.join(area, self.settings_folder)) or os.path.isdir(os.path.join(area, self.settings_folder))):
            os.mkdir(os.path.join(area, self.settings_folder))
        self._write_settings(area, self.settings_template)

    @is_managed
    def _get_settings(self, area):
        with open(os.path.join(area, self.settings_folder, self.settings_file, 'r')) as file:
            settings = json.load(file)
        return settings

    def _write_settings(self, area, settings):
        with open(os.path.join(area, self.settings_folder, self.settings_file), 'w+') as file:
            json.dump(settings, file)



