from enum import Enum


class JarPath(Enum):
    # 格式: 版本号 -> [{jar 内相对路径: [logo 资源基础名(不含扩展名), ...]}, ...]
    # 同一版本可配置多个 jar, 逐个修补
    Idea = {
        '253': [{"/lib/product-backend.jar": ["idea_logo", "idea_logo_subscription"]}],
        '262': [
            {"/lib/intellij.idea.ultimate.customization.jar": ["idea_logo", "idea_logo_subscription"]}
        ],
    }
    PyCharm = {
        '253': [{"/lib/product-backend.jar": ["pycharm_logo"]}],
        '262': [
            {"/lib/intellij.pycharm.community.jar": ["pycharm_core_logo"]},
            {"/lib/intellij.pycharm.pro.jar": ["pycharm_logo"]}
        ],
    }
    WebStorm = {
        '253': [{"/lib/app-backend.jar": ["artwork/webide_logo"]}],
        '262': [
            {"/lib/intellij.webstorm.branding.jar": ["artwork/webide_logo"]}
        ],
    }
