document.addEventListener('DOMContentLoaded', () => {
    // Для каждого блока вопроса назначаем обработчик
    document.querySelectorAll('.answer-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const block = btn.closest('.question-block');
        const qid   = parseInt(block.dataset.id, 10);
        const input = block.querySelector('.q-answer');
        const answer = input.value.trim();
        const feedback = block.querySelector('.feedback');
  
        // ничего не делаем, если нет ответа
        if (!answer) return;
  
        fetch('/quizzes/answer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: qid, answer })
        })
        .then(res => res.json())
        .then(data => {
          if (data.correct) {
            feedback.className = 'feedback correct';
            feedback.textContent = `✔ Правильно! ${data.explanation || ''}`;
          } else {
            feedback.className = 'feedback wrong';
            feedback.textContent = `✖ Неправильно. Правильный ответ: ${data.correct_answer}. ${data.explanation || ''}`;
          }
          // Заблокировать поле после ответа
          input.disabled = true;
          btn.disabled = true;
        })
        .catch(() => {
          feedback.className = 'feedback wrong';
          feedback.textContent = 'Ошибка соединения с сервером';
        });
      });
    });
  });
  