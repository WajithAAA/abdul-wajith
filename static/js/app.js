let video;
let stream;
let startButton;
let stopButton;

// When the page is loaded, set up the event listeners for the start and stop buttons
window.addEventListener('load', function() {
  startButton = document.getElementById('startButton');
  startButton.addEventListener('click', startCamera);

  stopButton = document.getElementById('stop');
  stopButton.addEventListener('click', stopCamera);
});

// Start the camera and set up the video element
function startCamera() {
  // Get the video element
  video = document.getElementById('video');

  // Use the getUserMedia API to get access to the camera
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(mediaStream) {
      // Save the stream so we can stop it later
      stream = mediaStream;

      // Set the video source to the camera stream
      video.srcObject = mediaStream;

      // Start playing the video
      video.play();

      // Call the API every 500ms to get the expression prediction and update the video
      setInterval(function() {
        // Get the current video frame as an image
        let canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        let image = canvas.toDataURL('image/jpeg');

        // Send the image to the API and get the expression prediction
        fetch('/expression_prediction', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ image: image })
        })
        .then(response => response.json())
        .then(function(data) {
          // Display the expression prediction on the video
          let prediction = data.result;
          let context = video.getContext('2d');
          context.font = '24px Arial';
          context.fillStyle = 'white';
          context.fillText(prediction, 10, 30);
        })
        .catch(function(error) {
          console.log(error);
        });
      }, 500);
    })
    .catch(function(error) {
      console.log(error);
    });
}

// Stop the camera and reset the video element
function stopCamera() {
  // Stop the camera stream
  stream.getTracks()[0].stop();

  // Reset the video element
  video.srcObject = null;
}
