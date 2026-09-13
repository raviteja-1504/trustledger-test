// VULNERABILITY: Client-side XSS vulnerabilities

function displayUserContent() {
    // VULNERABILITY: DOM-based XSS using innerHTML
    var userInput = document.getElementById('userInput').value;
    document.getElementById('output').innerHTML = userInput;
}

function loadExternalScript() {
    // VULNERABILITY: Loading external script from untrusted source
    var scriptUrl = document.getElementById('scriptUrl').value;
    var script = document.createElement('script');
    script.src = scriptUrl;
    document.head.appendChild(script);
}

function setCookie() {
    // VULNERABILITY: Setting cookie without HttpOnly flag
    var sessionId = document.getElementById('sessionId').value;
    document.cookie = "session=" + sessionId + "; path=/";
}

function processJSON() {
    // VULNERABILITY: Using eval to parse JSON
    var jsonStr = document.getElementById('jsonData').value;
    var data = eval('(' + jsonStr + ')');
    console.log(data);
}

function sendData() {
    // VULNERABILITY: Sending sensitive data over HTTP
    var creditCard = document.getElementById('creditCard').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://insecure-endpoint.com/api/payment', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ card: creditCard }));
}

// VULNERABILITY: Hardcoded API key in JavaScript
var API_KEY = 'sk_live_1234567890abcdef';

function makeAPICall() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://api.example.com/data', true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + API_KEY);
    xhr.send();
}

// VULNERABILITY: Insecure random number generation for security purposes
function generateToken() {
    var token = '';
    for (var i = 0; i < 32; i++) {
        token += Math.random().toString(36).substr(2, 1);
    }
    return token;
}