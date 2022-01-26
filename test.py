import pystray
from PIL import Image, ImageDraw
import time

def callback(icon):
    image = Image.new('RGBA', (128,128), (255,255,255,255)) # create new image
    percent = 100
    while True:
        img = image.copy()
        d = ImageDraw.Draw(img)
        d.rectangle([0, 128, 128, 128-(percent * 128) / 100], fill='blue')
        icon.icon = img
        time.sleep(1)
        percent -= 5
        if percent < 0:
            percent = 100

width = 50
height = 50


def create_image():
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), "blue")
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill="red")
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill="green")
    return image
# image = Image.open("bat1.png") #Battery Status Full
icon = pystray.Icon("Test Icon 1",create_image())

icon.visible = True
icon.run(setup=callback)