const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('', (answer) => {
  //document.getElementById("output").innerText = answer;
  //console.log(`Server name set to: ${answer}`);
  rl.close();
  return console.log(answer);
}
);

rl.on('close', () => {
  //console.log('Input closed.');
});