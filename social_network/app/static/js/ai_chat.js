document.addEventListener('DOMContentLoaded', () => {
    const genType       = document.getElementById('generationType');
    const modelSelect   = document.getElementById('modelType');
    const enhancedBtn   = document.getElementById('enhancedMode');
    const helpBtn       = document.querySelector('.help-btn');
    const modal         = document.getElementById('helpModal');
    const modalClose    = document.querySelector('.modal-close');
    const chatMsgs      = document.getElementById('chatMessages');
    const input         = document.getElementById('messageInput');
    const sendBtn       = document.querySelector('.send-btn');
    const avatarImg     = document.querySelector('.avatar-card img');
  
    // Обновление контролов при смене генерации
    const updateControls = () => {
      const isImage = genType.value === 'image';
      modelSelect.style.display   = isImage ? 'none' : '';
      enhancedBtn.style.display   = isImage ? 'none' : '';
      helpBtn.style.display       = isImage ? 'none' : '';
    };
    genType.addEventListener('change', updateControls);
    updateControls();
  
    // Переключение улучшенной генерации
    enhancedBtn.addEventListener('click', () => {
      enhancedBtn.classList.toggle('active');
    });
  
    // Открыть/закрыть модалку
    helpBtn.addEventListener('click', () => modal.style.display = 'flex');
    modalClose.addEventListener('click', () => modal.style.display = 'none');
    modal.addEventListener('click', e => { if (e.target === modal) modal.style.display = 'none' });
  
    // Добавить сообщение в чат
    function addMessage(text, cls) {
      const msg = document.createElement('div');
      msg.className = cls === 'ai' ? 'ai-message' : 'user-message';
      msg.textContent = text;
      chatMsgs.appendChild(msg);
      chatMsgs.scrollTop = chatMsgs.scrollHeight;
    }
  
    // Отправка сообщения на сервер
    function sendMessage() {
      const text = input.value.trim();
      if (!text) return;
      addMessage(text, 'user');
      input.value = '';
      avatarImg.src = '/static/images/Thinking_avatar.svg';
  
      fetch('/ai-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          model: modelSelect.value,
          type: genType.value,
          enhanced: enhancedBtn.classList.contains('active')
        })
      })
      .then(res => {
        if (!res.ok) throw new Error(`Status ${res.status}`);
        return res.json();
      })
      .then(data => {
        if (data.success === false) {
          addMessage(data.message || 'Ошибка AI', 'ai');
        } else {
          addMessage(data.response, 'ai');
        }
        avatarImg.src = '/static/images/Loving_Avatar.svg';
      })
      .catch(() => {
        addMessage('Ошибка соединения', 'ai');
        avatarImg.src = '/static/images/Basic_Avatar.svg';
      });
    }
  
    // Отправка по Enter
    input.addEventListener('keypress', e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    sendBtn.addEventListener('click', sendMessage);
  });
  