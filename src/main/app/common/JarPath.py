from enum import Enum


class JarPath(Enum):
    Idea = {
        '253': ["/lib/product-backend.jar", ["idea_logo","idea_logo_subscription"]]
    }
    PyCharm = {
        '253': ["/lib/product-backend.jar", ["pycharm_logo"]]
    }
    WebStorm = {
        '253': ["/lib/app-backend.jar", ["artwork/webide_logo"]]
    }
