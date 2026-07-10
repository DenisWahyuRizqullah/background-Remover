from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io
import os

app = FastAPI(title="AI Background Remover API")

@app.post("/remove-bg")
async def remove_background(image: UploadFile = File(...)):
    # 1. Validasi apakah file yang diunggah adalah gambar
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File yang diunggah harus berupa gambar!")

    try:
        # 2. Baca file gambar yang dikirim dari client ke dalam memori
        request_object_content = await image.read()
        input_image = Image.open(io.BytesIO(request_object_content))

        # 3. Proses penghapusan background menggunakan library rembg
        # Fungsi remove() ini otomatis memisahkan objek utama dari background-nya
        output_image = remove(input_image)

        # 4. Simpan gambar hasil (format PNG transparan) ke dalam bytes buffer di memori
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # 5. Langsung kirim balik file gambar fisik .png ke client
        return StreamingResponse(img_byte_arr, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses gambar: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Railway membutuhkan aplikasi berjalan di port yang disediakan oleh sistem enviroment
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)