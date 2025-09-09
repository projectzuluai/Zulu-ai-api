import os
import asyncio
from typing import Dict
from slugify import slugify
import google.generativeai as genai
from backend.app.core.config import settings
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger("zulu-ai-api")


def generate_mock_app(idea: str) -> Dict[str, str]:
    """Generate a mock app with hardcoded React and FastAPI files."""
    # Create safe folder name
    folder_name = slugify(idea)
    app_dir = f"generated/{folder_name}"
    
    # Create directory structure
    os.makedirs(f"{app_dir}/backend", exist_ok=True)
    os.makedirs(f"{app_dir}/frontend", exist_ok=True)
    
    # Mock FastAPI backend
    fastapi_content = f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="{idea.title()} API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {{"message": "Welcome to {idea.title()} API"}}

@app.get("/health")
async def health():
    return {{"status": "healthy"}}

@app.get("/items")
async def get_items():
    return {{"items": ["Item 1", "Item 2", "Item 3"]}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    # Mock React frontend
    react_content = f'''import React, {{ useState, useEffect }} from 'react';
import './App.css';

function App() {{
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {{
    fetchItems();
  }}, []);

  const fetchItems = async () => {{
    try {{
      const response = await fetch('/api/items');
      const data = await response.json();
      setItems(data.items);
    }} catch (error) {{
      console.error('Error fetching items:', error);
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <div className="App">
      <header className="App-header">
        <h1>{idea.title()}</h1>
        <p>A simple {idea} application</p>
        
        {{loading ? (
          <p>Loading...</p>
        ) : (
          <div>
            <h2>Items:</h2>
            <ul>
              {{items.map((item, index) => (
                <li key={{index}}>{{item}}</li>
              ))}}
            </ul>
          </div>
        )}}
      </header>
    </div>
  );
}}

export default App;
'''
    
    # Write files
    backend_file = f"{app_dir}/backend/main.py"
    frontend_file = f"{app_dir}/frontend/App.js"
    
    with open(backend_file, 'w') as f:
        f.write(fastapi_content)
    
    with open(frontend_file, 'w') as f:
        f.write(react_content)
    
    return {
        "backend": backend_file,
        "frontend": frontend_file
    }


async def generate_with_gemini(prompt: str) -> str:
    """Generate content using Gemini AI."""
    if not settings.gemini_api_key:
        raise ValueError("Gemini API key not configured")
    
    # Configure Gemini
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Error generating content with Gemini: {str(e)}")


async def generate_live_app(idea: str) -> Dict[str, str]:
    """Generate a live app using Gemini AI."""
    # Create safe folder name
    folder_name = slugify(idea)
    app_dir = f"generated/{folder_name}"
    
    # Create directory structure
    os.makedirs(f"{app_dir}/backend", exist_ok=True)
    os.makedirs(f"{app_dir}/frontend", exist_ok=True)
    
    # Improved Backend prompt - more strict and specific
    backend_prompt = f'''You are an expert Python developer. Generate a complete, production-ready FastAPI backend for a "{idea}". Your output MUST be a single, valid Python code file for main.py. Do not include any explanations, text outside of code comments, or markdown code blocks (no ```python or ```). The code must be runnable with `uvicorn main:app --reload` and include:
1. FastAPI app with CORSMiddleware.
2. Proper Pydantic models for data.
3. At least two working endpoints (e.g., GET and POST).
4. In-memory storage for simplicity.
5. A root endpoint returning a welcome message.
Return only the raw Python code.'''

    # Improved Frontend prompt - more strict and specific
    frontend_prompt = f'''You are an expert React developer. Generate a complete React frontend for a "{idea}" that interacts with a backend API. Your output MUST be a single, valid JavaScript code file for App.js. Do not include any explanations, text outside of code comments, or markdown code blocks (no ```js or ```). The code must be for a standard Create-React-App component and include:
1. Functional components with useState and useEffect hooks.
2. Fetch API calls to interact with the backend.
3. A form for creating items and a list to display them.
4. Basic inline styling for clarity.
Return only the raw JavaScript code.'''

    try:
        # Generate backend code with enhanced error handling
        try:
            backend_code = await generate_with_gemini(backend_prompt)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise Exception(f"Failed to generate backend code with Gemini: {str(e)}")
        
        # Generate frontend code with enhanced error handling
        try:
            frontend_code = await generate_with_gemini(frontend_prompt)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise Exception(f"Failed to generate frontend code with Gemini: {str(e)}")
        
        # Robust code cleaning for backend
        clean_backend_code = backend_code.strip()
        # Remove all markdown code block indicators if present
        if clean_backend_code.startswith("```python"):
            clean_backend_code = clean_backend_code.replace("```python", "").strip()
        if clean_backend_code.startswith("```"):
            clean_backend_code = clean_backend_code.replace("```", "").strip()
        if clean_backend_code.endswith("```"):
            clean_backend_code = clean_backend_code.replace("```", "").strip()
        # Remove any remaining backticks
        clean_backend_code = clean_backend_code.replace("```", "").strip()
        
        # Robust code cleaning for frontend
        clean_frontend_code = frontend_code.strip()
        # Remove all markdown code block indicators if present
        if clean_frontend_code.startswith("```javascript"):
            clean_frontend_code = clean_frontend_code.replace("```javascript", "").strip()
        if clean_frontend_code.startswith("```js"):
            clean_frontend_code = clean_frontend_code.replace("```js", "").strip()
        if clean_frontend_code.startswith("```jsx"):
            clean_frontend_code = clean_frontend_code.replace("```jsx", "").strip()
        if clean_frontend_code.startswith("```"):
            clean_frontend_code = clean_frontend_code.replace("```", "").strip()
        if clean_frontend_code.endswith("```"):
            clean_frontend_code = clean_frontend_code.replace("```", "").strip()
        # Remove any remaining backticks
        clean_frontend_code = clean_frontend_code.replace("```", "").strip()
        
        # Validate the code - check that cleaned code is not empty
        if not clean_backend_code or len(clean_backend_code.strip()) < 10:
            # Fall back to mock generator
            return generate_mock_app(idea)
        
        if not clean_frontend_code or len(clean_frontend_code.strip()) < 10:
            # Fall back to mock generator
            return generate_mock_app(idea)
        
        # Write files
        backend_file = f"{app_dir}/backend/main.py"
        frontend_file = f"{app_dir}/frontend/App.js"
        
        with open(backend_file, 'w') as f:
            f.write(clean_backend_code)
        
        with open(frontend_file, 'w') as f:
            f.write(clean_frontend_code)
        
        return {
            "backend": backend_file,
            "frontend": frontend_file
        }
    
    except Exception as e:
        # Enhanced error handling with clear error message
        raise Exception(f"Failed to generate code with Gemini: {str(e)}")