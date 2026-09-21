import os
import re
from zipfile import ZipFile, BadZipFile

# 匹配 jar 内部文件名(不含路径)形如 *logo*.png 的条目, 大小写不敏感
LOGO_PNG = re.compile(r"logo", re.IGNORECASE)


def scanJar(jarPath: str) -> list:
    """返回 jar 内所有文件名匹配 *logo*.png 的条目路径列表。"""
    matches = []
    try:
        with ZipFile(jarPath, "r") as zf:
            for name in zf.namelist():
                base = name.rsplit("/", 1)[-1]
                if base.lower().endswith(".png") and LOGO_PNG.search(base):
                    matches.append(name)
    except (BadZipFile, OSError):
        return []
    return matches


def scanDirectory(root: str):
    """遍历 root 下所有 .jar, 逐个产出 (jarPath, [pngName, ...])。

    生成器形式便于调用方在扫描过程中更新进度/取消。
    """
    jars = []
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            if f.lower().endswith(".jar"):
                jars.append(os.path.join(dirpath, f))
    total = len(jars)
    for i, jar in enumerate(sorted(jars), start=1):
        yield i, total, jar, scanJar(jar)
