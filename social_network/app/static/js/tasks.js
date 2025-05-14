document.addEventListener('DOMContentLoaded', () => {
    // Открытие задачи по клику
    document.querySelectorAll('.open-button').forEach(btn => {
      btn.addEventListener('click', () => {
        const taskId = btn.dataset.taskId;
        // Перенаправление на страницу просмотра конкретной задачи
        window.location.href = `/tasks/${taskId}`;
      });
    });
  
    // Бургер-меню для мобильных
    const burger = document.getElementById('burger');
    const nav = document.querySelector('.nav');
    const auth = document.querySelector('.auth-buttons');
    burger.addEventListener('click', () => {
      nav.classList.toggle('visible');
      auth.classList.toggle('visible');
    });
  });
  