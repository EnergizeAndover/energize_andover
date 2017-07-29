import os
from os import listdir
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from qr_generator.script import PDFGenerator

def generate():

    font = ImageFont.truetype("arial.ttf", 32)

    if os.path.exists("temp_rooms"):
        path = "temp_rooms"
        imgs = listdir(path)
        os.chdir(path)
        for x in imgs:
            img = Image.open(x)
            width, height = img.size
            newImage = Image.new("RGB", (width + 365, height), (255, 255, 255))
            newImage.paste(img)
            draw = ImageDraw.Draw(newImage)
            draw.text((width, height / 2 - 30), "Old: " + "\n" + "New: ", 000000, font=font)
            newImage.save(x[:-4] + ".png")

        os.chdir("..")

    if os.path.exists("temp_panels"):
        path = "temp_panels"
        imgs = listdir(path)
        os.chdir(path)
        for x in imgs:
            img = Image.open(x)
            width, height = img.size
            newImage = Image.new("RGB", (width + 365, height), (255, 255, 255))
            newImage.paste(img)
            draw = ImageDraw.Draw(newImage)
            draw.text((width, height / 2 - 30), "Old: " + "\n" + "New: ", 000000, font=font)
            newImage.save(x[:-4] + ".png")

        os.chdir("..")

    if os.path.exists("temp_closets"):
        path = "temp_closets"
        imgs = listdir(path)
        os.chdir(path)
        for x in imgs:
            img = Image.open(x)
            width, height = img.size
            print(str(width) + " " + str(height))
            newImage = Image.new("RGB", (width + 365, height), (255, 255, 255))
            newImage.paste(img)
            draw = ImageDraw.Draw(newImage)
            draw.text((width, height / 2 - 30), "Old: " + "\n" + "New: ", 000000, font=font)
            newImage.save(x[:-4] + ".png")

        os.chdir("..")

    PDFGenerator.generate()