// Инициализация элементов
const workspace = document.querySelector('.task-workspace');
const chatSection = document.querySelector('.chat-section');
const taskDescription = document.querySelector('.task-description');
const codeEditor = document.querySelector('.code-editor');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

// Функционал ресайза
let isResizing = false;
let currentResizer;

// Создаём вертикальный резайзер
const verticalResizer = document.createElement('div');
verticalResizer.className = 'resize-handle vertical';
workspace.insertBefore(verticalResizer, taskDescription);

// Создаём горизонтальный резайзер
const horizontalResizer = document.createElement('div');
horizontalResizer.className = 'resize-handle horizontal';
taskDescription.parentNode.insertBefore(horizontalResizer, codeEditor);

// Обработчики ресайза
verticalResizer.addEventListener('mousedown', initResize);
horizontalResizer.addEventListener('mousedown', initResizeHorizontal);

function initResize(e) {
    isResizing = true;
    currentResizer = e.target;
    document.addEventListener('mousemove', resize);
    document.addEventListener('mouseup', stopResize);
}

function resize(e) {
    if (!isResizing) return;
    if (currentResizer.classList.contains('vertical')) {
        const chatWidth = e.clientX - workspace.getBoundingClientRect().left;
        const totalWidth = workspace.offsetWidth;
        
        chatSection.style.width = `${chatWidth}px`;
        taskDescription.style.width = `${totalWidth - chatWidth - 10}px`;
        codeEditor.style.width = `${totalWidth - chatWidth - 10}px`;
    }
}

function initResizeHorizontal(e) {
    isResizing = true;
    currentResizer = e.target;
    document.addEventListener('mousemove', resizeHorizontal);
    document.addEventListener('mouseup', stopResize);
}

function resizeHorizontal(e) {
    if (!isResizing) return;
    const containerRect = workspace.getBoundingClientRect();
    const taskDescHeight = e.clientY - containerRect.top;
    
    taskDescription.style.height = `${taskDescHeight}px`;
    codeEditor.style.height = `${containerRect.height - taskDescHeight - 10}px`;
}

function stopResize() {
    isResizing = false;
    document.removeEventListener('mousemove', resize);
    document.removeEventListener('mousemove', resizeHorizontal);
    saveLayout();
}

// Сохранение и загрузка layout
function saveLayout() {
    const layout = {
        chatWidth: chatSection.style.width,
        taskDescHeight: taskDescription.style.height,
        codeEditorHeight: codeEditor.style.height
    };
    localStorage.setItem('taskViewLayout', JSON.stringify(layout));
}

// Управление сворачиванием секций
const controlButtons = document.querySelectorAll('.control-button');
controlButtons.forEach(button => {
    button.addEventListener('click', function() {
        const section = this.closest('.chat-section, .task-description, .code-editor');
        const content = section.querySelector('#chat-messages, #task-content, #code-editor');
        
        if (this.title === 'Свернуть') {
            content.style.display = 'none';
            this.textContent = '+';
            this.title = 'Развернуть';
        } else {
            content.style.display = 'block';
            this.textContent = '−';
            this.title = 'Свернуть';
        }
        
        const sectionStates = JSON.parse(localStorage.getItem('sectionStates') || '{}');
        sectionStates[section.className] = content.style.display;
        localStorage.setItem('sectionStates', JSON.stringify(sectionStates));
    });
});

