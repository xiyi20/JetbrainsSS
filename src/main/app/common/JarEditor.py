import os.path
import shutil
from enum import Enum
from zipfile import ZipFile

from src.main.app.common.RwConfig import RwConfig


class JarEditor:
    @staticmethod
    def edit(logoPath: [], baseDir: str, IDE: Enum):
        jarPath = f"{baseDir}{IDE.value[0]}"
        targetPath = IDE.value[1]
        tempJar = jarPath + ".tmp"
        try:
            JarEditor.restore(baseDir, IDE)
            shutil.copy(jarPath, jarPath + ".bak")
            print("备份文件创建成功")
            targets = [
                targetPath,
                targetPath[:targetPath.rfind(".")] + "@2x" + targetPath[targetPath.rfind("."):]
            ]
            with ZipFile(jarPath, "r") as old:
                with ZipFile(tempJar, "w") as new:
                    for file in old.infolist():
                        fileName = file.filename
                        if fileName in targets:
                            with open(logoPath[targets.index(fileName)], "rb") as logo:
                                data = logo.read()
                        else:
                            data = old.read(fileName)
                        new.writestr(file, data, compress_type=file.compress_type)
            shutil.move(tempJar, jarPath)
            print("splash修补成功")
            JarEditor.clearCache(IDE)
        except Exception as e:
            print(f"修改出错:\n{e}")
            JarEditor.restore(baseDir, IDE)
            print("-" * 10)
        finally:
            if os.path.exists(tempJar) and os.path.isfile(tempJar):
                os.remove(tempJar)

    @staticmethod
    def restore(baseDir: str, IDE: Enum):
        jarPath = baseDir + IDE.value[0]
        bakPath = jarPath + ".bak"
        if os.path.exists(jarPath) and os.path.isfile(bakPath):
            shutil.move(bakPath, jarPath)
            print("已还原备份文件")
            JarEditor.clearCache(IDE)
        else:
            print("当前没有备份文件")

    @staticmethod
    def clearCache(IDE: Enum):
        cachePath = f"C:/Users/{os.getlogin()}/AppData/Local/JetBrains/"
        version = RwConfig().config["IDE"][IDE.name]["version"]
        for directory in os.listdir(cachePath):
            if IDE.name in directory and directory.endswith(version):
                cachePath = f"{cachePath}{directory}/splash"
                if os.path.exists(cachePath) and os.path.isdir(cachePath):
                    for filename in os.listdir(cachePath):
                        if filename.endswith(".ij"):
                            os.remove(os.path.join(cachePath, filename))
                break
        print("缓存清理成功")
