const io = require('socket.io-client');
const socket = io('http://localhost:3000', {
  reconnectionDelayMax: 10000,
});

socket.on('connect', () => {
  console.log('Connected to Juice Shop Socket.IO');
  
  // xssBonusChallenge payload from config/default.yml
  const payload = `<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>`;
  console.log('Sending xssBonusPayload (length', payload.length, ')');
  socket.emit('verifyLocalXssChallenge', payload);
});

socket.on('verifyLocalXssChallenge', (data) => {
  console.log('Received response:', data);
  socket.disconnect();
});

socket.on('error', (err) => {
  console.error('Socket error:', err);
});

setTimeout(() => {
  console.log('Timeout, disconnecting');
  socket.disconnect();
  process.exit(0);
}, 3000);
