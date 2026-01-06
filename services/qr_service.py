import qrcode
import os

QR_FOLDER = "static/qr_codes"


def generate_qr_code(data: str, filename: str) -> str:
    os.makedirs(QR_FOLDER, exist_ok=True)

    qr = qrcode.make(data)
    file_path = os.path.join(QR_FOLDER, filename)
    qr.save(file_path)

    return file_path
