import os


# 创建文件夹
def createFolder(folder_name):
    folder_name = str(folder_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


# 删除文件夹及其下所有文件
def deleteFolderAndFile(folder_path):
    for root, dirs, files in os.walk(folder_path):
        # 删除文件
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        # 删除文件夹
        os.rmdir(folder_path)
