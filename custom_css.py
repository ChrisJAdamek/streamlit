<style>
  body {
    background-color: #000000;
    font-family: 'Courier New', monospace;
  }

  .stApp {
    padding: 2rem;
  }

  .chat-container {
    background-color: #000000;
    border: 2px solid #00ff00;
    border-radius: 10px;
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    overflow-y: scroll;
    height: 500px;
  }

  .message {
    color: #00ff00;
    white-space: nowrap;
    overflow: hidden;
    animation: typing 2s steps(30, end), blink-caret 0.5s step-end infinite;
  }

  @keyframes typing {
    from {
      width: 0;
    }
    to {
      width: 100%;
    }
  }

  @keyframes blink-caret {
    50% {
      border-color: transparent;
    }
  }
</style>
