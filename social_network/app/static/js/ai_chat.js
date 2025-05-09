document.addEventListener('DOMContentLoaded', () => {
  const genType     = document.getElementById('generationType');
  const modelSelect = document.getElementById('modelType');
  const enhancedBtn = document.getElementById('enhancedMode');
  const helpBtn     = document.querySelector('.help-btn');
  const modal       = document.getElementById('helpModal');
  const modalClose  = document.querySelector('.modal-close');
  const chatMsgs    = document.getElementById('chatMessages');
  const input       = document.getElementById('messageInput');
  const sendBtn     = document.getElementById('sendBtn');
  const avatarImg   = document.getElementById('avatar');

  // toggle controls for image/text
  function updateControls() {
    const isImage = genType.value === 'image';
    modelSelect.style.display = isImage ? 'none' : '';
    enhancedBtn.style.display = isImage ? 'none' : '';
    helpBtn.style.display = isImage ? 'none' : '';
  }
  genType.addEventListener('change', updateControls);
  updateControls();

  // enhanced mode toggle
  enhancedBtn.addEventListener('click', () => enhancedBtn.classList.toggle('active'));

  // modal open/close
  helpBtn.addEventListener('click', () => modal.style.display = 'flex');
  modalClose.addEventListener('click', () => modal.style.display = 'none');
  modal.addEventListener('click', e => { if (e.target === modal) modal.style.display = 'none'; });

  // simple markdown parser
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

  // add message to chat
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

  // send to server
  function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    input.value = '';
    avatarImg.src = '/static/images/Thinking_avatar.svg';

    fetch('/ai-chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        message: text,
        model: modelSelect.value,
        type: genType.value,
        enhanced: enhancedBtn.classList.contains('active')
      })
    })
    .then(r => r.ok ? r.json() : Promise.reject(`Status ${r.status}`))
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

  // enter or click
  input.addEventListener('keypress', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
  sendBtn.addEventListener('click', sendMessage);
});