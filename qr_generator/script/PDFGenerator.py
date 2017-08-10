import os
import shutil
from os import listdir
from qr_generator.script import markup
import pdfkit

def generate():
    if os.path.exists("temp_rooms"):
        path = "temp_rooms"
        imgs = listdir(path)

        os.chdir(path)
        page = markup.page()
        page.init(title="Rooms QR Codes")
        page.ul(class_='room_codes')
        page.ul.close()
        page.img(src=imgs, width=310, height=150, alt="Thumbnails")
        html = str(page)
        with open('room_codes.html', 'w') as file:
            file.write(html)
        os.chmod('room_codes.html', 0o777)
        # pdfkit.from_file('room_codes.html', 'room_codes.pdf')
        os.system('xvfb-run -a wkhtmltopdf room_codes.html room_codes.pdf')

        os.chdir("..")
        if os.path.exists("room_codes.pdf"):
            os.remove("room_codes.pdf")
        shutil.move("temp_rooms/room_codes.pdf", "room_codes.pdf")
        shutil.rmtree(path)

    if os.path.exists("temp_panels"):
        path = "temp_panels"
        imgs = listdir(path)

        os.chdir(path)
        page = markup.page()
        page.init(title="Panels QR Codes")
        page.ul(class_='panel_codes')
        page.ul.close()
        page.img(src=imgs, width=310, height=150, alt="Thumbnails")
        html = str(page)
        with open('panel_codes.html', 'w') as file:
            file.write(html)
        os.chmod('panel_codes.html', 0o777)
        # pdfkit.from_file('panel_codes.html', 'panel_codes.pdf')
        os.system('xvfb-run -a wkhtmltopdf panel_codes.html panel_codes.pdf')

        os.chdir("..")
        if os.path.exists("panel_codes.pdf"):
            os.remove("panel_codes.pdf")
        shutil.move("temp_panels/panel_codes.pdf", "panel_codes.pdf")
        shutil.rmtree(path)

    if os.path.exists("temp_closets"):
        path = "temp_closets"
        imgs = listdir(path)

        os.chdir(path)
        page = markup.page()
        page.init(title="Closets QR Codes")
        page.ul(class_='closet_codes')
        page.ul.close()
        page.img(src=imgs, width=310, height=150, alt="Thumbnails")
        html = str(page)
        with open('closet_codes.html', 'w') as file:
            file.write(html)
        os.chmod('closet_codes.html', 0o777)
        # pdfkit.from_file('closet_codes.html', 'closet_codes.pdf')
        os.system('xvfb-run -a wkhtmltopdf closet_codes.html closet_codes.pdf')

        os.chdir("..")
        if os.path.exists("closet_codes.pdf"):
            os.remove("closet_codes.pdf")
        shutil.move("temp_closets/closet_codes.pdf", "closet_codes.pdf")
        shutil.rmtree(path)

    os.chdir("..")