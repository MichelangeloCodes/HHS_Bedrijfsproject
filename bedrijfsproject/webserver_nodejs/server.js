const WebSocket = require('ws');
const express = require('express');
const app = express();
const port = 3000;

// Serve static files (e.g., index.html) from the "public" folder
app.use(express.static('public'));

app.listen(port, () => {
    console.log(`Web server running at http://localhost:${port}`);
});

// WebSocket server for real-time data (port 8080)
const wss = new WebSocket.Server({ port: 8080 }, () => {
    console.log('WebSocket server running on ws://localhost:8080');
});

wss.on('connection', (ws) => {
    console.log('Client connected to WebSocket');

    // Example of receiving data (from ROS2 or any other source)
    ws.on('message', (message) => {
        console.log('Received from client: %s', message);

        try {
            const data = JSON.parse(message); // Parse the incoming JSON data
            // console.log(`Received data: Value: ${data.value}, Description: ${data.description}`);

            lastReceivedData = data;
        } catch (error) {
            console.error('Error parsing message:', error);
        }
    });

    // Simulate sending random data every 2 seconds
    setInterval(() => {

        if(lastReceivedData) {
            const data_send = JSON.stringify({
                value: lastReceivedData.value,  // Random value
                description: lastReceivedData.description,
            });
            // console.log("Sending data to client:", data_send);
            ws.send(data_send);  // Send data to the WebSocket client}

        }
    }, 2000);

    // Handle WebSocket disconnection
    ws.on('close', () => {
        console.log('Client disconnected from WebSocket');
    });
});



