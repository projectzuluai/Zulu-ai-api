# Overview

Zulu AI API is a production-ready FastAPI backend service that generates complete full-stack applications based on user ideas. The service can operate in two modes: mock generation (hardcoded examples) and live AI generation using Google's Gemini API. It creates both React frontend and FastAPI backend code, providing a complete application scaffold for rapid prototyping and development.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **FastAPI**: Chosen for its high performance, automatic API documentation, and excellent async support
- **Uvicorn**: ASGI server for running the FastAPI application with hot reload capabilities
- **Pydantic**: Used for data validation and settings management through BaseSettings

## Application Structure
- **Modular Design**: Clean separation of concerns with dedicated modules for routes, services, and configuration
- **Environment-Based Configuration**: Uses `.env` files and Pydantic Settings for flexible deployment configurations
- **Dual Generation Modes**: Mock mode for development/testing and live mode for production AI generation

## API Design
- **RESTful Endpoints**: Clean API structure with versioned routes (`/api/v1/`)
- **Standardized Responses**: Consistent JSON response format across all endpoints
- **Error Handling**: Proper HTTP status codes and error messages with FastAPI's exception handling

## Code Generation Architecture
- **Service Layer Pattern**: Business logic separated into dedicated service modules
- **File System Management**: Automated directory creation and file writing for generated applications
- **Template-Based Generation**: Mock mode uses predefined templates while live mode leverages AI for dynamic generation

## CORS Configuration
- **Permissive CORS**: Currently allows all origins for development flexibility
- **Production Ready**: Designed to be easily configurable for specific origins in production

# External Dependencies

## AI Services
- **Google Gemini API**: Primary AI service for live code generation mode
- **API Key Authentication**: Secure key-based authentication for Gemini services

## Python Libraries
- **FastAPI**: Web framework with automatic OpenAPI documentation
- **Uvicorn**: ASGI server with hot reload for development
- **Google GenerativeAI**: Official client library for Google's Gemini API
- **Python-dotenv**: Environment variable management from `.env` files
- **Python-slugify**: URL-safe string generation for folder names
- **Python-multipart**: File upload support for FastAPI
- **Pydantic-settings**: Configuration management with environment variable binding

## Development Tools
- **Hot Reload**: Uvicorn's reload functionality for development efficiency
- **Environment Variables**: Flexible configuration through `.env` files
- **Generated Output Directory**: File system-based output for generated applications

## Optional Integrations
- The system is designed to support additional AI providers or generation methods through the service layer abstraction
- Database integration capabilities can be added through the existing modular architecture