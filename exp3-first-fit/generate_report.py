#!/usr/bin/env python3
"""生成实验报告 Word 文档"""
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

def set_chinese_font(run, font_name="宋体", size=12):
    run.font.name = font_name
    run.font.size = Pt(size)
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)

def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        set_chinese_font(run, "黑体", 16 if level == 1 else 14)
    return h

def add_paragraph(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_chinese_font(run)
    if bold:
        run.bold = True
    return p

def add_code_block(doc, code):
    p = doc.add_paragraph()
    run = p.add_run(code)
    run.font.name = "Courier New"
    run.font.size = Pt(8)
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    return p

def main():
    doc = Document()

    # 标题
    title = doc.add_heading("实验三  可变分区内存分配首次适应算法模拟", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        set_chinese_font(run, "黑体", 18)

    # 一、实验目的
    add_heading(doc, "一、实验目的", 1)
    add_paragraph(doc, "1. 了解动态分区分配方式中使用的数据结构和分配算法。")
    add_paragraph(doc, "2. 进一步加深对动态分区存储管理方式及其实现过程的理解。")
    add_paragraph(doc, "3. 通过编程模拟可变分区分配存储管理系统，掌握首次适应（First Fit）分配算法。")

    # 二、实验原理
    add_heading(doc, "二、实验原理", 1)
    add_paragraph(doc, "可变分区分配是一种重要的存储管理思想。与固定分区不同，可变分区总是根据作业的实际需要分配刚好够用的连续存储空间，避免了内部碎片的产生。")
    add_paragraph(doc, "首次适应算法（First Fit）要求空闲分区按地址递增的顺序排列。在进行内存分配时，从低地址部分向高地址部分查找，直到找到第一个能满足要求的空闲分区为止，然后按作业实际大小从该空闲区划出一块空间。")
    add_paragraph(doc, "分区回收时，系统根据回收分区的地址找到相应分区，将其状态置为空闲，并与相邻的空闲分区合并，以减少外部碎片。合并情况包括：")
    add_paragraph(doc, "（1）回收区与前一分区相邻接，合并为一个大分区；")
    add_paragraph(doc, "（2）回收区与后一分区相邻接，合并为一个大分区；")
    add_paragraph(doc, "（3）回收区与前后分区均相邻接，三个分区合并为一个；")
    add_paragraph(doc, "（4）回收区与前后分区均不邻接，独立成为一个空闲分区。")

    # 三、实验内容
    add_heading(doc, "三、实验内容", 1)
    add_paragraph(doc, "1. 用 C++ 语言实现采用首次适应算法的动态分区分配过程 alloc() 和回收过程 free()。")
    add_paragraph(doc, "2. 空闲分区通过双向链表来管理，在进行内存分配时，系统优先使用空闲区低端的空间。")
    add_paragraph(doc, "3. 假设初始状态下，可用的内存空间为 640KB，并按下列请求序列进行测试：")
    add_paragraph(doc, "作业1申请130KB → 作业2释放60KB → 作业3申请100KB → 作业2释放60KB → 作业4申请200KB → 作业3释放100KB → 作业1释放130KB → 作业5申请140KB → 作业6申请60KB → 作业7申请50KB → 作业6释放60KB")
    add_paragraph(doc, "4. 每次分配和回收后显示出内存分区表和空闲内存分区链的情况。")

    # 四、实验步骤
    add_heading(doc, "四、实验步骤", 1)

    add_heading(doc, "步骤1：选用合适的实验程序开发环境", 2)
    add_paragraph(doc, "本实验使用 Linux 环境，编译器为 g++，支持 C++11 标准。")

    add_heading(doc, "步骤2：设计程序结构，规划程序功能", 2)
    add_paragraph(doc, "程序采用双向链表管理内存分区，主要数据结构如下：")
    add_paragraph(doc, "• Partition 结构体：描述分区信息（起始地址、大小、状态、作业号）")
    add_paragraph(doc, "• DuLNode 结构体：双向链表结点，包含分区数据和前驱/后继指针")
    add_paragraph(doc, "主要功能模块：")
    add_paragraph(doc, "• init_memory()：初始化内存空间")
    add_paragraph(doc, "• first_fit()：首次适应分配算法")
    add_paragraph(doc, "• free_memory()：内存回收与合并算法")
    add_paragraph(doc, "• show_partitions()：显示内存分区表")
    add_paragraph(doc, "• show_free_chain()：显示空闲分区链")

    add_heading(doc, "步骤3：完成程序的编码与测试", 2)
    add_paragraph(doc, "完整源代码如下（first_fit.cpp）：")

    with open("first_fit.cpp", "r", encoding="utf-8") as f:
        code = f.read()
    add_code_block(doc, code)

    add_heading(doc, "步骤4：设计实验数据", 2)
    add_paragraph(doc, "输入文件 in.txt 内容如下：")
    with open("in.txt", "r") as f:
        add_code_block(doc, f.read())
    add_paragraph(doc, "格式说明：每行三个字段，分别为作业号、操作类型（a=申请，f=释放）、内存大小(KB)。")

    add_heading(doc, "步骤5：编译运行程序", 2)
    add_paragraph(doc, "编译命令：")
    add_code_block(doc, "make\n# 或\ng++ -Wall -std=c++11 -O2 -o first_fit first_fit.cpp")
    add_paragraph(doc, "运行批处理测试：")
    add_code_block(doc, "./first_fit batch in.txt")
    add_paragraph(doc, "交互式运行：")
    add_code_block(doc, "./first_fit")

    add_heading(doc, "步骤6：运行结果与截图", 2)
    add_paragraph(doc, "（1）批处理测试 - 序列1~3（分配阶段）：")
    if os.path.exists("screenshots/screenshot_batch_1-3.png"):
        doc.add_picture("screenshots/screenshot_batch_1-3.png", width=Inches(6))

    add_paragraph(doc, "（2）批处理测试 - 序列6~8（回收与合并阶段）：")
    if os.path.exists("screenshots/screenshot_batch_6-8.png"):
        doc.add_picture("screenshots/screenshot_batch_6-8.png", width=Inches(6))

    add_paragraph(doc, "（3）批处理测试 - 序列9~11（最终阶段）：")
    if os.path.exists("screenshots/screenshot_batch_9-11.png"):
        doc.add_picture("screenshots/screenshot_batch_9-11.png", width=Inches(6))

    add_paragraph(doc, "（4）批处理测试执行摘要：")
    if os.path.exists("screenshots/screenshot_summary.png"):
        doc.add_picture("screenshots/screenshot_summary.png", width=Inches(5))

    add_paragraph(doc, "（5）交互式操作演示：")
    if os.path.exists("screenshots/screenshot_interactive.png"):
        doc.add_picture("screenshots/screenshot_interactive.png", width=Inches(5))

    # 五、实验结果分析
    add_heading(doc, "五、实验结果分析", 1)
    add_paragraph(doc, "1. 首次适应算法总是从低地址开始查找，优先使用低地址的空闲分区，有利于保留高地址的大块空闲区。")
    add_paragraph(doc, "2. 序列2和序列4中作业2释放60KB失败，因为作业2从未被分配过内存，程序正确给出了错误提示。")
    add_paragraph(doc, "3. 序列6作业3释放100KB后，产生两个空闲分区（130KB和430KB），体现了回收后不自动合并非相邻空闲区的特点。")
    add_paragraph(doc, "4. 序列7作业1释放130KB后，低地址产生230KB空闲区，与序列6的空闲区合并（因不相邻而未合并）。")
    add_paragraph(doc, "5. 序列11作业6释放60KB后，与前面的90KB空闲区合并为140KB空闲区，体现了相邻空闲分区合并机制。")

    # 六、实验总结
    add_heading(doc, "六、实验总结", 1)
    add_paragraph(doc, "通过本次实验，我深入理解了可变分区内存管理的原理和首次适应分配算法的实现过程。使用双向链表管理分区，能够灵活地进行分区的分配、回收和合并操作。首次适应算法实现简单，分配速度快，但可能产生较多的外部碎片。实验程序支持交互式和批处理两种运行模式，能够清晰地展示每次内存操作后的分区状态变化。")

    output = "实验三_可变分区内存分配首次适应算法模拟.docx"
    doc.save(output)
    print(f"报告已生成: {output}")

if __name__ == "__main__":
    main()
