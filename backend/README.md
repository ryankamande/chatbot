# 🔧 Backend - AI Chatbot API

A high-performance FastAPI backend for the AI Chatbot application, powered by Groq's lightning-fast LLaMA 3.1 inference engine.

## 🚀 Features

- **FastAPI Framework** - Modern, fast web framework for APIs
- **Groq Integration** - Ultra-fast AI inference with LLaMA 3.1
- **Async/Await** - Non-blocking request handling
- **CORS Support** - Cross-origin requests enabled
- **Request Validation** - Pydantic models for data validation
- **Error Handling** - Comprehensive error management
- **Debug Endpoints** - Development and testing utilities
- **Auto Documentation** - OpenAPI/Swagger docs generation

## 🏗️ Architecture

```
backend/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── __pycache__/       # Python cache (auto-generated)
```

## 📋 Requirements

- Python 3.12+
- Groq API Key

## 🛠️ Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Create a `.env` file in the backend directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start the Server
```bash
python app.py
```

The server will start on `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints

#### `POST /chat/`
Main chat endpoint for AI conversations.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "conversation_id": "unique_conversation_id",
  "role": "user"
}
```

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking...",
  "conversation_id": "unique_conversation_id"
}
```

#### `POST /debug/`
Debug endpoint for testing request/response handling.

**Request Body:** Any JSON object
**Response:** Debug information including headers and body

#### `POST /test/`
Simple test endpoint for connectivity testing.

**Request Body:** Any JSON object
**Response:**
```json
{
  "success": true,
  "received": { /* your request data */ }
}
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |

### Server Configuration
The server runs with the following default settings:
- **Host**: `0.0.0.0` (all interfaces)
- **Port**: `8000`
- **CORS**: Enabled for all origins (development)

## 🧠 AI Configuration

### Model Settings
- **Model**: `llama-3.1-8b-instant`
- **Temperature**: `1` (creative responses)
- **Max Tokens**: `1024`
- **Top P**: `1`
- **Streaming**: `True` (for faster response delivery)

### Conversation Management
- **In-Memory Storage**: Conversations stored in Python dictionary
- **Unique IDs**: Each conversation has a unique identifier
- **Context Preservation**: Full conversation history maintained
- **Session Management**: Conversations persist until server restart

## 🛡️ Error Handling

The API handles various error scenarios:

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (inactive session)
- `422` - Unprocessable Entity (validation errors)
- `500` - Internal Server Error (API or processing errors)

### Error Response Format
```json
{
  "detail": "Error description here"
}
```

## 🔍 Logging

The application logs the following information:
- Request details (message, conversation ID, role)
- API interactions with Groq
- Error occurrences
- Debug information when using debug endpoints

## 🚀 Production Deployment

### Using Uvicorn
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production
```env
GROQ_API_KEY=your_production_groq_api_key
```

## 🔒 Security Considerations

### For Production
1. **Environment Variables**: Never commit API keys to version control
2. **CORS**: Restrict origins to your domain only
3. **Rate Limiting**: Implement request rate limiting
4. **Authentication**: Add user authentication for production use
5. **HTTPS**: Use HTTPS in production
6. **Input Validation**: Additional input sanitization may be needed

### Recommended Production CORS
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["POST"],  # Only required methods
    allow_headers=["Content-Type", "Authorization"],
)
```

## 🧪 Testing

### Manual Testing
Use the debug and test endpoints to verify functionality:

```bash
# Test endpoint
curl -X POST "http://localhost:8000/test/" \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'

# Chat endpoint
curl -X POST "http://localhost:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello", "conversation_id": "test123"}'
```

### Using Postman
1. Import the OpenAPI spec from `/docs`
2. Set up environment variables
3. Test all endpoints

## 📊 Performance

- **Response Time**: Sub-second responses with Groq
- **Concurrency**: Supports multiple simultaneous conversations
- **Memory Usage**: Efficient conversation storage
- **Scalability**: Stateless design allows horizontal scaling

## 🛠️ Development

### Code Structure
```python
# Main application components
- FastAPI app initialization
- CORS middleware setup
- Pydantic models for request/response
- Groq API integration
- Conversation management
- Error handling
```

### Adding New Features
1. Define Pydantic models for new endpoints
2. Create endpoint functions with proper typing
3. Add error handling and logging
4. Update documentation
5. Test thoroughly

### Dependencies
All dependencies are listed in `requirements.txt`:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `groq` - Groq API client
- `python-dotenv` - Environment variable loading
- `pydantic` - Data validation

## 🔧 Troubleshooting

### Common Issues

1. **"GROQ_API_KEY is not set"**
   - Ensure `.env` file exists with valid API key

2. **"422 Unprocessable Entity"**
   - Check request body format matches expected schema

3. **"Connection refused"**
   - Verify server is running on correct port

4. **CORS errors**
   - Check frontend URL is allowed in CORS settings

### Debug Mode
Enable debug logging by modifying the logging configuration in `app.py`.

## 📝 License

This backend is part of the AI Chatbot project and is licensed under the MIT License.

---

**Need help?** Check the main project README or create an issue on GitHub.
