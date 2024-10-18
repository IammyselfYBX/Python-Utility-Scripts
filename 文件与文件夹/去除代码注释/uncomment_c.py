import re
import os
import readline  # 支持终端 Tab 补全
import glob      # 文件路径匹配

def complete_path(text, state):
    """
    实现文件路径的 Tab 补全。
    """
    results = glob.glob(text + '*') + [None]
    return results[state]

# 注册路径补全函数
readline.set_completer(complete_path)
readline.parse_and_bind("tab: complete")

def extract_comments(file_content):
    """
    提取 C/C++ 代码中的注释：
    - 单行注释：行首或行尾有空格/TAB 后的 // 注释。
    - 多行注释：/* ... */ 包裹的注释。
    """
    # 单行注释：支持行首或行内的注释，确保 '//' 前面有空格或 TAB
    single_line_pattern = r"(?m)^\s*//.*$|(?<=\s)//.*$"
    
    # 多行注释：匹配 /* ... */ 的块注释
    multi_line_pattern = r"(?s)/\*.*?\*/"

    # 提取所有注释
    single_line_comments = re.findall(single_line_pattern, file_content)
    multi_line_comments = re.findall(multi_line_pattern, file_content)

    # 返回所有非空注释
    return [comment for comment in (single_line_comments + multi_line_comments) if comment.strip()]

def list_comments_with_index(comments):
    """
    列出所有注释，并为每条注释标上序号。
    """
    print("检测到以下注释：")
    for idx, comment in enumerate(comments, 1):
        print(f"{idx}. {repr(comment.strip())}")

def get_comments_to_keep(comments):
    """
    询问用户哪些注释需要保留，默认全部删除。
    """
    user_input = input("输入需要保留的注释编号（用逗号分隔），直接回车全部删除： ")
    if not user_input.strip():
        return []

    try:
        indices = [int(x) - 1 for x in user_input.split(',')]
        return [comments[i] for i in indices if 0 <= i < len(comments)]
    except ValueError:
        print("输入格式不正确，将默认删除所有注释。")
        return []

def remove_comments(file_content, comments_to_keep):
    """
    删除所有未保留的注释，并返回清理后的文件内容。
    """
    all_comments = extract_comments(file_content)

    for comment in all_comments:
        if comment not in comments_to_keep:
            file_content = file_content.replace(comment, '', 1)

    return file_content

def clean_file(input_file):
    """
    主函数：读取文件、处理注释、生成新文件。
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        file_content = f.read()

    comments = extract_comments(file_content)

    if not comments:
        print("未检测到任何注释。")
        return

    list_comments_with_index(comments)
    comments_to_keep = get_comments_to_keep(comments)

    cleaned_content = remove_comments(file_content, comments_to_keep)

    # 生成新文件名：原文件名(去除后缀)_clean.[原后缀名]
    base_name, ext = os.path.splitext(input_file)
    new_file_name = f"{base_name}_clean{ext}"

    with open(new_file_name, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"处理完成，新文件已保存为：{new_file_name}")

if __name__ == "__main__":
    input_file = input("请输入要处理的 C/C++ 文件路径： ")
    if os.path.isfile(input_file):
        clean_file(input_file)
    else:
        print("文件不存在，请检查路径是否正确。")


