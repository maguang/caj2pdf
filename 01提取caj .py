# Copyright (c) 2025 马光
# MIT License - see LICENSE file for details
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

    print(f'收集完成，共移动 {moved_count} 个文件至 {TARGET_DIR}，下一步请使用全球学术快报软件将CAJ/KDH/NH文件批量转成PDF：打开软件，全部文献→导入→选择文件→批量操作→点击右边隐藏的...按钮→导出PDF→选择存放的文件夹。文件多的话，可能会需要一些时间，请耐心等待。')


if __name__ == '__main__':

    collect_cnki_files()
