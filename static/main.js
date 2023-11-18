const socket = io('http://127.0.0.1:5000/upload')
socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('event', function() {
    console.log('test')
});

socket.on('redirect', function() {
    window.location.href = 'http://127.0.0.1:5000/results';
});