

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

const scriptURL = 'https://script.google.com/macros/s/AKfycbwefRrxf87BQEqFo7lUjkd4mvpDVwYk7aZ4KOvCKNYNpWje69m-lnh2AACcDXdpNUn0jQ/exec'
const form = document.forms['submit-to-google-sheet']
const msg = document.getElementById('msg')

form.addEventListener('submit', e => {
  e.preventDefault()
  fetch(scriptURL, { method: 'POST', body: new FormData(form)})
    .then(response => {
        msg.innerHTML = "Message sent successfully"
    
    setTimeout(function(){
        msg.innerHTML = ""
    }, 5000)
    form.reset()
    })
    .catch(error => console.error('Error!', error.message))
})



// emotional
document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent the form from submitting normally
  
    // get the input data from the form
    var inputData = document.getElementById('inputData').value;
  
    // call the API to process the input data
    fetch('/api/emotional-analysis', {
      method: 'POST',
      body: JSON.stringify({inputData: inputData}),
      headers: {'Content-Type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => {
      // display the results in the result div
      document.getElementById('result').innerHTML = data.result;
  
      // show the result and clear button
      document.getElementById('result').classList.remove('d-none');
      document.getElementById('clearButton').classList.remove('d-none');
    })
    .catch(error => console.error(error));
  });
  
  // add event listener to clear button
  document.getElementById('clearButton').addEventListener('click', function(event) {
    event.preventDefault(); // prevent the default behavior of the clear button
  
    // clear the input data and result
    document.getElementById('inputData').value = '';
    document.getElementById('result').innerHTML = '';
  
    // hide the result and clear button
    document.getElementById('result').classList.add('d-none');
    document.getElementById('clearButton').classList.add('d-none');
  });
  
  // hide the clear button initially
document.getElementById('clearButton').classList.add('d-none');
