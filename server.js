const WebSocket = require('ws');
const port = process.env.PORT || 8080;

const server = new WebSocket.Server({ port });

const clients = new Map();
const m="first"
server.on('connection', (socket) => {
    const clientId = Date.now().toString();
    clients.set(clientId, socket);

    console.log(`Client connected: ${clientId}`);
    socket.send(JSON.stringify({ type: 'welcome', id: clientId }));

    socket.on('message', (message) => {
        console.log(`Received: ${message}`);
        m=JSON.stringify( 'welcome'+ clientId +message)
    });

    socket.on('close', () => {
        clients.delete(clientId);
        console.log(`Client disconnected: ${clientId}`);
    });
});

console.log(`WebSocket server running on port ${port}`);

