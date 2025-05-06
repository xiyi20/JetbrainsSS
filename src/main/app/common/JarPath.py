from enum import Enum


class JarPath(Enum):
    Idea = {
        '2024': ["/lib/product.jar", "idea_logo"],
        '2025': ["/lib/product.jar", "idea_logo"]
    }
    PyCharm = {
        '2024': ["/lib/app.jar", "pycharm_logo"],
        '2025': ["/lib/app.jar", "pycharm_logo"]
    }
    WebStorm = {
        '2024': ["/lib/app.jar", "artwork/webide_logo"],
        '2025': ["/lib/app.jar", "artwork/webide_logo"]
    }
