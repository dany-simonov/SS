// Открытие/закрытие панели настроек
function toggleSettings() {
  const panel = document.getElementById('settingsPanel');
  panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
}

// Основной блок, выполняемый после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    // Переключение списка провайдеров: текстовые ↔ картинные
    // Перемещено внутрь DOMContentLoaded для доступности
    window.__addMessage = addMessage;
    function updateModelLists() {
      const genType = document.getElementById('generationType');
      const textSelect = document.getElementById('modelType');
      const imageSelect = document.getElementById('imageModelType');
      if (genType.value === 'image') {
        textSelect.parentElement.style.display = 'none';
        imageSelect.parentElement.style.display = '';
      } else {
        textSelect.parentElement.style.display = '';
        imageSelect.parentElement.style.display = 'none';
      }
    }

    // Инициализация переключения моделей
    updateModelLists();
    document.getElementById('generationType')
            .addEventListener('change', updateModelLists);

    // Привязка обработчика для кнопки настроек
    document.getElementById('settingsToggle')
            .addEventListener('click', toggleSettings);
    
    // Получение всех необходимых элементов DOM
    const genType = document.getElementById('generationType');
    const modelSelect = document.getElementById('modelType');
    const imageModelSelect = document.getElementById('imageModelType');
    const enhancedBtn = document.getElementById('enhancedMode');
    const helpBtn = document.querySelector('.help-btn');
    const modal = document.getElementById('helpModal');
    const modalClose = document.querySelector('.modal-close');
    const chatMsgs = document.getElementById('chatMessages');
    const input = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const avatarImg = document.getElementById('avatar');

    // Проверка наличия всех элементов (для отладки)
    console.log('Проверка элементов:', {
        genType, modelSelect, imageModelSelect, enhancedBtn,
        helpBtn, modal, modalClose, chatMsgs, input, sendBtn, avatarImg
    });

    // Переключение элементов управления в зависимости от типа генерации (текст/изображение)
    function updateControls() {
        if (!genType) {
            console.error('Элемент generationType не найден');
            return;
        }
        
        const isImage = genType.value === 'image';
        
        // Проверяем наличие элементов перед обращением к их свойствам
        if (modelSelect) {
            modelSelect.style.display = isImage ? 'none' : '';
        } else {
            console.error('Элемент modelType не найден');
        }
        
        if (enhancedBtn) {
            enhancedBtn.style.display = isImage ? 'none' : '';
        } else {
            console.error('Элемент enhancedMode не найден');
        }
        
        if (helpBtn) {
            helpBtn.style.display = isImage ? 'none' : '';
        } else {
            console.error('Элемент help-btn не найден');
        }
    }

    // Привязка обработчика для переключения типа генерации
    if (genType) {
        genType.addEventListener('change', updateControls);
        updateControls(); // Вызываем функцию при инициализации
    } else {
        console.error('Не удалось привязать обработчик к generationType - элемент не найден');
    }

    // Обработчик для кнопки расширенного режима
    if (enhancedBtn) {
        enhancedBtn.addEventListener('click', () => enhancedBtn.classList.toggle('active'));
    }

    // Обработчики для модального окна помощи
    if (helpBtn && modal) {
        helpBtn.addEventListener('click', () => modal.style.display = 'flex');
    }
    
    if (modalClose && modal) {
        modalClose.addEventListener('click', () => modal.style.display = 'none');
        modal.addEventListener('click', e => { if (e.target === modal) modal.style.display = 'none'; });
    }

    // Простой парсер Markdown для форматирования сообщений
    function parseMarkdown(text) {
        // code blocks ```
        text = text.replace(/```([\s\S]+?)```/g, '<pre><code>$1</code></pre>');
        // inline code `
        text = text.replace(/`([^`]+?)`/g, '<code>$1</code>');
        // bold **text**
        text = text.replace(/\*\*([^*]+?)\*\*/g, '<strong>$1</strong>');
        // italic *text*
        text = text.replace(/\*([^*]+?)\*/g, '<em>$1</em>');
        // line breaks
        text = text.replace(/\n/g, '<br>');
        return text;
    }

    // Добавление сообщения в чат
    function addMessage(raw, who) {
        const wrapper = document.createElement('div');
        wrapper.className = who === 'ai' ? 'ai-message' : 'user-message';

        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = parseMarkdown(raw);

        wrapper.appendChild(content);

        if (who === 'ai') {
            const copyBtn = document.createElement('button');
            copyBtn.textContent = 'Copy';
            copyBtn.className = 'copy-btn';
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(content.textContent);
                copyBtn.textContent = 'Copied';
                setTimeout(() => copyBtn.textContent = 'Copy', 2000);
            });
            wrapper.appendChild(copyBtn);
        }

        chatMsgs.appendChild(wrapper);
        chatMsgs.scrollTop = chatMsgs.scrollHeight;
    }

    // Функция отправки сообщения на сервер
    function sendMessage() {
        if (!input || !chatMsgs) {
            console.error('Элементы для отправки сообщения не найдены');
            return;
        }
        
        const text = input.value.trim();
        if (!text) return;
        
        addMessage(text, 'user');
        if (localStorage.getItem('ss_ai_chat_autosave') === 'true') {
            window.saveChatHistory();
        }
        input.value = '';
        
        if (avatarImg) {
            avatarImg.src = '/static/images/Thinking_avatar.svg';
        }

        // Определяем модель в зависимости от типа генерации
        const selectedModel = genType && genType.value === 'image' 
            ? (imageModelSelect ? imageModelSelect.value : '') 
            : (modelSelect ? modelSelect.value : '');

        // Отправка запроса на сервер
        fetch('/ai-chat', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                message: text,
                model: selectedModel,
                type: genType ? genType.value : 'text',
                enhanced: enhancedBtn ? enhancedBtn.classList.contains('active') : false
            })
        })
        .then(r => r.ok ? r.json() : Promise.reject(`Status ${r.status}`))
        .then(data => {
            if (data.success === false) {
                addMessage(data.message || 'Ошибка AI', 'ai');
            } else {
                addMessage(data.response, 'ai');
                if (localStorage.getItem('ss_ai_chat_autosave') === 'true') {
                    window.saveChatHistory();
                }
            }
            if (avatarImg) {
                avatarImg.src = '/static/images/Loving_Avatar.svg';
            }
        })
        .catch((error) => {
            console.error('Ошибка при отправке:', error);
            addMessage('Ошибка соединения', 'ai');
            if (avatarImg) {
                avatarImg.src = '/static/images/Basic_Avatar.svg';
            }
        });
    }

    // Привязка обработчиков для отправки сообщений
    if (input) {
        input.addEventListener('keypress', e => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
    
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
});