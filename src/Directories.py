import os
import json


class DirectoryManager(object):
    settings_folder = '.note_manager'
    settings_file = 'settings.json'
    settings_template = ''

    def move(self, area, file):
        settings = self.get_settings(area)

    def add_folder(self, area, foldername):
        if not os.path.exists(os.path.join(area, foldername)):
            print("Creating new folder...")
            os.mkdir(area, foldername)
            print("Folder created")
        settings = self.get_settings(area)
        new_folder = {
            'name': foldername,
            'tags': []
        }
        settings["folder"].append(json.load(new_folder))

    def add_tags(self, area, folder, tags):
        if not os.path.exists(os.path.join(area, folder)):
            raise FileNotFoundError
        settings = self.get_settings(area=area)
        # Add tags to folder in setting file

    def new_area(self, area):
        if os.path.exists(os.path.join(area, self.settings_folder, self.settings_file)):
            print("Area is already managed")
            return
        if not os.path.exists(area) or not os.path.isdir(area):
            raise FileNotFoundError
        os.mkdir(os.path.join(area, self.settings_folder))
        with open(os.path.join(area, self.settings_folder, self.settings_file, 'w+')) as file:
            file.write(self.settings_template)

    def get_settings(self, area):
        if not os.path.exists(os.path.join(area, self.settings_folder, self.settings_file)):
            raise FileNotFoundError
        with open(os.path.join(area, self.settings_folder, self.settings_file, 'r')) as file:
            settings = file.read()
        return json.dump(settings)

    def write_settings(self, area, settings):
        if not os.path.exists(os.path.join(area, self.settings_folder, self.settings_file)):
            raise FileNotFoundError
        with open(os.path.join(area, self.settings_folder, self.settings_file, 'w+')) as file:
            settings = file.write(settings)
