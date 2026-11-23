from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import qrcode
from io import BytesIO

app = FastAPI(title="QR Code Generator API")

@app.get("/generate-qr")
def generate_qr(
    data: str = Query(..., description="The text or URL to convert into a QR Code"),
    size: int = Query(10, description="The size of the QR code pixels (default: 10)"),
    color: str = Query("black", description="The color of the QR Code (e.g., 'black', 'blue', 'red')")
):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Usa il colore scelto dall'utente
    img = qr.make_image(fill_color=color, back_color="white")

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")
