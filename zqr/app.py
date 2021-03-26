import pyqrcode
import tkinter as tk
from tkinter import messagebox

def get_qr_image(qr_contents: str):
    #TODO Look into standardizing QR Code size with verson
    pyqrcode.create(qr_contents)

def gen_qr_code(qr_contents: str) -> None:
    print(qr_contents)
# 

def launch_bare_bones_gui() -> None:
    def gen_qr_code_button() -> None:
        err_msg = gen_qr_code(wallet_addr_entry.get())
        if err_msg:
            messagebox.showerror(title='Failure', message='Failed with error ' + err_msg)
            return
        messagebox.showinfo(title='Success', message='Wrote QR Code!')
        gui.quit()

    gui = tk.Tk()
    tk.Label(gui, text = 'wallet Address').grid(row=0)

    wallet_addr_entry = tk.Entry(gui)
    wallet_addr_entry.grid(row=0, column=1)

    tk.Button(gui, text='Quit', command=gui.quit).grid(row=2, column=0)
    tk.Button(gui, text='Generate QR Code', command=gen_qr_code_button).grid(row=2, column=0)

    tk.mainloop()
    

def run() -> None:
    print('test')
    launch_bare_bones_gui()


if __name__ == '__main__':
        run()
