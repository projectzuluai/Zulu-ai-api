# Zulu AI API

A production-ready FastAPI backend for generating AI-powered applications. This service can generate complete React frontends and FastAPI backends based on your ideas using either mock data or live AI generation with Google's Gemini.

## Features

- **Dual Mode Operation**: Switch between mock generation and live AI generation
- **Complete App Generation**: Creates both frontend (React) and backend (FastAPI) code
- **Production Ready**: Includes proper error handling, CORS, and input validation
- **Easy Setup**: Simple environment configuration
- **RESTful API**: Clean API endpoints for app generation

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   
   The application uses environment variables for configuration:
   - `AI_MODE`: Set to `mock` for hardcoded examples or `live` for AI generation
   - `GEMINI_API_KEY`: Your Google Gemini API key (required for live mode)

   To set up your environment:
   - For mock mode: No additional setup required
   - For live mode: You'll need a Google Gemini API key

## Usage

### Starting the Server

Run the FastAPI server with:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 5000
```

The server will start on `http://localhost:5000`

### API Endpoints

#### 1. Generate App
**POST** `/api/v1/generate_app`

Generate a complete application based on your idea.

**Request Body:**
```json
{
  "idea": "note taking app"
}
```

**Response:**
```json
{
  "message": "App generated successfully!",
  "generated_files": {
    "backend": "generated/note-taking-app/backend/main.py",
    "frontend": "generated/note-taking-app/frontend/App.js"
  },
  "mode": "mock"
}
```

#### 2. Get Modes
**GET** `/api/v1/modes`

Check available modes and current configuration.

**Response:**
```json
{
  "available_modes": ["mock", "live"],
  "current_mode": "mock",
  "gemini_configured": false
}
```

#### 3. Health Check
**GET** `/health`

Check service health and configuration.

#### 4. Root
**GET** `/`

Welcome message and basic info.

## Modes

### Mock Mode (`AI_MODE=mock`)
- Uses hardcoded templates to generate example applications
- No API key required
- Instant generation
- Good for testing and demonstrations

### Live Mode (`AI_MODE=live`)
- Uses Google's Gemini AI to generate custom applications
- Requires `GEMINI_API_KEY` environment variable
- Generates unique, tailored code based on your specific idea
- More sophisticated and contextual outputs

## Example Usage

### Using Mock Mode

1. Start the server in mock mode (default)
2. Send a POST request to generate an app:

```bash
curl -X POST "http://localhost:5000/api/v1/generate_app" \
     -H "Content-Type: application/json" \
     -d '{"idea": "task management app"}'
```

3. Check the `generated/` folder for your new app files

### Using Live Mode

1. Set your Gemini API key in environment variables
2. Set `AI_MODE=live` 
3. Generate apps with AI-powered code generation

## Generated Files

The service creates applications in the `generated/` directory with this structure:

```
generated/
└── your-app-name/
    ├── backend/
    │   └── main.py          # FastAPI backend
    └── frontend/
        └── App.js           # React frontend component
```

## Development

### File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuration and settings
│   ├── routes/
│   │   ├── __init__.py
│   │   └── generate.py      # API routes for app generation
│   └── services/
│       ├── __init__.py
│       └── codegen.py       # Core generation logic
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── generated/              # Generated applications directory
    └── .gitkeep
```

### Configuration

The application uses Pydantic for configuration management. Settings are defined in `backend/app/core/config.py` and can be overridden with environment variables.

### Error Handling

The API includes comprehensive error handling:
- Input validation using Pydantic models
- Proper HTTP status codes
- Detailed error messages for debugging
- Graceful handling of AI service failures

## Production Deployment

For production deployment:

1. Set environment variables appropriately
2. Use a production ASGI server like Gunicorn
3. Configure proper CORS origins (replace `["*"]` with specific domains)
4. Set up logging and monitoring
5. Consider rate limiting for AI generation endpoints

## Contributing

1. Follow the existing code structure and patterns
2. Add proper error handling and input validation
3. Include docstrings for new functions
4. Test both mock and live modes
5. Update this README for any new features