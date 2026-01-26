# Deckard

Deckard is an AI-powered "Second Brain" agent designed to ingest, organize, and synthesize your digital life.

## Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (for local development)

### Running with Docker
```bash
docker compose up -d
```
The API will be available at `http://localhost:8000`.

## Browser Extension
Deckard includes a browser extension for Chrome and Firefox that allows you to quickly save the current page to your second brain.

### Installation

#### Chrome
1.  Navigate to `chrome://extensions`.
2.  Enable **Developer mode** in the top right corner.
3.  Click **Load unpacked**.
4.  Select the `extension` directory inside the Deckard project folder.

#### Firefox
1.  Navigate to `about:debugging`.
2.  Click **This Firefox** in the sidebar.
3.  Click **Load Temporary Add-on...**.
4.  Select the `manifest.json` file located in the `extension` directory of the Deckard project.

### Usage
1.  Click the Deckard icon in your browser toolbar.
2.  The current page Title and URL will be pre-filled.
3.  Add any optional notes.
4.  Click **Send to Deckard**.
