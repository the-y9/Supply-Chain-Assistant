import React from 'react';

export default function LandingPage( {sendMessage, newMessage, setNewMessage, userColor, fontFamily, placeholder}) {
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
</>  );
}
