import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const App = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([
    {
      sender: 'ai',
      text: '👋 Hello! I\'m your AI assistant powered by Groq LLaMA 3.1. How can I help you today?',
      timestamp: new Date()
    }
  ]);
  const [isChatActive, setIsChatActive] = useState(true);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const chatContainerRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory, isTyping]);

  useEffect(() => {
    if (!conversationId) {
      setConversationId(`chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
    }
  }, [conversationId]);

  const sendMessage = async (event) => {
    event.preventDefault();
    if (message.trim() === '' || loading) return;

    const userMessage = {
      sender: 'user',
      text: message.trim(),
      timestamp: new Date()
    };

    setLoading(true);
    setIsTyping(true);
    setChatHistory((prevHistory) => [...prevHistory, userMessage]);
    const currentMessage = message;
    setMessage('');

    try {
      const response = await fetch(`http://localhost:8000/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentMessage,
          conversation_id: conversationId,
          role: 'user'
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Simulate typing delay for better UX
      setTimeout(() => {
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { sender: 'ai', text: data.response, timestamp: new Date() },
        ]);
        setIsTyping(false);
      }, 1000);

    } catch (error) {
      console.error('Error:', error);
      setTimeout(() => {
        setChatHistory((prevHistory) => [
          ...prevHistory,
          {
            sender: 'ai',
            text: '❌ Sorry, I encountered an error. Please check if the backend server is running and try again.',
            timestamp: new Date(),
            isError: true
          },
        ]);
        setIsTyping(false);
      }, 1000);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const clearChat = () => {
    setChatHistory([{
      sender: 'ai',
      text: '👋 Chat cleared! How can I help you today?',
      timestamp: new Date()
    }]);
    setConversationId(`chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -inset-10 opacity-50">
          <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl animate-blob"></div>
          <div className="absolute top-1/3 right-1/4 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-2000"></div>
          <div className="absolute bottom-1/4 left-1/3 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-4000"></div>
        </div>
      </div>

      {/* Main Chat Container */}
      <div className="relative w-full max-w-4xl bg-black/20 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/10 overflow-hidden">

        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 backdrop-blur-sm p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center text-2xl animate-pulse">
                  🤖
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-black/20 animate-ping"></div>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">AI Assistant</h1>
                <p className="text-purple-200 text-sm">Powered by Groq LLaMA 3.1</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-green-500/20 px-3 py-1 rounded-full">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-green-200 text-sm">Online</span>
              </div>
              <button
                onClick={clearChat}
                className="p-2 text-white/60 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200"
                title="Clear Chat"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div
          ref={chatContainerRef}
          className="h-96 lg:h-[500px] overflow-y-auto p-6 space-y-6 scroll-smooth"
          style={{
            scrollbarWidth: 'thin',
            scrollbarColor: 'rgba(255,255,255,0.3) transparent'
          }}
        >
          {chatHistory.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
            >
              <div className={`flex max-w-xs lg:max-w-md ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'} items-end space-x-3`}>

                {/* Avatar */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm ${msg.sender === 'user'
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                    : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  }`}>
                  {msg.sender === 'user' ? '👤' : '🤖'}
                </div>

                {/* Message Bubble */}
                <div className="flex flex-col">
                  <div className={`px-4 py-3 rounded-2xl ${msg.sender === 'user'
                      ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-br-md'
                      : msg.isError
                        ? 'bg-red-500/20 text-red-200 border border-red-500/30 rounded-bl-md'
                        : 'bg-white/10 text-white backdrop-blur-sm border border-white/10 rounded-bl-md'
                    } shadow-lg`}>
                    <p className="text-sm lg:text-base leading-relaxed">{msg.text}</p>
                  </div>
                  <span className={`text-xs text-white/40 mt-1 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}>
                    {formatTime(msg.timestamp)}
                  </span>
                </div>
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex justify-start animate-fadeIn">
              <div className="flex items-end space-x-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center text-sm">
                  🤖
                </div>
                <div className="bg-white/10 backdrop-blur-sm border border-white/10 rounded-2xl rounded-bl-md px-4 py-3">
                  <div className="flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className="text-white/60 text-sm">AI is thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        {isChatActive && (
          <div className="p-6 border-t border-white/10 bg-black/20 backdrop-blur-sm">
            <form onSubmit={sendMessage} className="flex items-end space-x-4">
              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full p-4 pr-12 bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white placeholder-white/50 resize-none transition-all duration-200"
                  placeholder="Type your message here... (Press Enter to send)"
                  rows="1"
                  style={{
                    minHeight: '56px',
                    maxHeight: '120px',
                  }}
                  disabled={loading}
                />
                <div className="absolute right-3 bottom-3 text-white/30">
                  <span className="text-xs">⏎</span>
                </div>
              </div>

              <button
                type="submit"
                className={`p-4 rounded-2xl font-medium transition-all duration-200 flex items-center space-x-2 ${loading || !message.trim()
                    ? 'bg-gray-600/50 text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-500 to-blue-500 text-white hover:from-purple-600 hover:to-blue-600 hover:scale-105 shadow-lg hover:shadow-purple-500/25'
                  }`}
                disabled={loading || !message.trim()}
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                )}
                <span className="hidden sm:inline">Send</span>
              </button>
            </form>

            <div className="mt-3 flex items-center justify-between text-xs text-white/40">
              <span>Conversation ID: {conversationId?.slice(-8)}</span>
              <span>Messages: {chatHistory.length}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;