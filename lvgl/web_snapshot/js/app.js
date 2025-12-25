const display = document.getElementById('display');
const btn = document.getElementById('action-btn');
const messages = ["now：waiting", "now：running", "now：completed"];
let idx = 0;

btn.addEventListener('click', () => {
  idx = (idx + 1) % messages.length;
  display.textContent = messages[idx];
});
