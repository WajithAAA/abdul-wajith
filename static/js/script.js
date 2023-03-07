

var tablinks = document.getElementsByClassName('tab-links');
var tabcontents = document.getElementsByClassName('tab-contents');

function opentab(tabname){
    for(tablink of tablinks){
        tablink.classList.remove('active-link');
    }

    for(tabcontent of tabcontents){
        tabcontent.classList.remove('active-tab');
    }
event.currentTarget.classList.add('active-link');
document.getElementById(tabname).classList.add('active-tab');
}


var sidemenu = document.getElementById('sidemenu');

function openmenu(){
    sidemenu.style.right = '0';
}

function closemenu(){
    sidemenu.style.right = '-200px';
}

var menuItems = sidemenu.querySelectorAll('a');
for (var i = 0; i < menuItems.length; i++) {
  menuItems[i].addEventListener('click', function() {
    // Close the side menu
    closemenu();
  });
}

// const scriptURL = 'https://script.google.com/macros/s/AKfycbwefRrxf87BQEqFo7lUjkd4mvpDVwYk7aZ4KOvCKNYNpWje69m-lnh2AACcDXdpNUn0jQ/exec'
// const form = document.forms['submit-to-google-sheet']
// const msg = document.getElementById('msg')

// form.addEventListener('submit', e => {
//   e.preventDefault()
//   fetch(scriptURL, { method: 'POST', body: new FormData(form)})
//     .then(response => {
//         msg.innerHTML = "Message sent successfully"
    
//     setTimeout(function(){
//         msg.innerHTML = ""
//     }, 5000)
//     form.reset()
//     })
//     .catch(error => console.error('Error!', error.message))
// })



// emotional

// Get the form and result elements
// const form = document.getElementById('inputForm');
// const result = document.getElementById('result');
// const clearButton = document.getElementById('clearButton');

// // Add event listener for form submission
// form.addEventListener('submit', (event) => {
//   event.preventDefault();

//   // Get the user input data from the form
//   const userInput = document.getElementById('inputData').value;

//   // Send a POST request to the emotion prediction API
//   fetch('http://127.0.0.1:3345/emotion_predictions', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({
//       'input': userInput
//     })
//   })
//   .then(response => response.json())
//   .then(data => {
//     // Display the predicted emotion
    

//     // Display emotion emojis
//     const emotionEmojis = {
//       'angry': '😠',
//       'fear': '😨',
//       'joy': '😄',
//       'love': '❤️',
//       'sad': '😢',
//       'surprise': '😮'
//     };
//     const emotionEmoji = emotionEmojis[data.emotions];

//     result.innerHTML = `<h3>You are feeling ${data.emotions} ${emotionEmoji}</h3>`;
//     // Display related advice or ideas for the predicted emotion
//     const emotionAdvice = {
//       'angry': 'Take a deep breath and count to 10 before reacting.',
//       'fear': 'Face your fears and challenge negative thoughts.',
//       'joy': 'Celebrate the moment and share your joy with others.',
//       'love': 'Express your feelings and show appreciation for loved ones.',
//       'sad': 'Allow yourself to feel your emotions and seek support from others.',
//       'surprise': 'Embrace the unexpected and stay open to new experiences.'
//     };
//     const advice = emotionAdvice[data.emotions];
//     result.innerHTML += `<p>${advice}</p>`;

//     // Show the result and clear button
//     result.classList.remove('d-none');
//     clearButton.classList.remove('d-none');
//   })
//   .catch(error => {
//     console.error('Error:', error);
//   });
// });

// // Add event listener for clear button click
// clearButton.addEventListener('click', () => {
//   // Clear the form and result elements
//   form.reset();
//   result.innerHTML = '';
//   result.classList.add('d-none');
//   clearButton.classList.add('d-none');
// });

const form = document.getElementById('inputForm');
const resultDiv = document.getElementById('result');
const clearButton = document.getElementById('clearButton');

form.addEventListener('submit', function(event) {
  event.preventDefault();
  const inputData = document.getElementById('inputData').value;
  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        resultDiv.innerHTML = 'Emotion: ' + response.emotions;
        resultDiv.classList.remove('d-none');
        clearButton.classList.remove('d-none');
      } else {
        resultDiv.innerHTML = 'Error: ' + xhr.status;
        resultDiv.classList.remove('d-none');
      }
    }
  }
  xhr.open('POST', 'http://127.0.0.1:3345/emotion_predictions', true);
  xhr.setRequestHeader('Content-type', 'application/json');
  xhr.send(JSON.stringify({inputData: inputData}));
});

clearButton.addEventListener('click', function(event) {
  resultDiv.innerHTML = '';
  resultDiv.classList.add('d-none');
  clearButton.classList.add('d-none');
});


 