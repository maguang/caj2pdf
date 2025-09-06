# CAJ to PDF
#中国知网CAJ/KDH/NH批量转PDF的技术方案

中国知网有CAJ/KDH/NH三种特殊格式，只能使用官方的阅读器阅读，兼容性太差，非常令人恼火。早些年曾经下载了一大批这样的文件，现在因为要批量处理成文本数据，不得不将其批量转成PDF文件。网上看了各种方案，但有几个弊端：1）不能完全转换；2）转换后体积膨胀太大；3）无法保留原始的文本层；4）无法批量处理。

今天，经过尝试，终于摸索到了批量将中国知网CAJ/KDH/NH三种特殊格式转成PDF的较好方式：

第一步：python脚本，批量自动遍历识别并移动CAJ/KDH/NH文件到A文件夹，并将文件的原始位置保存到json文件。

第二步：打开官方的全球学术快报软件，从A文件夹批量导入，导出为PDF格式。

第三步：python脚本，读取保存的json文件，将PDF移动到对应的CAJ原位置。成功后，删除CAJ即可。

这种方案的优点：

1）官方工具，基本上可以全部成功转换CAJ。

2）体积最小，避免体积膨胀，且可以保留原文件中的文本层。

3）速度快，且不易出错。

4）代码简单，避免调用旧版caj2pdf的复杂且常出错的过程。

5）适用于多种操作系统。

以上方案，完全可以避免cajviewer、caj2pdf-qt等软件的弊端。个人认为，这可能目前最佳的解决方案。当然，您若有更好的方案，还请赐教！

附：代码
###########第一步代码###########
# -*- coding: utf-8 -*-
import os
import shutil
import json

# ================== 配置区域 ==================
# 请根据实际情况修改以下配置

# 源文件夹列表（可填写多个需要扫描的根目录）
SOURCE_DIRS = [
    r'D:\test',
    #r'E:\test',
    # 可继续添加更多目录...
]

# 目标目录（所有收集到的文件将集中存放于此）
TARGET_DIR = r'D:\cnki_files'

# 需要收集的文件扩展名列表（支持中国知网特有格式）
TARGET_EXTENSIONS = ['.caj', '.nh', '.kdh']  # 可自行增删

# 是否生成文件路径映射日志（用于第三步PDF回迁）
GENERATE_PATH_MAP = True
# 自定义映射文件保存位置
PATH_MAP_FILE = r'D:\test\cnki_path_map.json'

# ================== 配置结束 ==================


def collect_cnki_files():
    """收集指定目录下的所有目标格式文件到统一目录"""
    os.makedirs(TARGET_DIR, exist_ok=True)
    # 确保映射文件所在目录存在
    if GENERATE_PATH_MAP:
        os.makedirs(os.path.dirname(PATH_MAP_FILE), exist_ok=True)
    
    path_map = {}
    moved_count = 0

    for dir_path in SOURCE_DIRS:
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in TARGET_EXTENSIONS:
                    src = os.path.join(root, file)
                    dst = os.path.join(TARGET_DIR, file)
                    
                    # 记录原始路径到映射表
                    path_map[file] = src
                    
                    # 移动文件（而不是复制）
                    try:
                        shutil.move(src, dst)
                        moved_count += 1
                        print(f'已移动: {src} -> {dst}')
                    except Exception as e:
                        print(f'移动失败: {src} -> {dst}, 错误: {e}')

    if GENERATE_PATH_MAP and path_map:
        with open(PATH_MAP_FILE, 'w', encoding='utf-8') as f:
            json.dump(path_map, f, ensure_ascii=False, indent=4)
        print(f'文件路径映射已保存至: {PATH_MAP_FILE}')

    print(f'收集完成，共移动 {moved_count} 个文件至 {TARGET_DIR}')


if __name__ == '__main__':
    collect_cnki_files()


#######第三步代码






