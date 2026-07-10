import io
import os
import gc
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from PIL import Image

app = FastAPI(
    title="AI Background Remover API",
    description="A lightweight and production-ready API for background removal optimized for low-RAM environments.",
    version="1.0.0"
)

# Initialize a lightweight session globally to avoid reloading the model on every request.
# 'u2net_fast' is specifically designed for systems with constrained hardware/RAM.
try:
    lightweight_session = new_session("u2netp")  # Use 'u2netp' for a smaller model footprint
except Exception as e:
    print(f"Error initializing rembg session: {str(e)}")
    lightweight_session = None

@app.post(
    "/remove-bg",
    summary="Remove image background",
    description="Upload an image file to process and extract the foreground object with a transparent background."
)
async def remove_background(image: UploadFile = File(...)):
    # Validate file type extension/mime-type
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. The uploaded file must be an image."
        )

    try:
        # Read file contents into memory safely
        file_content = await image.read()
        input_image = Image.open(io.BytesIO(file_content))

        # ASSISTED DOWNSCALING: Check if image dimensions exceed memory limits.
        # Restricting the maximum edge length to 1500 pixels scales down large compressed 
        # images (e.g., 4MB+ JPGs) so they don't blow up the RAM matrix.
        max_dimension = 1500
        if max(input_image.size) > max_dimension:
            input_image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

        # Process the image using our pre-loaded lightweight session
        output_image = remove(input_image, session=lightweight_session)

        # Save the result into a byte stream as PNG to preserve transparency (alpha channel)
        image_byte_array = io.BytesIO()
        output_image.save(image_byte_array, format="PNG")
        image_byte_array.seek(0)

        # Explicit garbage collection to force-release system memory immediately
        del input_image
        del output_image
        gc.collect()

        return StreamingResponse(image_byte_array, media_type="image/png")

    except Exception as e:
        # Catch unexpected errors gracefully and prevent server crashes
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while processing the image: {str(e)}"
        )