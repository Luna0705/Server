const WebSocket = require('ws');

// Set the port for the WebSocket server
const port = process.env.PORT || 8080;

// Create a new WebSocket server
const server = new WebSocket.Server({ port });

// Keep track of connected clients
const clients = new Set();

console.log(`WebSocket server is running on ws://localhost:${port}`);

// Handle new client connections
server.on('connection', (socket) => {
    console.log('New client connected');
    clients.add(socket);

    // Send a welcome message to the client
    // socket.send(JSON.stringify({ type: 'welcome', message: 'Welcome to the WebSocket server!' }));

    // // Handle messages received from the client
    // socket.on('message', (data) => {
    //     console.log(`Received message: ${data}`);
    //     // Broadcast the message to all connected clients
    //     for (const client of clients) {
    //         if (client !== socket && client.readyState === WebSocket.OPEN) {
    //             client.send(data);
    //         }
    //     }
    // });

    // Handle client disconnections
    socket.on('close', () => {
        console.log('Client disconnected');
        clients.delete(socket);
    });

    // Handle errors (optional)
    socket.on('error', (error) => {
        console.error(`WebSocket error: ${error.message}`);
    });
});
