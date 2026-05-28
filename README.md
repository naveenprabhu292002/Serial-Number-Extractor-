# Serial Number Extractor

A Python application that extracts serial numbers from device label images using AI vision models (Google Gemini or OpenRouter).

## Features

- Extracts serial numbers starting with "BW" from device label images
- Supports two AI providers: Google Gemini and OpenRouter
- FastAPI-based REST API for integration
- Command-line script for quick extraction

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file and add your API keys:

```bash
copy .env.example .env
```

Edit `.env` and add your API keys:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
OPENROUTER_API_KEY=your_actual_openrouter_api_key_here
```

**Important:** Never commit the `.env` file to version control. It's already included in `.gitignore`.

### 3. Get API Keys

- **Google Gemini**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenRouter**: Get your API key from [OpenRouter](https://openrouter.ai/keys)

## Usage

### Command Line Script

Edit `run_extract.py` to set your image path and preferred provider, then run:

```bash
python run_extract.py
```

### API Server

Start the FastAPI server:

```bash
python -m uvicorn serial_extractor_api:app --reload
```

Or use the batch file (Windows):

```bash
start_server.bat
```

The API will be available at `http://localhost:8000`

#### API Endpoints

- `POST /extract-serial` - Upload an image to extract serial number
- `GET /health` - Health check endpoint

Example using curl:

```bash
curl -X POST "http://localhost:8000/extract-serial" -F "file=@path/to/image.jpg"
```

## Docker

Build and run using Docker:

```bash
docker build -t serial-extractor .
docker run -p 8000:8000 --env-file .env serial-extractor
```

## Security

- API keys are stored in environment variables, not in code
- The `.env` file is excluded from version control
- Use `.env.example` as a template for required environment variables
