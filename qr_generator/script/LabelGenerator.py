import os
from os import listdir
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from qr_generator.script import PDFGenerator
from django.shortcuts import get_object_or_404
from energize_andover.models import Room, Panel, Closet, School

def generate(school_id):

    font = ImageFont.truetype("arial.ttf", 32)
    school_obj = get_object_or_404(School, pk=school_id)

    if os.path.exists("temp_rooms"):
        path = "temp_rooms"

        os.chmod(path, 0o777)
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                temp_path = os.path.join(dirpath, filename)
                os.chmod(temp_path, 0o777)

        imgs = listdir(path)
        os.chdir(path)
        for x in imgs:
            img = Image.open(x)
            qid = int(x[4:-4])
            room_obj = school_obj.rooms().get(QID=qid)
            width, height = img.size
            newImage = Image.new("RGB", (width + 365, height), (255, 255, 255))
            newImage.paste(img)
            draw = ImageDraw.Draw(newImage)
            draw.text((width, height / 2 - 30), "Old: " + room_obj.OldName + "\n" + "New: " + room_obj.Name, 000000, font=font)
            newImage.save(x[:-4] + ".png")
            os.chmod(x[:-4] + ".png", 0o777)

        os.chdir("..")

    if os.path.exists("temp_panels"):
        path = "temp_panels"

        os.chmod(path, 0o777)
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                temp_path = os.path.join(dirpath, filename)
                os.chmod(temp_path, 0o777)

        imgs = listdir(path)
        os.chdir(path)
        for x in imgs:
            img = Image.open(x)
            qid = int(x[5:-4])
            panel_obj = school_obj.panels().get(QID=qid)
            width, height = img.size
            newImage = Image.new("RGB", (width + 365, height), (255, 255, 255))
            newImage.paste(img)
            draw = ImageDraw.Draw(newImage)
            draw.text((width, height / 2 - 20), "Name: " + panel_obj.Name, 000000, font=font)
            newImage.save(x[:-4] + ".png")
            os.chmod(x[:-4] + ".png", 0o777)

        os.chdir("..")

    if os.path.exists("temp_closets"):
        path = "temp_closets"

        os.chmod(path, 0o777)
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                temp_path = os.path.join(dirpath, filename)
                os.chmod(temp_path, 0o777)

        imgs = listdir(path)
        os.chdir(path)
        for x in imgs:
            img = Image.open(x)
            qid = int(x[6:-4])
            closet_obj = school_obj.closets().get(QID=qid)
            width, height = img.size
            newImage = Image.new("RGB", (width + 365, height), (255, 255, 255))
            newImage.paste(img)
            draw = ImageDraw.Draw(newImage)
            draw.text((width, height / 2 - 30), "Old: " + closet_obj.Old_Name + "\n" + "New: " + closet_obj.Name, 000000, font=font)
            newImage.save(x[:-4] + ".png")
            os.chmod(x[:-4] + ".png", 0o777)

        os.chdir("..")

    PDFGenerator.generate()