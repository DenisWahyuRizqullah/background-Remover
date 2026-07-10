# Background Remover API

This is a simple FastAPI-based API for automatically removing the background from images using the rembg library.

## Features

- Upload an image through the API
- Automatically remove the background
- Return the result as a transparent PNG image
- Support automatic API documentation from FastAPI

## Technologies Used

- Python
- FastAPI
- Uvicorn
- rembg
- Pillow

## Prerequisites

Make sure you have installed:

- Python 3.9+
- pip

## Running Locally

### 1. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You can also run the application with:

```bash
python main.py
```

Once the server is running, open:

- API docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoint

### POST /remove-bg

This endpoint accepts an image file and returns the result without a background.

#### Parameters

- `image`: an image file (JPG, PNG, etc.)

#### Example with curl

```bash
curl -X POST "http://127.0.0.1:8000/remove-bg" \
  -F "image=@/path/to/your/image.jpg" \
  -o output.png
```

#### Example with Python

```python
import requests

url = "http://127.0.0.1:8000/remove-bg"
files = {"image": open("image.jpg", "rb")}
response = requests.post(url, files=files)

if response.status_code == 200:
    with open("output.png", "wb") as f:
        f.write(response.content)
    print("Image saved successfully as output.png")
else:
    print(response.text)
```

## Notes

- On the first run, the rembg library may download the required AI model. This can take a few minutes depending on your internet connection.
- The output returned is a PNG image with a transparent background.

## Project Structure

```text
Background-Remover/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## License

You can use and develop this project freely according to your needs.
