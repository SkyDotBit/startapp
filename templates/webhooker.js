function webhooker() {
    console.log("=========================STARTING==========================")
    const socket = new WebSocket('ws://(Your IP address):6789')
    socket.onopen = function() {
        console.log('Connected to the server');
    }
    socket.onmessage = function(event) {
        console.log('Received message: ' + event.data);
        const outputDiv = document.getElementById('output');
        outputDiv.innerHTML += '<p>' + event.data + "</p>";
    }
    socket.CLOSED = function() {
        console.log('Disconnected from the server');
    }
}
webhooker()