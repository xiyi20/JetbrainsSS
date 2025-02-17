import io
import json


class RwConfig:
    _rwConfig = None
    def __new__(cls, *args, **kwargs):
        if not cls._rwConfig:
            cls._rwConfig = super(RwConfig, cls).__new__(cls)
        return cls._rwConfig

    def __init__(self):
        self.config = {}
        self.configFile = "./config.json"
        try:
            with open(self.configFile, "r") as configFile:
                self.config = json.load(configFile)
        except FileNotFoundError as e:
            print(e)
        except json.decoder.JSONDecodeError as e:
            print(e)

    def wConfig(self,zone , name, key, value):
        try:
            with open(self.configFile, "wb") as configFile:
                self.config[zone][name][key] = value
                json.dump(self.config, io.TextIOWrapper(configFile), indent=4)
        except FileNotFoundError as e:
            print(e)
        except KeyError as e:
            print(e)
