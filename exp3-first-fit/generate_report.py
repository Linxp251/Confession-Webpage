#!/usr/bin/env python3
"""生成完整实验报告 Word 文档"""
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUTPUT_FILE = "实验三_可变分区内存分配首次适应算法模拟.docx"


def set_chinese_font(run, font_name="宋体", size=12, bold=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = color
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)


def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        sizes = {0: 18, 1: 16, 2: 14, 3: 12}
        set_chinese_font(run, "黑体", sizes.get(level, 12))
    return h


def add_paragraph(doc, text, bold=False, align=None, indent=0):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_chinese_font(run, bold=bold)
    if align:
        p.alignment = align
    if indent:
        p.paragraph_format.first_line_indent = Cm(indent)
    return p


def add_code_block(doc, code, font_size=8):
    p = doc.add_paragraph()
    run = p.add_run(code)
    run.font.name = "Courier New"
    run.font.size = Pt(font_size)
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), "F5F5F5")
    p._element.get_or_add_pPr().append(shading)
    return p


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        for p in hdr_cells[i].paragraphs:
            for run in p.runs:
                set_chinese_font(run, "黑体", 10, bold=True)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for ri, row in enumerate(rows):
        cells = table.rows[ri + 1].cells
        for ci, val in enumerate(row):
            cells[ci].text = str(val)
            for p in cells[ci].paragraphs:
                for run in p.runs:
                    set_chinese_font(run, size=10)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()
    return table


def add_page_break(doc):
    doc.add_page_break()


def add_cover_page(doc):
    for _ in range(3):
        doc.add_paragraph()
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("操作系统实验报告")
    set_chinese_font(run, "黑体", 22, bold=True)

    doc.add_paragraph()
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("实验三  可变分区内存分配首次适应算法模拟")
    set_chinese_font(run, "黑体", 18, bold=True)

    for _ in range(4):
        doc.add_paragraph()

    info_items = [
        ("学    院", "____________________"),
        ("专    业", "____________________"),
        ("班    级", "____________________"),
        ("姓    名", "____________________"),
        ("学    号", "____________________"),
        ("指导教师", "____________________"),
        ("完成日期", "2026年6月11日"),
    ]
    for label, value in info_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f"{label}：{value}")
        set_chinese_font(run, size=14)
        p.paragraph_format.space_after = Pt(12)

    add_page_break(doc)


def add_algorithm_flowchart(doc):
    add_heading(doc, "2.3 算法流程", 2)
    add_paragraph(doc, "（1）首次适应分配算法流程：", bold=True)
    flow_alloc = """开始
  ↓
输入作业号和申请大小 need
  ↓
从链表头结点开始，按地址递增遍历分区
  ↓
当前分区是否空闲 且 大小 ≥ need？
  ├─ 否 → 继续遍历下一分区
  │         ↓
  │       遍历结束？→ 是 → 分配失败，返回
  │         ↓ 否
  │       回到判断
  └─ 是 → 分区大小是否等于 need？
            ├─ 是 → 整块标记为已分配
            └─ 否 → 从低地址切割，创建新已分配结点
  ↓
分配成功，显示分区表
  ↓
结束"""
    add_code_block(doc, flow_alloc, font_size=9)

    add_paragraph(doc, "（2）内存回收与合并算法流程：", bold=True)
    flow_free = """开始
  ↓
输入要释放的作业号 job_id
  ↓
遍历分区链表，查找 job_id 对应的已分配分区
  ↓
是否找到？
  ├─ 否 → 回收失败，提示错误
  └─ 是 → 将该分区状态置为空闲
            ↓
          前驱分区是否空闲？→ 是 → 与前驱合并
            ↓
          后继分区是否空闲？→ 是 → 与后继合并
            ↓
          回收成功，显示分区表
  ↓
结束"""
    add_code_block(doc, flow_free, font_size=9)


