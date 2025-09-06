# -*- coding: utf-8 -*-
import os
import shutil
import json

# ================== 配置区域 ==================
PDF_DIR = r'D:\cnki_files'  # PDF所在目录
# 从自定义位置读取映射文件，一定要和生成的文件保持一致！
PATH_MAP_FILE = r'D:\test\cnki_path_map.json'
# ================== 配置结束 ==================


def move_pdfs_back():
    """将PDF文件移动回原始目录"""
    # 读取映射文件
    try:
        with open(PATH_MAP_FILE, 'r', encoding='utf-8') as f:
            path_map = json.load(f)
        print(f'成功读取映射文件，共 {len(path_map)} 条记录')
    except Exception as e:
        print(f'读取映射文件失败: {e}')
        return

    # 确保PDF目录存在
    if not os.path.exists(PDF_DIR):
        print(f'PDF目录不存在: {PDF_DIR}')
        return

    moved_count = 0
    failed_count = 0

    # 遍历PDF目录中的所有文件
    for pdf_file in os.listdir(PDF_DIR):
        if pdf_file.lower().endswith('.pdf'):
            # 获取PDF文件的基础名称（去掉.pdf扩展名）
            pdf_base_name = pdf_file[:-4]
            
            # 在映射表中查找对应的原始文件
            original_file = None
            original_path = None
            
            # 尝试精确匹配
            for ext in ['caj', 'nh', 'kdh']:
                candidate_file = pdf_base_name + ext
                if candidate_file in path_map:
                    original_file = candidate_file
                    original_path = path_map[candidate_file]
                    break
            
            if original_file and original_path:
                try:
                    # 获取原始文件所在目录
                    target_dir = os.path.dirname(original_path)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # 移动PDF文件
                    src_pdf = os.path.join(PDF_DIR, pdf_file)
                    dst_pdf = os.path.join(target_dir, pdf_file)
                    
                    shutil.move(src_pdf, dst_pdf)
                    moved_count += 1
                    print(f'✅ 已移动: {pdf_file} -> {target_dir}')
                    
                except Exception as e:
                    failed_count += 1
                    print(f'❌ 移动失败: {pdf_file}, 错误: {e}')
            else:
                failed_count += 1
                print(f'❌ 未找到原始文件映射: {pdf_file}')
                print(f'   可选的原始文件名: {pdf_base_name}.caj, {pdf_base_name}.nh, {pdf_base_name}.kdh')

    print(f'\n回迁完成:')
    print(f'✅ 成功移动: {moved_count} 个文件')
    print(f'❌ 失败: {failed_count} 个文件')


if __name__ == '__main__':
    move_pdfs_back()