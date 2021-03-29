import pyqrcode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from enum import Enum
import png
from pathlib import Path
import os
import json
from typing import Tuple
import random


MY_PATH = os.getcwd()
TEMP_PATH = os.path.join(MY_PATH, 'temp')
TEMPLATE_PATH = os.path.join(MY_PATH, 'templates')
TEMPLATE_DEFINITIONS = os.path.join(TEMPLATE_PATH, 'template_definitions.txt')
TEMP_QR_CODE_PNG = os.path.join(TEMP_PATH, 'qr_code.png')
OUTPUT_PNG = 'output.png'
BACKGROUND_PNG = 'background.jpg'
TEST_WALLET_ADDR = '1Aa' * 11 + 'a'


class OffsetType(Enum):
    TOP_LEFT = 1
    CENTER = 2

# In charge of a single template
class Template():
    def load_from_dict(json):
        background_src = json['background_src'] if 'background_src' in json else ''
        ro_w = json['raw_offset_width'] if 'raw_offset_width' in json else 0
        ro_h = json['raw_offset_height'] if 'raw_offset_height' in json else 0
        offset_type = OffsetType(
            json['offset_type']) if 'offset_type' in json else OffsetType.CENTER
        return Template(background_src, (ro_w, ro_h), offset_type)

    def __init__(self, background_src: str,
                 raw_offset: Tuple[int, int], offset_type: OffsetType):
        self.background_src = background_src
        self.raw_offset = raw_offset
        self.offset_type = offset_type

    def to_dict(self) -> dict:
        ro_w, ro_h = self.raw_offset
        return {
            'background_src': self.background_src,
            'raw_offset_width': ro_w,
            'raw_offset_height': ro_h,
            'offset_type': OffsetType(self.offset_type)
        }

# In charge of loading/storing/holding templates
class TemplateController():
    def __init__(self, load_templates=True):
        self.templates = []
        if load_templates:
            self.load_templates()
            if len(self.templates) == 0:
                self.create_blank_template()

    def load_templates(self) -> None:
        loaded_dicts = []
        if os.path.isfile(TEMPLATE_DEFINITIONS):
            with open(TEMPLATE_DEFINITIONS) as file:
                loaded_dicts = json.load(file)
        else:
            print('NOT A FILE')
        self.templates = [Template.load_from_dict(x) for x in loaded_dicts]

    def add_template(self, template, write_to_disk=True) -> None:
        templates.append(template)
        if write_to_disk:
            self.write_templates()

    def write_templates(self) -> None:
        to_write_dicts = []
        for template in self.templates:
            to_write_dicts.append(template.to_dict())
        with open(TEMPLATE_DEFINITIONS) as file:
            file.write(json.dumps(to_write_dicts, indent=4))

    def get_random_template(self):
        return self.templates[random.randint(0, len(self.templates) - 1)]

    def create_blank_template(self):
        # TODO
        pass

