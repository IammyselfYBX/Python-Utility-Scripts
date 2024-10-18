import re
import os
import readline  # 用于支持终端输入的 Tab 补全
import glob      # 用于文件路径匹配

def complete_path(text, state):
    """
    实现路径的 Tab 补全。
    """
    results = glob.glob(text + '*') + [None]
    return results[state]

# 注册路径补全函数
readline.set_completer(complete_path)
readline.parse_and_bind("tab: complete")

def extract_comments(file_content):
    multi_line_pattern = r"(?s)('''.*?'''|\"\"\".*?\"\"\")"
    single_line_pattern = r"(?m)(^\s*#.*$|\s+#.*$)"

    multi_line_comments = re.findall(multi_line_pattern, file_content)
    cleaned_content = re.sub(multi_line_pattern, '', file_content)
    single_line_comments = re.findall(single_line_pattern, cleaned_content)

    return [comment for comment in (multi_line_comments + single_line_comments) if comment.strip()]

def list_comments_with_index(comments):
    print("检测到以下注释：")
    for idx, comment in enumerate(comments, 1):
        print(f"{idx}. {repr(comment.strip())}")

def get_comments_to_keep(comments):
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
    all_comments = extract_comments(file_content)

    for comment in all_comments:
        if comment not in comments_to_keep:
            file_content = file_content.replace(comment, '', 1)

    return file_content

def clean_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        file_content = f.read()

    comments = extract_comments(file_content)

    if not comments:
        print("未检测到任何注释。")
        return

    list_comments_with_index(comments)
    comments_to_keep = get_comments_to_keep(comments)

    cleaned_content = remove_comments(file_content, comments_to_keep)

    new_file_name = os.path.splitext(input_file)[0] + "_clean.py"
    with open(new_file_name, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"处理完成，新文件已保存为：{new_file_name}")

if __name__ == "__main__":
    input_file = input("请输入要处理的 Python 文件路径： ")
    if os.path.isfile(input_file):
        clean_file(input_file)
    else:
        print("文件不存在，请检查路径是否正确。")


