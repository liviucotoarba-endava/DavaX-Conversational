# DavaX-Conversational - Chatbot API

A simple FastAPI-based chatbot API that provides AI-powered conversations with support for text, image, and audio messages.

## Features

- **RESTful API** built with FastAPI
- **OpenAI Integration** using GPT-4.1-mini model
- **Multimodal Support** for text, image, and audio
- **Conversation History** with local and cloud based persistence
- **Health Check** endpoint for monitoring

## Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key exported as an environment variable: `ENDAVA_OPENAI_API_KEY`

### Installation

1. Create virtual environment (recommended):

```bash
python -m venv .env
source .env/bin/activate  # On Windows: .env\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:

```bash
export ENDAVA_OPENAI_API_KEY=your_api_key_here
```

4. Run the server:

```bash
python main.py
```

The API will be available at `http://localhost:8181` and can be tested with Bruno collection`DavaX Conversational.json`.

## API Endpoints

### POST `/chat`

Send a message to the chatbot.

**Request Body:**

```json
{
  "text": "Hello, how are you?",
  "image": "<base64-encoded-image> / <image-url>",
  "audio": "<base64-encoded-audio> / <audio-url>"
}
```

**Response:**

```json
{
  "text": "I'm doing great, thanks for asking!",
  "image": "<base64-encoded-image>",
  "audio": "<base64-encoded-audio>"
}
```

### GET `/health`

Check if the service is running.

**Response:**

```json
{
  "status": "up"
}
```
