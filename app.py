from PIL import Image, ImageDraw
from pystray import Icon as icon, Menu as menu, MenuItem as item

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


def icon_clicked(icon, **kwargs):
    icon


icon('test', create_image(), menu=menu(
    item(
        "Run",
        default=True,
        action=icon_clicked
    ),
    item(
        'Quit',
        action=lambda icon, item: icon.stop(),
    ),
)).run()
