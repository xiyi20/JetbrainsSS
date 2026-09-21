from PyQt6.QtGui import QColor
from qfluentwidgets import themeColor, isDarkTheme

# 应用主题色: 与 logo 火箭的紫罗兰色调呼应 (覆盖 qfluentwidgets 默认青色)
APP_THEME_COLOR = "#6C5CE7"


def _mix(base: QColor, other: QColor, factor: float) -> QColor:
    """按 factor 将 base 向 other 插值 (0=base, 1=other)。"""
    return QColor(
        int(base.red() + (other.red() - base.red()) * factor),
        int(base.green() + (other.green() - base.green()) * factor),
        int(base.blue() + (other.blue() - base.blue()) * factor),
    )


def versionBadgeStyle() -> str:
    """卡片右上角版本徽章: 使用主题色的柔和底色, 深浅模式自适应。"""
    c = QColor(themeColor())
    if isDarkTheme():
        bg = QColor(c.red(), c.green(), c.blue(), 70)
        fg = _mix(c, QColor(255, 255, 255), 0.55).name()
    else:
        bg = QColor(c.red(), c.green(), c.blue(), 38)
        fg = _mix(c, QColor(0, 0, 0), 0.25).name()
    return (
        f"background-color: {bg.name(QColor.NameFormat.HexArgb)};"
        f"color: {fg};"
        "border-radius: 9px;"
        "padding: 1px 6px;"
        "font-weight: bold;"
    )


def unsupportedBadgeStyle() -> str:
    """暂不支持版本的徽章: 红色警示底色, 深浅模式自适应。"""
    if isDarkTheme():
        bg = "rgba(255, 99, 99, 0.22)"
        fg = "#ff9d9d"
    else:
        bg = "rgba(210, 50, 50, 0.14)"
        fg = "#b22222"
    return (
        f"background-color: {bg};"
        f"color: {fg};"
        "border-radius: 9px;"
        "padding: 1px 6px;"
        "font-weight: bold;"
    )


def warningBannerStyle() -> str:
    """首页更新警告条: 琥珀色提示, 深浅模式自适应。"""
    if isDarkTheme():
        return (
            "color: #f0c674;"
            "background-color: rgba(255, 193, 7, 0.14);"
            "border: 1px solid rgba(255, 193, 7, 0.35);"
            "border-radius: 8px;"
            "padding: 6px 12px;"
            "font-weight: bold;"
        )
    return (
        "color: #9a6700;"
        "background-color: rgba(255, 173, 51, 0.18);"
        "border: 1px solid rgba(255, 173, 51, 0.45);"
        "border-radius: 8px;"
        "padding: 6px 12px;"
        "font-weight: bold;"
    )


def separatorStyle() -> str:
    """卡片内分隔线: 深浅模式自适应。"""
    line = "rgba(255, 255, 255, 0.12)" if isDarkTheme() else "rgba(0, 0, 0, 0.08)"
    return f"color: {line}; background: transparent; border: none;"


def pngListStyle() -> str:
    """扫描结果中 png 资源列表容器: 柔和底色圆角块, 深浅模式自适应。"""
    if isDarkTheme():
        return (
            "background-color: rgba(255, 255, 255, 0.06);"
            "border: 1px solid rgba(255, 255, 255, 0.08);"
            "border-radius: 6px;"
        )
    return (
        "background-color: rgba(0, 0, 0, 0.035);"
        "border: 1px solid rgba(0, 0, 0, 0.06);"
        "border-radius: 6px;"
    )


def summaryBannerStyle() -> str:
    """扫描结果统计条: 主题色柔和底, 深浅模式自适应。"""
    c = QColor(themeColor())
    if isDarkTheme():
        bg = QColor(c.red(), c.green(), c.blue(), 46)
        fg = _mix(c, QColor(255, 255, 255), 0.6).name()
    else:
        bg = QColor(c.red(), c.green(), c.blue(), 28)
        fg = _mix(c, QColor(0, 0, 0), 0.3).name()
    return (
        f"background-color: {bg.name(QColor.NameFormat.HexArgb)};"
        f"color: {fg};"
        "border-radius: 8px;"
        "padding: 8px 14px;"
        "font-weight: bold;"
    )
