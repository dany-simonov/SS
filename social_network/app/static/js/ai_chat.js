// Обработка переключения режима генерации
document.getElementById('generationType').addEventListener('change', function() {
    const modelSelect = document.getElementById('modelType');
    const enhancedControls = document.querySelector('.enhanced-controls');
    const enhancedExplanation = document.querySelector('.enhanced-explanation');
    if (this.value === 'text') {
        modelSelect.style.display = 'block';
        enhancedControls.style.display = 'flex';
        enhancedExplanation.style.display = 'block';
    } else {
        modelSelect.style.display = 'none';
        enhancedControls.style.display = 'none';
        enhancedExplanation.style.display = 'none';
    }
});

// Обработка улучшенной генерации
const enhancedButton = document.getElementById('enhancedMode');
enhancedButton.addEventListener('click', function() {
    this.classList.toggle('active');
});

// Функции модального окна
function showModal() {
    document.getElementById('helpModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('helpModal').style.display = 'none';
}

function maximizeModal() {
    const modal = document.querySelector('.modal-content');
    modal.classList.toggle('maximized');
}

// Отправка сообщений
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const modelType = document.getElementById('modelType');
    const generationType = document.getElementById('generationType');
    const enhancedButton = document.getElementById('enhancedMode');
    const message = messageInput.value.trim();
    
    if (!message) return;

    // Добавляем сообщение пользователя в чат
    addMessage(message, 'user');
    // Очищаем поле ввода
    messageInput.value = '';

    console.log('Отправка сообщения:');
    console.log('- Модель:', modelType.value);
    console.log('- Тип генерации:', generationType.value);
    console.log('- Улучшенная генерация:', enhancedButton.classList.contains('active'));

    fetch('/ai-chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
            model: modelType.value,
            type: generationType.value,
            enhanced: enhancedButton.classList.contains('active')  // Добавляем параметр
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.response) {
            addMessage(data.response, 'ai');
        } else {
            addMessage(data.message || 'Произошла ошибка при получении ответа', 'ai');
        }
    })
    .catch(error => {
        addMessage('Ошибка соединения с сервером', 'ai');
        console.error('Ошибка:', error);
    });
}


// Добавление сообщений в чат
function addMessage(content, type) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    if (type === 'ai') {
        content = content
            // Заголовки
            .replace(/#{6}\s(.*?)(?:\n|$)/g, '<h6>$1</h6>')
            .replace(/#{5}\s(.*?)(?:\n|$)/g, '<h5>$1</h5>')
            .replace(/#{4}\s(.*?)(?:\n|$)/g, '<h4>$1</h4>')
            .replace(/#{3}\s(.*?)(?:\n|$)/g, '<h3>$1</h3>')
            .replace(/#{2}\s(.*?)(?:\n|$)/g, '<h2>$1</h2>')
            .replace(/#{1}\s(.*?)(?:\n|$)/g, '<h1>$1</h1>')
            
            // Форматирование текста
            .replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/~~(.*?)~~/g, '<del>$1</del>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            
            // Списки
            .replace(/^\s*[-+*]\s+(.*?)(?:\n|$)/gm, '<li>$1</li>')
            .replace(/^\s*(\d+)\.\s+(.*?)(?:\n|$)/gm, '<li>$2</li>')
            
            // Цитаты
            .replace(/^\s*>\s+(.*?)(?:\n|$)/gm, '<blockquote>$1</blockquote>')
            
            // Горизонтальная линия
            .replace(/^(?:[-*_]){3,}$/gm, '<hr>')
            
            // Ссылки
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
            
            // Переносы строк
            .replace(/\n/g, '<br>');
        messageDiv.innerHTML = content;
    } else {
        messageDiv.textContent = content;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Перетаскивание модального окна
let isDragging = false;
let currentX;
let currentY;
let initialX;
let initialY;
let xOffset = 0;
let yOffset = 0;

const modalContent = document.querySelector('.modal-content');

modalContent.addEventListener('mousedown', dragStart);
document.addEventListener('mousemove', drag);
document.addEventListener('mouseup', dragEnd);

function dragStart(e) {
    initialX = e.clientX - xOffset;
    initialY = e.clientY - yOffset;

    if (e.target === modalContent || e.target.closest('.modal-header')) {
        isDragging = true;
    }
}

function drag(e) {
    if (isDragging) {
        e.preventDefault();
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;
        xOffset = currentX;
        yOffset = currentY;

        setTranslate(currentX, currentY, modalContent);
    }
}

function dragEnd() {
    isDragging = false;
}

function setTranslate(xPos, yPos, el) {
    el.style.transform = `translate(${xPos}px, ${yPos}px)`;
}

// Обработка нажатия Enter
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