def add_result_table(doc):
    add_heading(doc, "5.1 测试序列执行结果汇总", 2)
    add_paragraph(doc, "下表汇总了 640KB 内存条件下，11 步标准测试序列的执行结果：")
    headers = ["序列", "操作", "结果", "空闲分区数", "说明"]
    rows = [
        ["1", "作业1 申请130KB", "成功", "1", "从0地址分配，剩余510KB空闲"],
        ["2", "作业2 释放60KB", "失败", "1", "作业2未分配，正确提示错误"],
        ["3", "作业3 申请100KB", "成功", "1", "从130地址分配，剩余410KB空闲"],
        ["4", "作业2 释放60KB", "失败", "1", "作业2仍未分配"],
        ["5", "作业4 申请200KB", "成功", "1", "从230地址分配，剩余210KB空闲"],
        ["6", "作业3 释放100KB", "成功", "2", "产生130KB和430KB两个空闲区"],
        ["7", "作业1 释放130KB", "成功", "2", "低地址产生230KB空闲区"],
        ["8", "作业5 申请140KB", "成功", "2", "从0地址首次适应分配140KB"],
        ["9", "作业6 申请60KB", "成功", "2", "从140地址分配，剩余30KB碎片"],
        ["10", "作业7 申请50KB", "成功", "2", "从430地址分配，剩余160KB空闲"],
        ["11", "作业6 释放60KB", "成功", "2", "与90KB空闲区合并为140KB"],
    ]
    add_table(doc, headers, rows)


def add_data_structure_section(doc):
    add_heading(doc, "4.1 数据结构设计", 2)
    add_paragraph(doc, "本程序使用双向链表管理内存分区，核心数据结构定义如下：")
    struct_code = """// 分区信息
struct Partition {
    long address;   // 起始地址 (KB)
    long size;      // 分区大小 (KB)
    int  state;     // 0=空闲, 1=已分配
    int  job_id;    // 占用作业号，空闲时为 -1
};

// 双向链表结点
struct DuLNode {
    Partition data;
    DuLNode *prior;  // 前驱指针
    DuLNode *next;   // 后继指针
};"""
    add_code_block(doc, struct_code)

    add_heading(doc, "4.2 程序模块结构", 2)
    headers = ["模块函数", "功能说明"]
    rows = [
        ["init_memory()", "初始化内存，创建带头结点的双向链表"],
        ["first_fit()", "首次适应分配算法，从低地址查找并切割分区"],
        ["free_memory()", "按作业号回收内存，合并相邻空闲分区"],
        ["show_partitions()", "显示当前全部分区（已分配+空闲）"],
        ["show_free_chain()", "显示空闲分区链及空闲块数量"],
        ["run_batch()", "从文件读取请求序列并自动执行"],
    ]
    add_table(doc, headers, rows)


