<<<<<<< HEAD
# chatbot
A simple chatbot using Groq API
=======
# 🤖 AI Chatbot - Powered by Groq LLaMA 3.1

A modern, full-stack AI chatbot application featuring a beautiful React frontend and a robust FastAPI backend. Built with cutting-edge technologies to deliver lightning-fast AI conversations with an exceptional user experience.

![Chatbot Demo](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Tailwind](https://img.shields.io/badge/TailwindCSS-3.0-blue)

## ✨ Features

### 🎨 **Modern UI/UX**
- **Glassmorphism Design** - Beautiful, modern interface with blur effects
- **Animated Gradients** - Dynamic background with floating blob animations
- **Real-time Typing Indicators** - See when AI is thinking
- **Smooth Animations** - Fade-in effects and micro-interactions
- **Responsive Design** - Works perfectly on desktop and mobile
- **Dark Theme** - Eye-friendly design for extended conversations

### 🧠 **AI Capabilities**
- **Groq LLaMA 3.1** - Ultra-fast AI responses
- **Conversation Memory** - Maintains context throughout the chat
- **Multiple Conversation Support** - Each session has a unique ID
- **Error Handling** - Graceful handling of API errors
- **Real-time Status** - Connection status indicators

### 🚀 **Performance**
- **Lightning Fast** - Groq's optimized inference for sub-second responses
- **Efficient Backend** - FastAPI with async/await patterns
- **Modern Frontend** - Vite for instant hot module replacement
- **Optimized Build** - Production-ready with code splitting

## 🏗️ Architecture

```
CHATBOT/
├── backend/          # FastAPI Python backend
│   ├── app.py       # Main application
│   ├── requirements.txt
│   └── .env         # Environment variables
├── frontend/        # React Vite frontend
│   └── chatbotui/   # Main UI application
└── README.md        # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn
- Groq API Key ([Get one here](https://console.groq.com/))

### 1. Clone the Repository
```bash
git clone https://github.com/ryankamande/chatbot.git
cd chatbot
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Start the backend server
python app.py
```
Backend will run on `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend/chatbotui
npm install
npm run dev
```
Frontend will run on `http://localhost:5173`

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### API Configuration
The frontend is configured to connect to the backend at `http://localhost:8000`. To change this, update the API URL in the frontend configuration.

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

### Main Endpoints
- `POST /chat/` - Send a message to the AI
- `POST /debug/` - Debug endpoint for testing
- `POST /test/` - Simple test endpoint

## 🛠️ Development

### Backend Development
```bash
cd backend
# Install in development mode
pip install -r requirements.txt

# Run with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend/chatbotui
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🎨 Customization

### Adding New Features
1. **Backend**: Add new endpoints in `app.py`
2. **Frontend**: Create new components in `src/components/`
3. **Styling**: Modify `src/App.css` and Tailwind classes

### Theming
The app uses a purple/blue gradient theme. Customize colors in:
- Tailwind config: `tailwind.config.js`
- CSS variables: `src/index.css`

## 🚢 Deployment

### Backend Deployment
```bash
cd backend
# Using uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000

# Or using gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment
```bash
cd frontend/chatbotui
npm run build
# Deploy the dist/ folder to your hosting service
```

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example for backend
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** - For providing ultra-fast AI inference
- **FastAPI** - For the excellent Python web framework
- **React** - For the powerful frontend framework
- **Tailwind CSS** - For the utility-first CSS framework
- **Vite** - For the lightning-fast build tool

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ryankamande/chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ryankamande/chatbot/discussions)
- **Email**: [Your Email](mailto:your.email@example.com)

## 🔮 Future Features

- [ ] Voice input/output
- [ ] File upload support
- [ ] Multiple AI model support
- [ ] Chat export functionality
- [ ] User authentication
- [ ] Chat history persistence
- [ ] Real-time collaboration
- [ ] Mobile app

---

**Built with ❤️ by [Ryan Kamande](https://github.com/ryankamande)**

*Star ⭐ this repository if you found it helpful!*
>>>>>>> 8db5c0d (Add README.md with project overview, features, setup instructions, and contribution guidelines)
