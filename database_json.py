import json

from project import Project
from user import User


class Database:
    """
    JSON database for project manager
    """
    CLSS = {'users': User, 'projects': Project}

    def __init__(self, file_name='data.json'):
        self.file_name = file_name

    def _get_result_format(self):
        return {'projects': [], "users": []}

    def update_data(self, new_data):
        result = {'projects': [], "users": []}
        for group in new_data:
            for item in  range(len(new_data[group])):
                result[group].append(new_data[group][item].__dict__)
        with open(self.file_name, 'w') as storage:
            json.dump(result, storage)

    def _parse_object(self, cls, item):
        fields = {name: item[name] for name in cls.get_fields()}
        return item[cls.get_fields()[0]], cls(**fields)

    def _parse_data(self, data):
        result = self._get_result_format()
        for group in data:
            for item in data[group]:
                key, obj = self._parse_object(self.CLSS[group], item)
                result[group].append(obj)
        return result

    def get_data(self):
        try:
            with open(self.file_name, 'r') as storage:
                return self._parse_data(json.load(storage))
        except FileNotFoundError:
            return self._get_result_format()
