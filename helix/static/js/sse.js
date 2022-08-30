function sse() {
    var source = new EventSource('/api/stream');
    
    source.onmessage = function(e) {
        myName = document.getElementById('username-label').textContent.trim();
        author = e.data.split('¯')[1].trim();
        content = e.data.split('¯')[2];
        time = e.data.split('¯')[0];

        var msgElement = document.createElement('div');
        msgElement.className = 'hx-message';

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
        
        contentElement.innerText = content;
        
        if (!(author === myName)) {
            var authorElement = document.createElement('div');
            authorElement.className = 'hx-author';
            authorElement.innerText = author;
            contentElement.appendChild(authorElement);
        }
        
        var timeElement = document.createElement('span');
        timeElement.className = 'hx-time';
        timeElement.innerText = time;
        contentElement.appendChild(timeElement);

        // out.textContent = e.data + '\\n' + out.textContent;

        window.scrollTo(0, document.body.scrollHeight);
    };
}

// Key Bindings
window.addEventListener("keydown", (event) => {
    if (event.key == 'Enter' && document.getElementById('message-input').value != '') {
        var xhr = new XMLHttpRequest();

        xhr.open('POST', '/api/send', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            message: document.getElementById('message-input').value
        }));

        document.getElementById('message-input').value = '';
    }

}, true);

sse();
