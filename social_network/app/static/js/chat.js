let lastMessageId = 0;
const messagesContainer = document.getElementById('messages');

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    fetch(`/send_message/${receiverId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data, true);
        input.value = '';
        lastMessageId = data.id;
    });
}

function appendMessage(message, isSent) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isSent ? 'sent' : 'received'}`;
    messageDiv.innerHTML = `
        <div class="message-content">${message.content}</div>
        <div class="message-info">
            <span class="message-time">${message.timestamp}</span>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateChat() {
    fetch(`/api/get_new_messages/${lastMessageId}`)
        .then(response => response.json())
        .then(messages => {
            messages.forEach(message => {
                if (message.id > lastMessageId) {
                    appendMessage(message, message.sender_id === currentUserId);
                    lastMessageId = message.id;
                }
            });
        });
}

// Обновление чата каждые 3 секунды
setInterval(updateChat, 3000);

// Автопрокрутка при загрузке
messagesContainer.scrollTop = messagesContainer.scrollHeight;
