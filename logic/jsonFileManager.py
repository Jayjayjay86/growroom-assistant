import datetime
import json
import os

dehumidifier_jsonfile = "./gui/config/dehumidifiers.json"
bad_dehumidifier_jsonfile = "./gui/config/bad_dehumidifiers.json"
settings_jsonfile = "./gui/config/settings.json"


class JSONFileManager:
    def __init__(self, selection):
        if selection == "devices":
            self.file_path = dehumidifier_jsonfile
        if selection == "settings":
            self.file_path = settings_jsonfile
        if selection == "reject":
            self.file_path = bad_dehumidifier_jsonfile

    def create_file_if_not_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as json_file:
                json.dump([], json_file)

    def read_json(self):
        try:
            with open(self.file_path, "r") as json_file:
                data = json.load(json_file)
            return data
        except:
            return []

    def write_json(self, data):
        with open(self.file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def add_to_json(self, data):
        existing_data = self.read_json()
        existing_data.append(data)
        self.write_json(existing_data)

    def clear_all_json(self):
        self.write_json([])

    def delete_by_id(self, item_id):
        existing_data = self.read_json()
        updated_data = [item for item in existing_data if item.get("id") != item_id]
        self.write_json(updated_data)

    def update_settings(self, updated_settings):
        current_settings = self.read_json()
        if current_settings:
            current_settings.update(updated_settings)
            with open(self.file_path, "w") as file:
                json.dump(current_settings, file, indent=4)

    def replace_object_by_id(self, id, new_object):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        # Find the index of the object to replace based on its ID
        for index, obj in enumerate(data):
            if obj["id"] == id:
                object_index = index
                break

        if object_index is not None:
            # Replace the old object with the new one
            data[object_index] = new_object

            # Write the updated data back to the file
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)

            return True
        else:
            return False
