import os
import zipfile

def zip_file(file_path):
    """将文件压缩为.zip格式"""
    zip_name = f"{file_path}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    print(f"{file_path} 已成功压缩为 {zip_name}")

def find_and_zip_large_files(folder_path, size_limit=100 * 1024 * 1024):
    """查找并压缩大于size_limit的文件"""
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > size_limit:
                try:
                    zip_file(file_path)
                except Exception as e:
                    print(f"压缩 {file_path} 时出错: {e}")

if __name__ == "__main__":
    folder_path = input("请输入要遍历的文件夹路径：")
    find_and_zip_large_files(folder_path)
