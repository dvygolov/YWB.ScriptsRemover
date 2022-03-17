import json

class SoftSettings(object):
    def __init__(self, jsn):
        self.__dict__ = jsn
    def __str__(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4, sort_keys=True)

def load_settings():
    with open("settings.json", "r", encoding="utf-8") as f:
        content = f.read()
        return SoftSettings(json.loads(content))


def save_settings(s: SoftSettings):
    settings=str(s)
    with open("settings.json", "w", encoding="utf-8") as f:
        f.write(settings)
    pass


