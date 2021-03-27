import pyqrcode
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from enum import Enum
import png
from pathlib import Path
import os
import json
from typing import Tuple


MY_PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_PATH = os.path.join(MY_PATH, 'temp')
TEMPLATE_PATH = os.path.join(MY_PATH, 'templates')
TEMPLATE_DEFINITIONS = os.path.join(TEMPLATE_PATH, 'template_definition.txt')
TEMP_QR_CODE_PNG = os.path.join(TEMP_PATH, 'qr_code.png')
BACKGROUND_PNG = 'background.jpg'
TEST_WALLET_ADDR = '1Aa' * 11 + 'a'


class OffsetType(Enum):
    TOP_LEFT = 1
    CENTER = 2


class Template():
    def load_from_json(json):
        background_src = json['background_src'] if 'background_src' in json else ''
        ro_w = json['raw_offset_width'] if 'raw_offset_width' in json else 0
        ro_h = json['raw_offset_height'] if 'raw_offset_height' in json else 0
        offset_type = json['offset_type'] if 'offset_type' in json else OffsetType.Center
        return Template(background_src, (ro_w, ro_h), offset_type)

    def __init__(self, background_src: str,
                 raw_offset: Tuple[int, int], offset_type: OffsetType):
        self.background_src = background_src
        self.raw_offset = raw_offset
        self.offset_type = offset_type


def TemplateController():
    def __init__(self):
        pass

    def load_templates(self) -> None:
        templates = []
        if os.path.isfile(TEMPLATE_DEFINITIONS):
            with open(TEMPLATE_DEFINITIONS) as file:
                templates = json.load(file)


def add_img(background_src: str, foreground_src: str,
            raw_offset: Tuple[int, int], offset_type: OffsetType) -> None:
    # TODO: Propagate errors
    background = Image.open(background_src, 'r')
    bg_w, bg_h = background.size
    foreground = Image.open(foreground_src, 'r')
    fg_w, fg_h = foreground.size

    offset = None
    if offset_type == OffsetType.TOP_LEFT:
        offset = raw_offset
    elif offset_type == OffsetType.CENTER:
        ro_w, ro_h = raw_offset
        offset = (ro_w - fg_w // 2, ro_h - fg_h // 2)
    else:
        raise Exception("Unknown Offset Type")
    background.paste(foreground, offset)
    background.save('combined.png')

# Generates a QR code saved locally.  If it fails, returns an error code.


def gen_qr_code(qr_contents: str) -> str:
    if not qr_contents:
        return ''

    print(qr_contents)
    qr_code = pyqrcode.create(qr_contents)
    qr_code.png(TEMP_QR_CODE_PNG, scale=5)

# Returns true if the wallet address is valid.


def check_wallet_addr(wallet_addr: str) -> bool:
    # TODO replace this with something more reasonable.
    return bool(wallet_addr)

# App Specific

# Wishlist


def launch_bare_bones_gui(root: tk.Tk) -> None:
    def gen_qr_code_button() -> None:
        wallet_addr = wallet_addr_entry.get()
        if not check_wallet_addr(wallet_addr):
            messagebox.showerror(title="Bad Inputs",
                                 message='Enter Valid Wallet Address')

        err_msg = gen_qr_code(wallet_addr_entry.get())
        add_img(BACKGROUND_PNG, TEMP_QR_CODE_PNG,
                (380, 260), OffsetType.CENTER)

        if err_msg:
            messagebox.showerror(
                title='Failure', message='Failed with error ' + err_msg)
            return
        messagebox.showinfo(title='Success', message='Wrote QR Code!')
        root.quit()

    tk.Label(root, text='Wallet Address').grid(row=0)

    wallet_addr_entry = tk.Entry(root)
    wallet_addr_entry.grid(row=0, column=1)

    tk.Button(root, text='Quit', command=root.quit).grid(row=2, column=0)
    tk.Button(root, text='Generate QR Code',
              command=gen_qr_code_button).grid(row=2, column=0)


class QRCreationPage:
    def __init__(self, root, template=None):
        self.root = root
        self.frame = tk.Frame(self.root)
        launch_bare_bones_gui(root)


class TemplateSelectorPage:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)

    def choose_template(self):
        # TODO get template
        self.newWindow = tk.Toplevel(self.parent)


class AppController():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.template_selector_page = TemplateSelectorPage(tk.Frame(self.root))
        self.show_qr_creation_page()

    def show_template_selector_page(self) -> None:
        self.template_selector_page.tkraise()

    # TODO find type for template
    def show_qr_creation_page(self, template=None) -> None:
        cur_page = QRCreationPage(self.root)
        cur_page.frame.tkraise()


def run() -> None:
    Path(TEMP_PATH).mkdir(parents=True, exist_ok=True)
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()
    # launch_bare_bones_gui()


if __name__ == '__main__':
    run()
