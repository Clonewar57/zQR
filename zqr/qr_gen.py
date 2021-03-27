import pyqrcode


def get_qr_image(qr_contents: str):

    qr = pyqrcode.QRCode(
        version=1,
        error_correction=pyqrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('Some data')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    print(type(img))


def write_qr_to_disk(qr_contents: str) -> None:
    img = get_qr_image(qr_contents)
