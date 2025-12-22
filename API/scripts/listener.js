// Note: This file web browser JavaScript, we would need node.js for server-side JavaScript.
// server side will use the CLI to manage servers.
// Script to adjust API header and place clickable elements on the page

console.log("Listener script loaded."); //use node command line to see this log
//document.getElementById("output").innerText = "Server 1"; // run flask to see this change

const {exec} = require('child_process');
exec('node API/scripts/extraction.js', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing script: ${error}`);
        return;
    }
    console.log(`Script output: ${stdout}`);
    document.getElementById("output").innerText = stdout;
    // You can also handle stderr if needed
    if (stderr) {
        console.error(`Script stderr: ${stderr}`);
    }
});

