from PIL import Image, ImageFont, ImageDraw, ImageTk

class ImageHandler():
    def __init__(self):
        """class that adds a watermark to images"""
        self.watermark_img = None
        self.main_img = None
        self.watermark_text = ""

    def watermark_image(self, path):
        self.watermark_img = Image.open(path)

    def main_image(self, path):
        self.main_img = Image.open(path)

    def add_text_watermark(self, text, size):
        draw = ImageDraw.Draw(self.main_img)
        font = ImageFont.truetype("arial.ttf", round(25*size))
        draw.text((0, 0), text, (255, 255, 255), font=font)

    def add_image_watermark(self, size):
        self.watermark_img.thumbnail((100, 100), Image.ANTIALIAS)
        resized_image = self.watermark_img.resize((round(50*size),round(50*size)), Image.ANTIALIAS)
        self.main_img.paste(resized_image)
  
    def resize_image(self):
        resized_image = self.main_img.resize((300,300), Image.ANTIALIAS)
        new_image = ImageTk.PhotoImage(resized_image)
        return new_image

    def save_image(self, filename):
        self.main_img.save(filename)