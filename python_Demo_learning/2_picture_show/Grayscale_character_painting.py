from PIL import Image

# ===== 字符集：画家的调色盘 =====
# 从暗到亮排列（视觉密度递减）
# @ 最密（笔画最多，代表最暗的像素）→ 空格最疏（代表最亮的像素）
# 你可以自定义这个序列——不同的字符集产生不同的艺术风格
CHARS = "@%#*+=-:. "

def image_to_ascii(image_path, width=120):
    """
    图片 → 灰度字符画（灰度版是彩色版本的"草稿"）
    
    算法流程：
    1. 打开图片，计算缩放后的尺寸
    2. 等比例缩放（保持构图比例）
    3. 转灰度（去掉颜色，只留明暗信息）
    4. 逐像素映射：亮度值(0~255) → 字符索引(0~len(CHARS)-1)
    5. 返回完整的字符串（可直接print）
    
    参数：
    - image_path: 图片路径（支持 jpg/png/bmp 等常见格式）
    - width: 输出的字符宽度（越大越精细，但终端可能显示不全）
    """
    img = Image.open(image_path)

    # 计算缩放后的高度
    # 终端字符的高宽比约2:1（一个字符的高度约等于两个字符的宽度）
    # 所以高度 = 宽度的像素比 × 0.5（补偿终端字符的扁长形状）
    # 示例：1920×1080照片，width=120
    #   aspect_ratio = 1080/1920 = 0.5625
    #   height = int(120 × 0.5625 × 0.5) = int(33.75) = 33
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)

    # 高质量缩放（将百万像素压缩为几千个字符的网格）
    # Image.LANCZOS：Lanczos滤波器，质量最高，适合缩小图片
    # （Pillow ≥10.0 中用 LANCZOS 替代了旧名称 ANTIALIAS）
    img = img.resize((width, height), Image.LANCZOS)

    # 转灰度模式 "L"
    # 转换公式：L = 0.299×R + 0.587×G + 0.114×B（人眼对不同颜色敏感度不同）
    # 之后 getpixel((x,y)) 返回单个整数 0(纯黑)~255(纯白)
    img = img.convert("L")

    # 逐像素映射：亮度 → 字符
    result = ""
    for y in range(height):
        for x in range(width):
            gray = img.getpixel((x, y))   # 0(黑) ~ 255(白)
            # 线性映射：gray=0→chars_idx=0('@'), gray=255→chars_idx=9(' ')
            # gray * (len(CHARS) - 1) // 255 是整数运算版本的归一化
            char_idx = gray * (len(CHARS) - 1) // 255
            result += CHARS[char_idx]
        result += "\n"   # 每行结束加换行

    return result

# ===== 使用示例 =====
ascii_art = image_to_ascii("your_photo.jpg", width=150)
print(ascii_art)

# 保存为txt文件——方便截图分享到评论区
with open("ascii_output.txt", "w", encoding="utf-8") as f:
    f.write(ascii_art)