"""
封面日期生成器
在AI每日新闻封面图片上添加当天日期
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

def add_date_to_cover(
    input_path: str,
    output_path: str,
    date: datetime = None,
    font_path: str = None
) -> str:
    """
    在封面图片上添加日期
    
    Args:
        input_path: 原始封面图片路径
        output_path: 输出图片路径
        date: 要显示的日期，默认为今天
        font_path: 字体文件路径，默认使用系统字体
    
    Returns:
        输出文件路径
    """
    if date is None:
        date = datetime.now()
    
    # 打开图片
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    
    # 日期格式：2026 . 01 . 17（点前后加空格，提高可读性）
    date_text = date.strftime("%Y . %m . %d")
    
    # 根据图片宽度动态计算字体大小
    img_width, img_height = img.size
    font_size = max(24, int(img_width * 0.045))  # 约为图片宽度的4.5%
    font = None
    
    # 尝试多种字体路径
    font_candidates = [
        font_path,
        # macOS 系统字体 - 手写/艺术风格
        "/System/Library/Fonts/Noteworthy.ttc",
        "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf",
        "/System/Library/Fonts/Supplemental/Chalkduster.ttf",
        "/System/Library/Fonts/Supplemental/Comic Sans MS.ttf",
        "/System/Library/Fonts/Supplemental/Marker Felt.ttc",
        # Ubuntu/Linux 系统字体（GitHub Actions 环境）
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        # 备用系统字体
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SF-Pro.ttf",
    ]
    
    for fp in font_candidates:
        if fp and os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, font_size)
                print(f"使用字体: {fp}")
                break
            except Exception as e:
                continue
    
    if font is None:
        # 使用默认字体
        font = ImageFont.load_default()
        print("使用默认字体")
    
    # 计算日期文字的位置（img_width, img_height 已在上方获取）
    # icon区域大约在图片右侧，日期放在icon下方中央
    
    # 获取文字边界框
    bbox = draw.textbbox((0, 0), date_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 位置：icon区域（右半部分）的底部
    # icon区域大约从图片50%位置开始到95%位置
    icon_area_center_x = img_width * 0.72
    date_x = icon_area_center_x - text_width / 2
    date_y = img_height * 0.82  # 底部留一些边距
    
    # 使用温暖的棕橙色，与封面的秋叶主题搭配
    # 类似标题 "Kaede's AI daily news" 的颜色
    text_color = "#D2691E"  # 巧克力橙色 / Chocolate
    
    # 添加轻微的阴影效果增加立体感
    shadow_color = "#8B4513"  # 深棕色
    shadow_offset = max(2, int(font_size * 0.05))  # 根据字体大小调整阴影
    
    # 绘制阴影
    draw.text(
        (date_x + shadow_offset, date_y + shadow_offset),
        date_text,
        font=font,
        fill=shadow_color
    )
    
    # 绘制主文字
    draw.text(
        (date_x, date_y),
        date_text,
        font=font,
        fill=text_color
    )
    
    # 保存图片（根据扩展名选择格式）
    if output_path.lower().endswith('.png'):
        img.save(output_path, format='PNG')
    else:
        img.save(output_path, quality=95)
    print(f"封面已生成: {output_path}（尺寸: {img_width}x{img_height}, 字体大小: {font_size}）")
    
    return output_path


def main():
    """主函数 - 用于测试"""
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 输入输出路径
    input_path = os.path.join(project_root, "assets", "Untitled design.png")
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now()
    output_filename = f"cover_{today.strftime('%Y%m%d')}.jpg"
    output_path = os.path.join(output_dir, output_filename)
    
    # 生成封面
    add_date_to_cover(input_path, output_path, today)


if __name__ == "__main__":
    main()
