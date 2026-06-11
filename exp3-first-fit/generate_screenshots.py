#!/usr/bin/env python3
"""将终端输出渲染为截图图片"""
from PIL import Image, ImageDraw, ImageFont
import os

SCREENSHOT_DIR = "screenshots"
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)
TITLE_COLOR = (100, 200, 255)
SUCCESS_COLOR = (100, 255, 100)
ERROR_COLOR = (255, 100, 100)
FONT_SIZE = 14
LINE_HEIGHT = 18
PADDING = 20
MAX_WIDTH = 900


def get_font(size=FONT_SIZE):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render_terminal(text, output_path, title=None):
    font = get_font()
    lines = text.strip().split("\n")

    # 计算图片尺寸
    max_line_len = max(len(line) for line in lines) if lines else 40
    img_width = min(MAX_WIDTH, max_line_len * 8 + PADDING * 2)
    img_height = len(lines) * LINE_HEIGHT + PADDING * 2
    if title:
        img_height += LINE_HEIGHT + 10

    img = Image.new("RGB", (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    y = PADDING
    if title:
        draw.text((PADDING, y), title, fill=TITLE_COLOR, font=font)
        y += LINE_HEIGHT + 10

    for line in lines:
        color = TEXT_COLOR
        if "[分配成功]" in line or "[回收成功]" in line:
            color = SUCCESS_COLOR
        elif "[分配失败]" in line or "[回收失败]" in line or "[错误]" in line:
            color = ERROR_COLOR
        elif line.startswith(">>>") or "====" in line or "----" in line:
            color = TITLE_COLOR
        draw.text((PADDING, y), line, fill=color, font=font)
        y += LINE_HEIGHT

    img.save(output_path)
    print(f"Generated: {output_path}")


def main():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # 截图1: 批处理测试前3步
    with open("output_batch.txt") as f:
        content = f.read()
    sections = content.split(">>> 序列")
    if len(sections) >= 4:
        part1 = ">>> 序列" + sections[1] + "\n>>> 序列" + sections[2] + "\n>>> 序列" + sections[3]
        render_terminal(part1, f"{SCREENSHOT_DIR}/screenshot_batch_1-3.png",
                        "图1 批处理测试 - 序列1~3")

    # 截图2: 批处理测试序列6-8（含回收合并）
    if len(sections) >= 9:
        part2 = ">>> 序列" + sections[6] + "\n>>> 序列" + sections[7] + "\n>>> 序列" + sections[8]
        render_terminal(part2, f"{SCREENSHOT_DIR}/screenshot_batch_6-8.png",
                        "图2 批处理测试 - 回收与合并")

    # 截图3: 批处理测试最后几步
    if len(sections) >= 12:
        part3 = ">>> 序列" + sections[9] + "\n>>> 序列" + sections[10] + "\n>>> 序列" + sections[11]
        render_terminal(part3, f"{SCREENSHOT_DIR}/screenshot_batch_9-11.png",
                        "图3 批处理测试 - 序列9~11")

    # 截图4: 完整批处理概览（压缩版）
    summary_lines = []
    for i, sec in enumerate(sections[1:], 1):
        first_line = sec.split("\n")[0].strip()
        for line in sec.split("\n")[1:4]:
            if "[分配" in line or "[回收" in line:
                summary_lines.append(f"序列{i}: {first_line}")
                summary_lines.append(f"  {line.strip()}")
                break
    render_terminal("\n".join(summary_lines), f"{SCREENSHOT_DIR}/screenshot_summary.png",
                    "图4 批处理测试执行摘要")

    # 截图5: 交互式菜单
    menu_text = """
+--------------------------------------------------+
|  可变分区内存分配 —— 首次适应算法模拟            |
+--------------------------------------------------+
|  1. 分配内存 (首次适应)                          |
|  2. 回收内存                                     |
|  3. 显示内存分区表                               |
|  4. 显示空闲分区链                               |
|  5. 运行批处理测试 (640KB标准序列)               |
|  0. 退出                                         |
+--------------------------------------------------+

  请输入初始内存大小(KB) [默认640]: 640
  内存初始化完成，总大小: 640KB

  请选择操作: 1
  请输入作业号: 1
  请输入申请内存大小(KB): 130
  [分配成功] 作业1 获得 130KB 内存

  ========== 当前内存分区表 ==========
  分区号  起始地址(KB)  大小(KB)  状态      作业号
  ----------------------------------------------
     0           0       130 已分配         1
     1         130       510    空闲         -
  ==============================================
"""
    render_terminal(menu_text, f"{SCREENSHOT_DIR}/screenshot_interactive.png",
                    "图5 交互式操作演示")


if __name__ == "__main__":
    main()
