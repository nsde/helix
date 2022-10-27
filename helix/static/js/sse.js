function receive(data) {
    myName = document.getElementById('username-label').textContent.trim();

    if (data.includes('¤')) {
        // New day message
        var dayElement = document.createElement('div');
        dayElement.className = 'hx-message hx-day';
        dayElement.innerHTML = data.split('¤')[1]
        document.getElementById('chat-history').appendChild(dayElement);
        return;
    }

    author = data.split('¯')[1].trim();
    content = data.split('¯')[2];
    time = data.split('¯')[0];
    
    var msgElement = document.createElement('div');
    msgElement.className = 'hx-message';

    if (content.includes('»@')) {
        // Welcome message
        msgElement.classList.add('hx-system')

        var iconElement = document.createElement('div');
        iconElement.className = 'bi bi-arrow-right hx-join';
        msgElement.appendChild(iconElement);
        msgElement.insertAdjacentHTML('beforeend',  author + ' is online'); // [!] XSS WARNING [!]
    }

    else {              
        // Normal message
        if (author === myName) {
            msgElement.classList.add('hx-own')
        }
        else {
            msgElement.classList.add('hx-foreign')
        }

        document.getElementById('chat-history').appendChild(msgElement);
        
        var contentElement = document.createElement('div');
        contentElement.className = 'hx-content';
        msgElement.appendChild(contentElement);
        
        if (!(author === myName)) {
            var authorElement = document.createElement('div');
            authorElement.className = 'hx-author';
            authorElement.innerText = author;
            contentElement.appendChild(authorElement);
        }
        
        var timeElement = document.createElement('span');
        timeElement.className = 'hx-time';
        timeElement.innerText = time;

        contentElement.insertAdjacentHTML('beforeend', content); // [!] XSS WARNING [!]
        contentElement.appendChild(timeElement);
    }
}

function sse() {
    var source = new EventSource('/api/stream');
    
    source.onmessage = function(e) {
        receive(e.data);
        window.scrollTo(0, document.body.scrollHeight);
    };
}

// API
function post(content) {
    var xhr = new XMLHttpRequest();
    
    xhr.open('POST', '/api/send', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        room: window.location.href.split('@').pop(),
        message: content
    }));

}

// Key Bindings
window.addEventListener("keydown", (event) => {
    if (event.key == 'Enter' && document.getElementById('message-input').value != '') {
        post(document.getElementById('message-input').value);
        document.getElementById('message-input').value = '';
    }

}, true);

sse();

window.onload = function() {
    post('»@' + document.getElementById('username-label').textContent.trim()) // join message
}

