const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Enter server name: ', (answer) => {
  //document.getElementById("output").innerText = answer;
  console.log(`Server name set to: ${answer}`);
  rl.close();
  return answer;
}
);

rl.on('close', () => {
  console.log('Input closed.');
});