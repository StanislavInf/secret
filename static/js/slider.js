var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
var value = 0;

output.innerHTML = slider.value;
const socket = io();

slider.addEventListener('input', function() {
  output.innerHTML = this.value;
  socket.emit('slider_change', { value: this.value });
});

socket.on('server_response', function(data) {
  video.style.filter = `brightness(${data.value}%)`;
});