# Holds generic image manipulation functions
class ImageUtils():
    def add_img_from_src(background_src: str,
                         foreground_src: str,
                         raw_offset: Tuple[int,
                                           int],
                         offset_type: OffsetType) -> None:
        # TODO: Propagate errors
        background = Image.open(background_src, 'r')
        foreground = Image.open(foreground_src, 'r')
        background = ImageUtils.add_img(
            background, foreground, raw_offset, offset_type)
        background.save(OUTPUT_PNG)

    def add_img(background: Image, foreground: Image,
                raw_offset: Tuple[int, int], offset_type: OffsetType) -> Image:
        # TODO: Propagate errors
        bg_w, bg_h = background.size
        fg_w, fg_h = foreground.size

        offset = None
        if offset_type == OffsetType.TOP_LEFT:
            offset = raw_offset
        elif offset_type == OffsetType.CENTER:
            ro_w, ro_h = raw_offset
            offset = (ro_w - fg_w // 2, ro_h - fg_h // 2)
        else:
            raise Exception('Unknown Offset Type')
        background.paste(foreground, offset)

        return background

    # Generates a QR code saved locally.  If it fails, returns an error code.
    def gen_qr_code(qr_contents: str) -> str:
        if not qr_contents:
            return ''

        qr_code = pyqrcode.create(qr_contents)
        qr_code.png(TEMP_QR_CODE_PNG, scale=5)

    def resize_and_fill_area(image: Image, size: Tuple[int, int]) -> Image:
        background = Image.new('RGB', size, color='black')
        image.thumbnail(size, Image.ANTIALIAS)

        size_w, size_h = size
        image_w, image_h = image.size

        offset = (0, 0)
        if size_w > image_w:
            offset = ((size_w - image_w) // 2, 0)
        else:
            offset = (0, (size_h - image_h) // 2)

        image = ImageUtils.add_img(
            background, image, offset, OffsetType.TOP_LEFT)
        return image

    def resize_to_tumbnail(image_src: str, size: Tuple[int, int]) -> Image:
        pass


# App Specific


class PostQRCreationPage:
    def __init__(self, app_controller, root, template=None):
        self.app_controller = app_controller
        self.root = root
        self.template = template
        self.setup_page()

    def setup_page(self):
        img = Image.open(OUTPUT_PNG)
        img = ImageUtils.resize_and_fill_area(img, (600, 450))
        img = ImageTk.PhotoImage(img)

        img_label = tk.Label(self.root, image=img)
        img_label.image = img
        img_label.grid(row=0, columnspan=8)

        tk.Label(
            self.root,
            text='Image written to: ' +
            OUTPUT_PNG).grid(
            row=1,
            column=0,
            columnspan=6)

        tk.Button(
            self.root,
            text='Back',
            command=lambda: self.app_controller.show_qr_creation_page(
                self.template)).grid(
            row=1,
            column=6)
        tk.Button(
            self.root,
            text='Quit',
            command=self.root.quit).grid(
            row=1,
            column=7)


class QRCreationPage:
    def __init__(self, app_controller, root, template=None):
        self.app_controller = app_controller
        self.root = root
        self.template = template
        self.setup_page()

    def setup_page(self):
        img = Image.open(
            os.path.join(
                TEMPLATE_PATH,
                self.template.background_src))
        img = ImageUtils.resize_and_fill_area(img, (600, 450))
        img = ImageTk.PhotoImage(img)

        img_label = tk.Label(self.root, image=img)
        img_label.image = img
        img_label.grid(row=0, columnspan=5)
        
        # Returns true if the wallet address is valid.
        def check_wallet_addr(wallet_addr: str) -> bool:
            # TODO replace this with something more reasonable.
            return bool(wallet_addr)

        def gen_qr_code_button() -> None:
            wallet_addr = wallet_addr_entry.get()
            if not check_wallet_addr(wallet_addr):
                messagebox.showerror(title='Bad Inputs',
                                     message='Enter Valid Wallet Address')

            err_msg = ImageUtils.gen_qr_code(wallet_addr_entry.get())
            ImageUtils.add_img_from_src(os.path.join(
                TEMPLATE_PATH, self.template.background_src), os.path.join(
                    TEMP_PATH, TEMP_QR_CODE_PNG),
                self.template.raw_offset, self.template.offset_type)

            if err_msg:
                messagebox.showerror(
                    title='Failure', message='Failed with error ' + err_msg)
                return
            self.app_controller.show_post_qr_creation_page(self.template)

        tk.Label(self.root, text='Wallet Address').grid(row=1, column=0)

        wallet_addr_entry = tk.Entry(self.root)
        wallet_addr_entry.grid(row=1, column=1, columnspan=2)

        tk.Button(self.root, text='Generate QR Code',
                  command=gen_qr_code_button).grid(row=1, column=3)
        tk.Button(
            self.root,
            text='Quit',
            command=self.root.quit).grid(
            row=1,
            column=4)

# Key strategy MVC (definition https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
# Move image on mouse click: https://stackoverflow.com/questions/23275445/move-an-image-in-python-using-tkinter
# Files can be selected by the user with from tkinter.filedialog import askopenfilename
#  https://stackoverflow.com/questions/9239514/filedialog-tkinter-and-opening-files
#
# *** ADD TEMPLATE ***
#   self.template_controller.add_template(template=template, write_to_disk=True)
class CreateTemplatePage:
    def __init__(self, app_controller, root, template_controller):
        self.app_controller = app_controller
        self.root = root
        self.template_controller = template_controller
        self.setup_page()

    def setup_page(self):
        # TODO: replace this demo page.
        def button_press():
            self.app_controller.show_template_selector_page()

        tk.Button(
            self.root,
            text="Back",
            command=button_press).grid(
            row=0,
            column=0)

# Helper functions
# *** CREATE A CLICKABLE IMAGE ***
#   (taken from https://stackoverflow.com/questions/40658728/clickable-images-for-python)
#   image = Image.open(image_src)
#   photo = ImageTk.PhotoImage(image)

#   # Create a url element from the image (Important, passing in root adds it to the current frame)
#   l = tk.Label(self.root, image=photo)
#   # add the image to the grid at position (0,0)
#   l.grid(row=0, column=0)
#   #bind click event to image
#   def on_click():
#       pass
#   l.bind('<Button-1>', on_click)
#
# *** GET TEMPLATES ***
#   self.template_controller.templates
#
# *** GET RANDOM TEMPLATE ***
#   self.template_controller.get_random_template()
#
# *** GET IMAGE LOCATION FROM TEMPLATE ***
#   template.background_src
#
# *** TURN AN IMAGE INTO A TUMBNAIL ***
#   img = Image.open('test.png')
#   img = ImageUtils.resize_and_fill_area(img, (600, 450))
#
# *** SHOW THE QR CREATION PAGE ***
#   self.app_controller.show_qr_creation_page(template)
class TemplateSelectorPage:
    def __init__(self, app_controller, root, template_controller):
        self.app_controller = app_controller
        self.root = root
        self.template_controller = template_controller
        self.setup_page()

    def setup_page(self):
        # TODO: replace this demo page.
        def random_template_button_press():
            self.app_controller.show_qr_creation_page()

        def new_template_button_press():
            self.app_controller.show_create_template_page()

        tk.Button(
            self.root,
            text="Random Template",
            command=random_template_button_press).grid(
            row=0,
            column=0)
        tk.Button(
            self.root,
            text="New Template",
            command=new_template_button_press).grid(
            row=0,
            column=1)


class AppController():
    def __init__(self, root: tk.Tk) -> None:
        self.cur_frame = None
        self.root = root
        self.template_controller = TemplateController()
        self.show_template_selector_page()

    def switch_frame(self) -> tk.Frame:
        if self.cur_frame is not None:
            self.cur_frame.grid_forget()
        self.cur_frame = tk.Frame(self.root)
        self.cur_frame.grid()
        return self.cur_frame

    def show_create_template_page(self) -> None:
        frame = self.switch_frame()
        CreateTemplatePage(self, frame, self.template_controller)

    def show_template_selector_page(self) -> None:
        frame = self.switch_frame()
        TemplateSelectorPage(self, frame, self.template_controller)

    def show_qr_creation_page(self, template=None) -> None:
        frame = self.switch_frame()
        if template is None:
            template = self.template_controller.get_random_template()
        cur_page = QRCreationPage(self, frame, template)

    def show_post_qr_creation_page(self, template=None) -> None:
        frame = self.switch_frame()
        cur_page = PostQRCreationPage(self, frame, template)


def run() -> None:
    Path(TEMP_PATH).mkdir(parents=True, exist_ok=True)
    root = tk.Tk()
    root.geometry('600x480')
    app = AppController(root)
    root.mainloop()


if __name__ == '__main__':
    run()
