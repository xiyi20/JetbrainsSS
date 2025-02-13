import os.path
import shutil
import zipfile
from enum import Enum
from zipfile import ZipFile
from tempfile import mkdtemp


class JarEditor:
    @staticmethod
    def edit(logoPath: [], IDE: Enum):
        tempPath = mkdtemp()
        try:
            jarPath = IDE.value[:IDE.value.index("\\")]
            targetPath = IDE.value[IDE.value.index("\\"):]
            shutil.copy(jarPath, jarPath + ".bak")

            with ZipFile(jarPath) as jar:
                jar.extractall(tempPath)
                jar.close()

            target1 = tempPath+targetPath
            target2 = target1[:target1.rfind(".")]+"@2x"+target1[target1.rfind("."):]

            for target in [target1, target2]:
                if os.path.exists(target) and os.path.isfile(target):
                    os.remove(target)

            shutil.copy(logoPath[0], target1)
            shutil.copy(logoPath[1], target2)

            jarName = jarPath[jarPath.rfind("/")+1:]
            with ZipFile(jarName,"w",zipfile.ZIP_DEFLATED) as jar:
                for root, dirs, files in os.walk(tempPath):
                    for file in files:
                        filePath = os.path.join(root, file)
                        arcName = os.path.relpath(filePath, start=tempPath)
                        jar.write(filePath, arcName)
            os.remove(jarPath)
            shutil.move(jarName,"C:/Users/dxcxy/Desktop")
        finally:
            shutil.rmtree(tempPath)

    @staticmethod
    def restore(IDE: Enum):
        pass


class A(Enum):
    a = "C:/Users/dxcxy/Desktop/product.jar\\idea_logo.png"


JarEditor.edit([r"C:\Users\dxcxy\Desktop\1.jpg",r"C:\Users\dxcxy\Desktop\2.jpg"], A.a)
