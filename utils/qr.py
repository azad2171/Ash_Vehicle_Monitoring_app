import qrcode
import os

QR_DIR = "static/qr_codes"


def generate_qr_code(qr_data: str, filename: str) -> str:
    """
    Generates a QR code image.

    :param qr_data: Data to encode in QR
    :param filename: Filename WITHOUT extension
    :return: Relative path to saved QR image
    """
    os.makedirs(QR_DIR, exist_ok=True)

    file_path = os.path.join(QR_DIR, f"{filename}.png")

    qr = qrcode.make(qr_data)
    qr.save(file_path)

    return file_path
