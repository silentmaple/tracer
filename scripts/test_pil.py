from PIL import Image, ImageDraw
from PIL import ImageFont

# 参考代码：https://www.cnblogs.com/wupeiqi/articles/5812291.html
# 1. 创建图片
# img = Image.new(mode="RGB", size=(120, 30), color=(255, 255, 255))
# img.show()
# 保存到本地
# with open('code.png', 'wb') as f:
#     img.save(f, format='png')


# 2. 创建画笔，用于在图片上画任意内容
# img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
# 创建画笔
# draw = ImageDraw.Draw(img, mode='RGB')


# 3. 画点
# img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
# draw = ImageDraw.Draw(img, mode='RGB')
# # 第一个参数：表示坐标
# 第二个参数：表示颜色
# draw.point([100, 100], fill="red")
# draw.point([300, 300], fill=(255, 255, 255))


# 4.画线
# img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
# draw = ImageDraw.Draw(img, mode='RGB')
# 第一个参数：表示起始坐标和结束坐标
# 第二个参数：表示颜色
# draw.line((100,100,100,300), fill='red')
# draw.line((100,100,300,100), fill=(255, 255, 255))


# 5. 画圆
# img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
# draw = ImageDraw.Draw(img, mode='RGB')
# 第一个参数：表示起始坐标和结束坐标（圆要画在其中间）
# 第二个参数：表示开始角度
# 第三个参数：表示结束角度
# 第四个参数：表示颜色
# draw.arc((100, 100, 300, 300), 0, 90, fill="red")
# img.show()


# 写文本
img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
draw = ImageDraw.Draw(img, mode='RGB')
# 第一个参数：表示起始坐标
# 第二个参数：表示写入内容
# 第三个参数：表示颜色
draw.text([0, 0], 'python', "red")


# 7. 特殊字体文字
img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
draw = ImageDraw.Draw(img, mode='RGB')
# 第一个参数：表示字体文件路径
# 第二个参数：表示字体大小
font = ImageFont.truetype("kumo.ttf", 28)
# 第一个参数：表示起始坐标
# 第二个参数：表示写入内容
# 第三个参数：表示颜色
# 第四个参数：表示颜色
draw.text([0, 0], 'python', "red", font=font)

with open('code.png', 'wb') as f:
    img.save(f, format='png')
