import os
import asyncio
from typing import Dict
from slugify import slugify
import google.generativeai as genai
from backend.app.core.config import settings


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
    model = genai.GenerativeModel('gemini-pro')
    
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
    
    # Backend prompt
    backend_prompt = f'''You are an expert Python developer. Generate a complete, production-ready FastAPI backend for a '{idea}' application.

Requirements:
- Create a fully functional FastAPI application
- Include proper CORS middleware configuration
- Add at least 5 relevant endpoints for the {idea} concept
- Use proper HTTP status codes and error handling
- Include Pydantic models for request/response validation
- Add proper documentation strings
- Make it production-ready with proper structure

Return ONLY the raw Python code for main.py without any markdown formatting, explanations, or backticks. The code should be ready to save directly to a file and run.'''

    # Frontend prompt  
    frontend_prompt = f'''You are an expert React developer. Generate a complete, production-ready React component for a '{idea}' application.

Requirements:
- Create a fully functional React App component
- Include useState and useEffect hooks
- Add proper error handling and loading states
- Style the component with inline CSS or CSS classes
- Make API calls to a backend service
- Include at least 3 interactive features relevant to {idea}
- Add proper JSX structure and component organization

Return ONLY the raw React JSX code for App.js without any markdown formatting, explanations, or backticks. The code should be ready to save directly to a file and use.'''

    try:
        # Generate backend code
        backend_code = await generate_with_gemini(backend_prompt)
        
        # Generate frontend code  
        frontend_code = await generate_with_gemini(frontend_prompt)
        
        # Clean up any potential markdown formatting
        backend_code = backend_code.replace('```python', '').replace('```', '').strip()
        frontend_code = frontend_code.replace('```javascript', '').replace('```jsx', '').replace('```', '').strip()
        
        # Write files
        backend_file = f"{app_dir}/backend/main.py"
        frontend_file = f"{app_dir}/frontend/App.js"
        
        with open(backend_file, 'w') as f:
            f.write(backend_code)
        
        with open(frontend_file, 'w') as f:
            f.write(frontend_code)
        
        return {
            "backend": backend_file,
            "frontend": frontend_file
        }
    
    except Exception as e:
        raise Exception(f"Error generating live app: {str(e)}")