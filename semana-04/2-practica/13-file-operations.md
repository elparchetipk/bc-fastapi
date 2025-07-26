# Practice 13: File Operations

## Objective

Learn to handle file uploads and downloads in FastAPI.

## Time: 60 minutes

## Implementation

### Step 1: File Upload Endpoint (30 min)

```python
from fastapi import FastAPI, File, UploadFile
import shutil

app = FastAPI()

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploaded_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded successfully"
    }
```

### Step 2: List Files Endpoint (30 min)

```python
import os

@app.get("/files/")
async def list_files():
    files = []
    for filename in os.listdir("."):
        if filename.startswith("uploaded_"):
            files.append({
                "name": filename,
                "size": os.path.getsize(filename)
            })
    return {"files": files}
```

## Testing

- Upload a small text file
- Check the file list
- Verify file was saved

## Deliverable

Working file upload and listing functionality.
