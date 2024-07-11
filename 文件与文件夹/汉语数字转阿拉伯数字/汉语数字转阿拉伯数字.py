import os
import re

# 定义中文数字到阿拉伯数字的映射
zh_num_map = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '百': 100, '千': 1000, '万': 10000
}

# 将中文数字转换为阿拉伯数字
def zh_num_to_arabic(zh_num):
    result = 0
    temp = 0
    count = 0

    for char in zh_num:
        if char in zh_num_map:
            digit = zh_num_map[char]
            if digit == 10 or digit == 100 or digit == 1000 or digit == 10000:
                if temp == 0:
                    temp = 1
                result += temp * digit
                temp = 0
                count = 0
            else:
                temp = temp * 10 ** count + digit
                count += 1
        else:
            result += temp
            temp = 0

    result += temp
    return str(result)

# 定义正则表达式模式，匹配中文数字
pattern = re.compile(r'[零一二三四五六七八九十百千万]+')

def convert_zh_num_to_en(name):
    return pattern.sub(lambda match: zh_num_to_arabic(match.group(0)), name)

def rename_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for name in dirs + files:
            new_name = convert_zh_num_to_en(name)
            if new_name != name:
                os.rename(os.path.join(root, name), os.path.join(root, new_name))
                print(f'Renamed: {name} -> {new_name}')

# 指定目标文件夹路径
target_directory = r'D:\BaiduNetdiskDownload\高数叔\0004 高数叔-c语言(2小时速成)'

rename_files_in_directory(target_directory)