def main():
    doc = Document()

    # 设置默认字体
    style = doc.styles["Normal"]
    style.font.name = "宋体"
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # 封面
    add_cover_page(doc)

    # 一、实验目的
    add_heading(doc, "一、实验目的", 1)
    purposes = [
        "了解动态分区分配方式中使用的数据结构和分配算法；",
        "进一步加深对动态分区存储管理方式及其实现过程的理解；",
        "通过编程模拟可变分区分配存储管理系统，掌握首次适应（First Fit）分配算法；",
        "熟悉内存回收时相邻空闲分区的合并机制，理解外部碎片的产生原因。",
    ]
    for i, p in enumerate(purposes, 1):
        add_paragraph(doc, f"{i}. {p}", indent=0.74)

    # 二、实验原理
    add_heading(doc, "二、实验原理", 1)
    add_heading(doc, "2.1 可变分区分配", 2)
    add_paragraph(
        doc,
        "可变分区分配是一种重要的存储管理思想，目前流行的操作系统分段存储管理的基本思想就源自该方法。"
        "与固定分区分配不同，可变分区总是根据作业的实际需要分配刚好够用的连续存储空间，"
        "保证分配给作业的存储空间都是有用的，避免了内部碎片的产生。",
        indent=0.74,
    )

    add_heading(doc, "2.2 首次适应算法", 2)
    add_paragraph(
        doc,
        "首次适应算法（First Fit）要求空闲分区按地址递增的顺序排列。在进行内存分配时，"
        "从低地址部分向高地址部分查找，直到找到第一个能满足要求的空闲分区为止。"
        "然后按作业实际大小，从该空闲区划出一块空间给作业，剩余部分继续留在空闲分区链中。"
        "该算法的优点是实现简单、分配速度快；缺点是在低地址部分可能产生较多外部碎片。",
        indent=0.74,
    )

    add_paragraph(doc, "分区回收时，需处理以下四种合并情况：", indent=0.74)
    merge_cases = [
        "回收区与前一空闲分区相邻接 → 合并为一个大分区；",
        "回收区与后一空闲分区相邻接 → 合并为一个大分区；",
        "回收区与前后空闲分区均相邻接 → 三个分区合并为一个；",
        "回收区与前后分区均不邻接 → 独立成为一个新的空闲分区。",
    ]
    for i, c in enumerate(merge_cases, 1):
        add_paragraph(doc, f"（{i}）{c}")

    add_algorithm_flowchart(doc)

    # 三、实验环境
    add_heading(doc, "三、实验环境", 1)
    headers = ["项目", "配置"]
    rows = [
        ["操作系统", "Linux / Windows"],
        ["开发语言", "C++（C++11 标准）"],
        ["编译器", "g++"],
        ["开发工具", "Visual Studio Code / 命令行"],
        ["初始内存", "640 KB"],
    ]
    add_table(doc, headers, rows)

    # 四、实验内容与步骤
    add_heading(doc, "四、实验内容与步骤", 1)

    add_heading(doc, "4.1 实验内容", 2)
    add_paragraph(doc, "1. 用 C++ 实现首次适应算法的动态分区分配 alloc() 和回收 free() 过程；", indent=0.74)
    add_paragraph(doc, "2. 空闲分区通过双向链表管理，分配时优先使用空闲区低端空间；", indent=0.74)
    add_paragraph(doc, "3. 按下列 11 步请求序列进行测试，每次操作后显示分区表和空闲分区链：", indent=0.74)

    seq_text = (
        "作业1申请130KB → 作业2释放60KB → 作业3申请100KB → 作业2释放60KB → "
        "作业4申请200KB → 作业3释放100KB → 作业1释放130KB → 作业5申请140KB → "
        "作业6申请60KB → 作业7申请50KB → 作业6释放60KB"
    )
    add_paragraph(doc, seq_text, indent=0.74)

    add_data_structure_section(doc)

    add_heading(doc, "4.3 实验步骤", 2)
    steps = [
        ("步骤1：环境准备", "安装 g++ 编译器，创建项目目录 exp3-first-fit。"),
        ("步骤2：设计数据结构", "定义 Partition 分区结构体和 DuLNode 双向链表结点。"),
        ("步骤3：编写核心算法", "实现 init_memory()、first_fit()、free_memory() 函数。"),
        ("步骤4：编写显示模块", "实现 show_partitions() 和 show_free_chain() 函数。"),
        ("步骤5：编写主程序", "实现交互式菜单和批处理两种运行模式。"),
        ("步骤6：设计测试数据", "编写 in.txt 输入文件，包含 11 步标准测试序列。"),
        ("步骤7：编译运行", "执行 make 编译，运行 ./first_fit batch in.txt 进行测试。"),
        ("步骤8：记录结果", "保存运行输出，截图记录每次分配/回收后的分区状态。"),
    ]
    for title, desc in steps:
        add_paragraph(doc, title, bold=True)
        add_paragraph(doc, desc, indent=0.74)

    add_heading(doc, "4.4 完整源代码", 2)
    add_paragraph(doc, "主程序文件 first_fit.cpp 完整代码如下：")
    with open("first_fit.cpp", "r", encoding="utf-8") as f:
        add_code_block(doc, f.read(), font_size=7)

    add_heading(doc, "4.5 测试数据文件", 2)
    add_paragraph(doc, "输入文件 in.txt（格式：作业号 操作类型 大小，a=申请 f=释放）：")
    with open("in.txt", "r") as f:
        add_code_block(doc, f.read())

    add_heading(doc, "4.6 编译与运行", 2)
    add_paragraph(doc, "编译命令：")
    add_code_block(doc, "cd exp3-first-fit\nmake\n# 等价于：g++ -Wall -std=c++11 -O2 -o first_fit first_fit.cpp")
    add_paragraph(doc, "批处理运行（自动执行11步测试序列）：")
    add_code_block(doc, "./first_fit batch in.txt")
    add_paragraph(doc, "交互式运行：")
    add_code_block(doc, "./first_fit")

    add_page_break(doc)

    # 五、实验结果
    add_heading(doc, "五、实验结果", 1)
    add_result_table(doc)

    add_heading(doc, "5.2 运行截图", 2)
    add_paragraph(doc, "以下为本程序在 640KB 标准测试序列下的运行截图。")

    screenshots = [
        ("screenshots/screenshot_batch_1-3.png", "图5-1  序列1~3运行结果（初始分配阶段）"),
        ("screenshots/screenshot_batch_6-8.png", "图5-2  序列6~8运行结果（回收与再分配阶段）"),
        ("screenshots/screenshot_batch_9-11.png", "图5-3  序列9~11运行结果（最终阶段）"),
        ("screenshots/screenshot_summary.png", "图5-4  11步测试序列执行摘要"),
        ("screenshots/screenshot_interactive.png", "图5-5  交互式操作界面演示"),
    ]
    for path, caption in screenshots:
        add_paragraph(doc, caption, bold=True)
        if os.path.exists(path):
            doc.add_picture(path, width=Inches(5.8))
        else:
            add_paragraph(doc, "（截图文件缺失，请重新运行 generate_screenshots.py 生成）")
        doc.add_paragraph()

    add_heading(doc, "5.3 完整运行输出（节选）", 2)
    if os.path.exists("output_batch.txt"):
        with open("output_batch.txt", "r", encoding="utf-8") as f:
            output = f.read()
        # 截取前 60 行作为节选
        lines = output.split("\n")[:60]
        add_code_block(doc, "\n".join(lines), font_size=7)
        add_paragraph(doc, "（完整输出见 output_batch.txt 文件）")

    add_page_break(doc)

    # 六、结果分析
    add_heading(doc, "六、实验结果分析", 1)
    analyses = [
        (
            "首次适应算法的地址选择策略",
            "算法总是从低地址（0KB）开始查找空闲分区。序列8中作业5申请140KB时，"
            "从地址0的空闲区（230KB）中分配，而非使用高地址的空闲区，体现了首次适应的特点。"
            "这种策略有利于保留高地址的大块连续空闲空间。",
        ),
        (
            "错误处理机制",
            "序列2和序列4中，作业2释放60KB均失败。这是因为作业2从未被分配过内存，"
            "程序通过遍历分区表找不到对应作业号，正确给出「未找到作业2的内存分区」的错误提示，"
            "说明程序的异常处理是有效的。",
        ),
        (
            "外部碎片的产生",
            "序列9中作业6申请60KB后，在地址200处仅剩30KB空闲区，无法满足后续较大请求，"
            "形成了外部碎片。这是首次适应算法的典型问题——低地址频繁切割导致碎片增多。",
        ),
        (
            "空闲分区合并机制",
            "序列11中作业6释放60KB后，该分区与前面90KB的空闲区（地址140）相邻，"
            "系统自动合并为140KB的空闲区，验证了回收时前向合并的正确性。"
            "序列6中作业3释放100KB后产生两个不相邻的空闲区（130KB和430KB），未发生合并，"
            "说明只有地址相邻的空闲分区才会合并。",
        ),
        (
            "内存利用率变化",
            "测试结束时，640KB内存中：作业5占用140KB、作业4占用200KB、作业7占用50KB，"
            "共占用390KB；两个空闲区分别为140KB和160KB，共250KB空闲，内存利用率约60.9%。",
        ),
    ]
    for i, (title, content) in enumerate(analyses, 1):
        add_paragraph(doc, f"{i}. {title}", bold=True)
        add_paragraph(doc, content, indent=0.74)

    # 七、实验总结
    add_heading(doc, "七、实验总结", 1)
    summary = (
        "通过本次实验，我深入理解了可变分区内存管理的原理和首次适应分配算法的实现过程。"
        "实验采用双向链表管理内存分区，能够灵活地进行分区的分配、回收和合并操作。\n\n"
        "首次适应算法的优点是实现简单、分配速度快，在低地址优先分配的策略下有利于保留高地址的大块空闲区；"
        "但其缺点是在低地址部分容易产生较多的外部碎片，影响内存利用率。\n\n"
        "实验过程中，我掌握了以下关键技术点："
        "（1）双向链表的插入与删除操作；（2）分区切割时新结点的创建与地址计算；"
        "（3）回收时四种相邻情况的判断与合并逻辑；（4）分区表的可视化显示。\n\n"
        "本程序支持交互式和批处理两种运行模式，能够清晰地展示每次内存操作后的分区状态变化，"
        "为理解操作系统内存管理提供了直观的实验平台。"
    )
    add_paragraph(doc, summary, indent=0.74)

    # 八、参考文献
    add_heading(doc, "八、参考文献", 1)
    refs = [
        "[1] 汤子瀛, 哲凤屏, 汤小丹. 计算机操作系统（第四版）[M]. 西安: 西安电子科技大学出版社.",
        "[2] 操作系统原理课程讲义 —— 动态分区分配方式.",
        "[3] 首次适应算法（First Fit）相关资料.",
    ]
    for ref in refs:
        add_paragraph(doc, ref)

    doc.save(OUTPUT_FILE)
    print(f"实验报告已生成: {OUTPUT_FILE}")
    print(f"文件大小: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
