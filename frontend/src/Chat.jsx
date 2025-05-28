import React, { useState, useRef, useEffect } from 'react';
import LandingPage from './LandingPage';

export default function ChatGPTStyle({
  userColor = '#10a37f',
  aiColor = '#4a4a4a',
  backgroundColor = '#f7f7f8',
  fontFamily = "Papyrus, Tahoma, Geneva, Verdana, sans-serif",
  placeholder = 'Type your query...',
}) {
  const [messages, setMessages] = useState([
    { from: 'ai', text: 'Hello! How can I help you today?' },
  ]);
  const [newMessage, setNewMessage] = useState('');
  const [data, setData] = useState(null);
  const chatWindowRef = useRef(null);
  const [collapsed, setCollapsed] = useState(true);
  const navbarWidth = 360;
  const collapsedWidth = 48;

  useEffect(() => {
    // Scroll to bottom whenever messages update
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async (e) => {
  e.preventDefault();
  const text = newMessage.trim();
  if (!text) return;

  // Add user message immediately
  setMessages((msgs) => [...msgs, { from: 'user', text }]);
  setNewMessage('');

  try {
    const response = await fetch('http://127.0.0.1:8000/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: text }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    setData(data);

    const aiReply = data.answer || 'Sorry, no response from AI.';

    setMessages((msgs) => [...msgs, { from: 'ai', text: aiReply }]);
  } catch (error) {
    setMessages((msgs) => [
      ...msgs,
      { from: 'ai', text: `Error: ${error.message}` },
    ]);
  }
};

  if (!data) {
    return (
        <LandingPage
          sendMessage={sendMessage}
          newMessage={newMessage}
          setNewMessage={setNewMessage}
          userColor={userColor}
          fontFamily={fontFamily}
          placeholder={placeholder}
        />

    );
  }
  else if (data) {
return (<>
  <h1 style={{ textAlign: 'center', fontSize: '300%' }}>Smart Assisstant</h1>
  <div
    style={{
      display: 'flex',
      maxWidth: 1200,
      margin: '40px auto',
      gap: 32,
      fontFamily,
      padding: '0 16px',
      boxSizing: 'border-box',
    }}
  >
    {/* Chat section (Left) */}
    <div
      style={{
        backgroundColor,
        flex: 1,
        borderRadius: 16,
        boxShadow: '0 12px 32px rgba(0,0,0,0.12)',
        display: 'flex',
        flexDirection: 'column',
        height: '80vh',
        overflow: 'hidden',
        border: `1px solid ${aiColor}20`,
        transition: 'box-shadow 0.3s ease',
      }}
      tabIndex={-1} // to enable keyboard focus for accessibility if needed
      onFocus={(e) => e.currentTarget.style.boxShadow = `0 16px 40px ${aiColor}50`}
      onBlur={(e) => e.currentTarget.style.boxShadow = '0 12px 32px rgba(0,0,0,0.12)'}
    >
      <div
        ref={chatWindowRef}
        role="log"
        aria-live="polite"
        style={{
          flexGrow: 1,
          padding: 28,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          gap: 18,
          backgroundColor: '#fff',
        }}
      >
        {messages.map((msg, i) => {
          const isUser = msg.from === 'user';
          return (
            <div
              key={i}
              style={{
                maxWidth: '75%',
                alignSelf: isUser ? 'flex-end' : 'flex-start',
                backgroundColor: isUser ? userColor : aiColor,
                color: '#fff',
                padding: '16px 24px',
                borderRadius: 28,
                borderTopRightRadius: isUser ? 8 : 28,
                borderTopLeftRadius: isUser ? 28 : 8,
                fontSize: 16,
                lineHeight: 1.6,
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
                boxShadow: isUser
                  ? '0 3px 12px rgba(16, 163, 127, 0.35)'
                  : '0 3px 12px rgba(74, 74, 74, 0.25)',
                transition: 'background-color 0.3s ease',
                userSelect: 'text',
              }}
              aria-label={isUser ? "User message" : "AI message"}
            >
              {msg.text}
            </div>
          );
        })}
      </div>

      <form
        onSubmit={sendMessage}
        style={{
          display: 'flex',
          padding: '18px 28px',
          backgroundColor: '#fafafa',
          borderTop: '1px solid #e0e0e0',
        }}
      >
        <textarea
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder={placeholder}
          rows={1}
          style={{
            flexGrow: 1,
            resize: 'none',
            padding: '14px 20px',
            fontSize: 16,
            borderRadius: 28,
            border: `2px solid ${userColor}`,
            outline: 'none',
            fontFamily,
            boxSizing: 'border-box',
            lineHeight: 1.5,
            transition: 'border-color 0.3s',
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              sendMessage(e);
            }
          }}
          aria-label="Message input"
          onFocus={(e) => (e.target.style.borderColor = userColor + 'cc')}
          onBlur={(e) => (e.target.style.borderColor = userColor)}
        />
        <button
          type="submit"
          style={{
            marginLeft: 20,
            padding: '14px 26px',
            borderRadius: 28,
            fontWeight: '700',
            cursor: 'pointer',
            border: 'none',
            backgroundColor: userColor,
            color: '#fff',
            transition: 'background-color 0.3s, box-shadow 0.3s',
            boxShadow: '0 6px 16px rgba(16, 163, 127, 0.45)',
            userSelect: 'none',
          }}
          aria-label="Send message"
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = userColor + 'cc';
            e.currentTarget.style.boxShadow = '0 8px 20px rgba(16, 163, 127, 0.6)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = userColor;
            e.currentTarget.style.boxShadow = '0 6px 16px rgba(16, 163, 127, 0.45)';
          }}
        >
          Send
        </button>
      </form>
    </div>

    
      {/* Collapsible right navbar */}
      <div
        style={{
          position: 'fixed',
          top: 0,
          right: 0,
          height: '100vh',
          width: collapsed ? collapsedWidth : navbarWidth,
          backgroundColor: '#fff',
          borderRadius: '0 0 0 16px',
          padding: collapsed ? '16px 8px' : 28,
          boxShadow: '-4px 0 20px rgba(0,0,0,0.1)',
          overflowY: 'auto',
          borderLeft: `1px solid ${aiColor}20`,
          fontSize: 15,
          lineHeight: 1.6,
          color: '#b97006',
          zIndex: 1000,
          transition: 'width 0.3s ease, padding 0.3s ease',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Toggle button */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          style={{
            position: 'absolute',
            top: 16,
            left: collapsed ? '50%' : 10,
            transform: collapsed ? 'translateX(-50%)' : 'none',
            width: 32,
            height: 32,
            borderRadius: '50%',
            border: 'none',
            backgroundColor: aiColor,
            color: '#fff',
            cursor: 'pointer',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'left 0.3s ease',
            fontSize: 18,
            fontWeight: 'bold',
            userSelect: 'none',
            outline: 'none',
          }}
        >
          {collapsed ? '›' : '‹'}
        </button>

        {/* Content - hide when collapsed */}
        {!collapsed && (
          <>
            <h1 style={{ marginBottom: 20, marginTop: '10%' }}>Response Info</h1>
            {!data && (<p style={{textColor:'rgb(188, 188, 188)'}}
            >Details of your response will be displayed here. </p>)}
            {data && (
              <div>
                {Object.entries(data).map(([key, value], i) => {
                  if (key === 'answer') return null;
                  return (
                    <div key={i} style={{ marginBottom: 10 }}>
                      <strong style={{ textTransform: 'capitalize' }}>{key}:</strong>{' '}
                      <span>{String(value)}</span>
                    </div>
                  );
                })}
              </div>
            )}
          </>
        )}
      </div>
  </div>
</>);
  }

}
