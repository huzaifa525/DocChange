# DocChange

A production-ready Document QA Backend built with Flask.

## Features
- PDF document processing with OCR support
- Vector-based document search
- LLM-powered question answering
- Web search fallback
- JWT authentication
- Docker support

## Setup

1. Clone the repository:
```bash
git clone https://github.com/huzaifa525/DocChange.git
cd DocChange
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate    # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python wsgi.py
```

## Docker Deployment

```bash
docker build -t document-qa .
docker run -p 8080:8080 document-qa
```

## API Endpoints

### Upload Document
```bash
POST /api/v1/documents
Content-Type: multipart/form-data
Authorization: Bearer <token>

file: <pdf_file>
```

### Query Document
```bash
POST /api/v1/query
Content-Type: application/json
Authorization: Bearer <token>

{
    "question": "What does the document say about..."
}
```

## License
Proprietary software by CleverFlow. All rights reserved.