// Функционал чата
chatInput.addEventListener('keypress', async function(e) {
    if (e.key === 'Enter' && this.value.trim()) {
        const message = this.value.trim();
        this.value = '';
        
        addMessage(message, 'user');
        showTypingIndicator();
        
        try {
            const response = await fetch('/ai-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            removeTypingIndicator();
            
            if (data.success) {
                addMessage(data.response, 'ai');
            } else {
                addMessage('Извините, произошла ошибка. Попробуйте позже.', 'ai');
            }
        } catch (error) {
            removeTypingIndicator();
            console.error('Error:', error);
            addMessage('Произошла ошибка при отправке сообщения.', 'ai');
        }
    }
});

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}-message`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = chatMessages.querySelector('.typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Загрузка сохранённых состояний при старте
window.addEventListener('load', () => {
    const savedLayout = JSON.parse(localStorage.getItem('taskViewLayout') || '{}');
    const sectionStates = JSON.parse(localStorage.getItem('sectionStates') || '{}');
    
    if (savedLayout.chatWidth) {
        chatSection.style.width = savedLayout.chatWidth;
    }
    if (savedLayout.taskDescHeight) {
        taskDescription.style.height = savedLayout.taskDescHeight;
        codeEditor.style.height = savedLayout.codeEditorHeight;
    }
    
    Object.entries(sectionStates).forEach(([className, state]) => {
        const section = document.querySelector(`.${className}`);
        if (section) {
            const content = section.querySelector('#chat-messages, #task-content, #code-editor');
            const button = section.querySelector('.control-button');
            
            content.style.display = state;
            if (state === 'none') {
                button.textContent = '+';
                button.title = 'Развернуть';
            }
        }
    });
});

// Инициализация подсветки синтаксиса
const codeTextarea = document.getElementById('code-editor');
const preElement = document.createElement('pre');
const codeElement = document.createElement('code');
codeElement.className = 'language-python';
preElement.appendChild(codeElement);
codeTextarea.parentNode.insertBefore(preElement, codeTextarea.nextSibling);

codeTextarea.addEventListener('input', function() {
    codeElement.textContent = this.value;
    hljs.highlightElement(codeElement);
});

// Начальная подсветка
hljs.highlightAll();

// Добавление кнопки форматирования
const formatButton = document.createElement('button');
formatButton.className = 'format-button';
formatButton.textContent = 'Форматировать код';
codeEditor.parentNode.insertBefore(formatButton, codeEditor.nextSibling);

// Функция форматирования
formatButton.addEventListener('click', function() {
    try {
        const formattedCode = prettier.format(codeEditor.value, {
            parser: "python",
            plugins: prettierPlugins,
            tabWidth: 4,
            semi: false,
            singleQuote: true
        });
        codeEditor.value = formattedCode;
        codeElement.textContent = formattedCode;
        hljs.highlightElement(codeElement);
    } catch (error) {
        console.error('Ошибка форматирования:', error);
    }
});

// После инициализации остальных элементов
const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    mode: 'python',
    theme: 'monokai',
    lineNumbers: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    indentUnit: 4,
    extraKeys: {
        'Ctrl-Space': 'autocomplete',
        'Tab': function(cm) {
            if (cm.somethingSelected()) {
                cm.indentSelection('add');
            } else {
                cm.replaceSelection('    ');
            }
        }
    }
});

editor.on('change', function() {
    codeElement.textContent = editor.getValue();
    hljs.highlightElement(codeElement);
});

document.querySelector('.run-button').addEventListener('click', async function() {
    const code = editor.getValue();
    try {
        const response = await fetch('/execute-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });
        
        const data = await response.json();
        if (data.success) {
            showOutput(data.output);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Ошибка выполнения кода');
    }
});

function showOutput(output) {
    // Создаем область вывода, если её нет
    let outputArea = document.querySelector('.output-area');
    if (!outputArea) {
        outputArea = document.createElement('div');
        outputArea.className = 'output-area';
        document.querySelector('.code-editor').appendChild(outputArea);
    }
    outputArea.innerHTML = `<pre class="success">${output}</pre>`;
}

function showError(error) {
    let outputArea = document.querySelector('.output-area');
    if (!outputArea) {
        outputArea = document.createElement('div');
        outputArea.className = 'output-area';
        document.querySelector('.code-editor').appendChild(outputArea);
    }
    outputArea.innerHTML = `<pre class="error">${error}</pre>`;
}

// Добавляем после существующих обработчиков
document.getElementById('saveTask').addEventListener('click', async function() {
    const taskData = {
        title: prompt('Введите название задачи:'),
        description: document.getElementById('task-content').textContent,
        code: editor.getValue()
    };

    try {
        const response = await fetch('/tasks/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        });
        
        const data = await response.json();
        if (data.success) {
            alert('Задача успешно сохранена!');
        }
    } catch (error) {
        alert('Ошибка при сохранении задачи');
    }
});

document.getElementById('loadTask').addEventListener('click', async function() {
    const taskId = prompt('Введите ID задачи:');
    if (!taskId) return;

    try {
        const response = await fetch(`/tasks/${taskId}`);
        const task = await response.json();
        
        document.getElementById('task-content').textContent = task.description;
        editor.setValue(task.initial_code || '');
    } catch (error) {
        alert('Ошибка при загрузке задачи');
    }
});
