import os.path
import shutil
from enum import Enum
from zipfile import ZipFile


class JarEditor:
    @staticmethod
    def edit(logoPath: [], IDE: Enum):
        jarPath = IDE.value[0]
        targetPath = IDE.value[1]
        tempJar = jarPath + ".tmp"
        try:
            JarEditor.restore(IDE)
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
                        else: data = old.read(fileName)
                        new.writestr(file, data, compress_type=file.compress_type)
            shutil.move(tempJar, jarPath)
            cachePath = f"C:/Users/{os.getlogin()}/AppData/Local/JetBrains/"
            print("splash修补成功")
        except Exception as e:
            shutil.copy(jarPath + ".bak", jarPath)
            print(e)
        finally:
            if os.path.exists(tempJar) and os.path.isfile(tempJar):
                os.remove(tempJar)

    @staticmethod
    def restore(IDE: Enum):
        jarPath = IDE.value[0]
        bakPath = jarPath + ".bak"
        if os.path.exists(jarPath) and os.path.isfile(bakPath):
            shutil.move(bakPath, jarPath)
        else:
            print("当前没有备份文件")


class A(Enum):
    a = ["C:/Users/dxcxy/Desktop/app.jar","artwork/webide_logo.png"]


JarEditor.edit([r"C:\Users\dxcxy\Desktop\idea_logo.png", r"C:\Users\dxcxy\Desktop\idea_logo@2x.png"], A.a)

# JarEditor.restore(A.a)