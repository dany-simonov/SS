(function() {
  const STORAGE_PREFIX = 'ss_ai_chat_';
  const defaults = {
    theme: 'light',
    tone: 'friendly',
    maxLength: '500',
    temperature: '0.5',
    autosave: false,
    showTimestamps: false,
    language: 'ru'
  };

  // получить или дефолт
  function loadSetting(key) {
    const v = localStorage.getItem(STORAGE_PREFIX + key);
    return v !== null ? JSON.parse(v) : defaults[key];
  }

  function saveSetting(key, value) {
    localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(value));
  }

  // элементы
  const elems = {
    theme: document.querySelectorAll('input[name="theme"]'),
    tone: document.querySelectorAll('input[name="tone"]'),
    maxLength: document.getElementById('maxLength'),
    temperature: document.getElementById('temperature'),
    autosave: document.getElementById('autosave'),
    showTimestamps: document.getElementById('showTimestamps'),
    language: document.getElementById('language')
  };

  // применение темы
  function applyTheme(val) {
    document.documentElement.dataset.theme = val;
  }

  // переключение других стилей, если нужно
  function applyShowTimestamps(val) {
    document.getElementById('chatMessages')
      .dataset.showTimestamps = val;
  }

  // инициализация контролов из хранилища
  function initControls() {
    // тема
    const theme = loadSetting('theme');
    elems.theme.forEach(r => {
      r.checked = (r.value === theme);
      r.addEventListener('change', () => {
        saveSetting('theme', r.value);
        applyTheme(r.value);
      });
    });
    applyTheme(theme);

    // тон
    const tone = loadSetting('tone');
    elems.tone.forEach(r => {
      r.checked = (r.value === tone);
      r.addEventListener('change', () => {
        saveSetting('tone', r.value);
      });
    });

    // длина
    const ml = loadSetting('maxLength');
    elems.maxLength.value = ml;
    elems.maxLength.addEventListener('change', () => {
      saveSetting('maxLength', elems.maxLength.value);
    });

    // температура
    const temp = loadSetting('temperature');
    elems.temperature.value = temp;
    elems.temperature.addEventListener('input', () => {
      saveSetting('temperature', elems.temperature.value);
    });

    // автосохранение
    const auto = loadSetting('autosave');
    elems.autosave.checked = auto;
    elems.autosave.addEventListener('change', () => {
      saveSetting('autosave', elems.autosave.checked);
      if (elems.autosave.checked) saveChatHistory();
    });

    // таймстемпы
    const ts = loadSetting('showTimestamps');
    elems.showTimestamps.checked = ts;
    elems.showTimestamps.addEventListener('change', () => {
      saveSetting('showTimestamps', elems.showTimestamps.checked);
      applyShowTimestamps(elems.showTimestamps.checked);
    });
    applyShowTimestamps(ts);

    // язык
    const lang = loadSetting('language');
    elems.language.value = lang;
    elems.language.addEventListener('change', () => {
      saveSetting('language', elems.language.value);
    });
  }

  // сохранить историю чата
  function saveChatHistory() {
    const msgs = Array.from(
      document.querySelectorAll('.message-content')
    ).map(el => el.textContent);
    localStorage.setItem(STORAGE_PREFIX + 'history', JSON.stringify(msgs));
  }

  // восстановить историю
  function loadChatHistory() {
    try {
      const data = JSON.parse(localStorage.getItem(STORAGE_PREFIX + 'history'));
      if (Array.isArray(data)) {
        const addMessage = window.__addMessage;
        data.slice(-10).forEach((text, i) => {
          addMessage(text, i % 2 === 0 ? 'user' : 'ai');
        });
      }
    } catch (_) {}
  }

  // запуск
  document.addEventListener('DOMContentLoaded', () => {
    initControls();
    if (loadSetting('autosave')) loadChatHistory();
  });

  // экспонируем saveChatHistory, чтоб дергать при каждом сообщении
  window.saveChatHistory = saveChatHistory;
})();
