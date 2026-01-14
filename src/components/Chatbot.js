import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  // Initialize messages from localStorage or use default
  const [messages, setMessages] = useState(() => {
    try {
      const savedMessages = localStorage.getItem('chatbot_messages');
      if (savedMessages) {
        const parsed = JSON.parse(savedMessages);
        // Convert timestamp strings back to Date objects
        return parsed.map(msg => ({
          ...msg,
          timestamp: new Date(msg.timestamp)
        }));
      }
    } catch (error) {
      console.error('Error loading chat messages:', error);
    }
    return [
      {
        text: "Hello! I'm here to help you with questions about City College of Bayawan. How can I assist you today?",
        sender: 'bot',
        timestamp: new Date()
      }
    ];
  });

  // Initialize isOpen from localStorage
  const [isOpen, setIsOpen] = useState(() => {
    try {
      const savedState = localStorage.getItem('chatbot_is_open');
      return savedState === 'true';
    } catch (error) {
      return false;
    }
  });

  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showCloseConfirm, setShowCloseConfirm] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Save messages to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem('chatbot_messages', JSON.stringify(messages));
    } catch (error) {
      console.error('Error saving chat messages:', error);
    }
  }, [messages]);

  // Save isOpen state to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('chatbot_is_open', isOpen.toString());
    } catch (error) {
      console.error('Error saving chatbot state:', error);
    }
  }, [isOpen]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Handle Escape key to close confirmation dialog
  useEffect(() => {
    if (!showCloseConfirm) return;
    
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        setShowCloseConfirm(false);
      }
    };
    
    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [showCloseConfirm]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isTyping) return;

    const userMessage = {
      text: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage.trim();
    setInputMessage('');
    setIsTyping(true);

    // TODO: Implement chatbot backend integration
    // Backend functionality will be reimplemented here
    
    setTimeout(() => {
      const botMessage = {
        text: "Chatbot backend functionality is being reimplemented. Please check back soon!",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
    }, 500);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleCloseClick = () => {
    // Only show confirmation when closing (not opening)
    if (isOpen) {
      setShowCloseConfirm(true);
    } else {
      setIsOpen(true);
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  const confirmClose = () => {
    setShowCloseConfirm(false);
    setIsOpen(false);
    // Clear messages from localStorage when user confirms closing
    try {
      localStorage.removeItem('chatbot_messages');
      localStorage.removeItem('chatbot_is_open');
      // Reset to default welcome message
      setMessages([
        {
          text: "Hello! I'm here to help you with questions about City College of Bayawan. How can I assist you today?",
          sender: 'bot',
          timestamp: new Date()
        }
      ]);
    } catch (error) {
      console.error('Error clearing chat messages:', error);
    }
  };

  const cancelClose = () => {
    setShowCloseConfirm(false);
  };

  const toggleChatbot = () => {
    if (isOpen) {
      // When closing via toggle button, also show confirmation
      setShowCloseConfirm(true);
    } else {
      setIsOpen(true);
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Parse markdown-style links and render as HTML
  const renderMessage = (text) => {
    if (!text) return text;
    
    // Simple regex to match [text](url) pattern
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    const parts = [];
    let lastIndex = 0;
    let match;
    
    while ((match = linkRegex.exec(text)) !== null) {
      // Add text before the link
      if (match.index > lastIndex) {
        parts.push({ type: 'text', content: text.substring(lastIndex, match.index) });
      }
      // Add the link
      parts.push({ type: 'link', text: match[1], url: match[2] });
      lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text
    if (lastIndex < text.length) {
      parts.push({ type: 'text', content: text.substring(lastIndex) });
    }
    
    // If no links found, return original text
    if (parts.length === 0 || (parts.length === 1 && parts[0].type === 'text')) {
      return <>{text}</>;
    }
    
    // Render with links
    return (
      <>
        {parts.map((part, index) => {
          if (part.type === 'link') {
            return (
              <a
                key={index}
                href={part.url}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  color: '#ff8c00',
                  textDecoration: 'underline',
                  fontWeight: '500'
                }}
                onClick={(e) => {
                  // Handle relative URLs
                  if (part.url.startsWith('/')) {
                    e.preventDefault();
                    window.location.href = part.url;
                  }
                }}
              >
                {part.text}
              </a>
            );
          }
          return <span key={index}>{part.content}</span>;
        })}
      </>
    );
  };

  return (
    <div className="chatbot-container">
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-header-content">
              <div className="chatbot-avatar">
                <i className="fas fa-robot"></i>
              </div>
              <div className="chatbot-header-text">
                <h3>CCB Assistant</h3>
                <p>We're here to help</p>
              </div>
            </div>
            <button 
              className="chatbot-close-btn"
              onClick={handleCloseClick}
              aria-label="Close chat"
            >
              <i className="fas fa-times"></i>
            </button>
          </div>
          
          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div 
                key={index} 
                className={`chatbot-message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}
              >
                <div className="message-content">
                  {renderMessage(msg.text)}
                </div>
                <div className="message-time">
                  {formatTime(msg.timestamp)}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="chatbot-message bot-message">
                <div className="message-content typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="chatbot-input-container">
            <input
              ref={inputRef}
              type="text"
              className="chatbot-input"
              placeholder="Type your message..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isTyping}
            />
            <button 
              className="chatbot-send-btn"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isTyping}
              aria-label="Send message"
            >
              <i className="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      )}
      
      <button 
        className={`chatbot-toggle-btn ${isOpen ? 'open' : ''}`}
        onClick={toggleChatbot}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
        aria-expanded={isOpen}
      >
        {isOpen ? (
          <i className="fas fa-times"></i>
        ) : (
          <i className="fas fa-comments"></i>
        )}
      </button>
      
      {/* Close Confirmation Dialog */}
      {showCloseConfirm && (
        <div className="chatbot-confirm-overlay" onClick={cancelClose}>
          <div className="chatbot-confirm-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="chatbot-confirm-header">
              <h3>Close Chat?</h3>
            </div>
            <div className="chatbot-confirm-body">
              <p>Closing the chat will clear all message history and you won't be able to restore it.</p>
              <p>Are you sure you want to close?</p>
            </div>
            <div className="chatbot-confirm-actions">
              <button 
                className="chatbot-confirm-btn chatbot-confirm-cancel"
                onClick={cancelClose}
              >
                Cancel
              </button>
              <button 
                className="chatbot-confirm-btn chatbot-confirm-close"
                onClick={confirmClose}
              >
                Close Chat
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
