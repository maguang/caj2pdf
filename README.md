# CAJ to PDF
## 中国知网CAJ/KDH/NH批量转PDF技术方案

中国知网有CAJ/KDH/NH三种特殊格式，只能使用官方的阅读器阅读，兼容性较差。网上现有各种方案，或有以下弊端：
1. 不能完全转换
2. 转换后体积膨胀太大
3. 无法保留原始的文本层
4. 无法批量处理

经过尝试，终于摸索到了批量将中国知网CAJ/KDH/NH三种特殊格式转成PDF的较好方式（以Windows操作系统为例）：

---

## 📋 方案步骤

### 第一步：收集文件
使用Python脚本（[01提取CAJ.py](https://github.com/maguang/caj2pdf/blob/main/01%E6%8F%90%E5%8F%96caj%20.py)），批量自动遍历识别并移动CAJ/KDH/NH文件到指定文件夹，并将文件的原始位置保存到JSON文件。

**依赖要求**：
- [Python](https://www.python.org/) 3.6+
- 无需额外库（仅使用标准库）

**使用方法**：
1. 修改脚本中的配置（源目录、目标目录等）
2. 运行脚本：`python 01提取CAJ.py`

### 第二步：转换格式
打开官方的全球学术快报软件，从第一步的目标文件夹批量导入，导出为PDF格式。

**软件要求**：
- 全球学术快报（[中国知网官方下载](https://m.cnki.net/mcnkidown/down.html)）

**操作步骤**：
1. 打开全球学术快报软件
2. 选择"导入"功能，导入第一步生成的文件夹中的所有文件
3. 全选导入的文件，点击右边隐藏的...按钮，选择"导出为PDF"
4. 将PDF文件保存到指定目录（建议与第一步的目标目录同级，命名为`output_pdfs`）

### 第三步：回迁PDF
使用Python脚本（[02回迁PDF.py](https://github.com/maguang/caj2pdf/blob/main/02%E5%9B%9E%E8%BF%81PDF.py)），读取第一步保存的JSON文件，将PDF移动到对应的CAJ原位置。成功后，删除CAJ即可。

**依赖要求**：
- [Python](https://www.python.org/) 3.6+
- 无需额外库（仅使用标准库）

**使用方法**：
1. 确保PDF文件已生成在指定目录（如`output_pdfs`）
2. 修改脚本中的配置（PDF目录、JSON文件路径等）
3. 运行脚本：`python 02回迁PDF.py`

---

## ✅ 方案优点

1. **官方工具**：基本上可以全部成功转换CAJ
2. **体积最小**：避免体积膨胀，且可以保留原文件中的文本层
3. **速度快**：且不易出错
4. **代码简单**：避免调用旧版[caj2pdf](https://github.com/caj2pdf/caj2pdf)的复杂且常出错的过程
5. **跨平台**：适用于多种操作系统

以上方案，完全可以避免[CAJViewer](https://cajviewer.cnki.net/)、[caj2pdf-qt](https://github.com/sainnhe/caj2pdf-qt)等软件的不足之处。个人认为，这可能目前较佳的解决方案。当然，您若有更好的方案，还请赐教！

---

## ⚠️ 注意事项

- 本人为菜鸟，无法解答高难度问题，有问题请直接问高手或AI，谢谢！

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
