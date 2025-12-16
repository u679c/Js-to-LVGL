const display = document.getElementById('display');
const btn = document.getElementById('action-btn');
const messages = ["当前状态：等待", "当前状态：运行", "当前状态：完成"];
let idx = 0;

btn.addEventListener('click', () => {
  idx = (idx + 1) % messages.length;
  display.textContent = messages[idx];
});
