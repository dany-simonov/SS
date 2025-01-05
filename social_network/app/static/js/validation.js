document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    // Функция создания и показа уведомления
    function showNotification(message, isSuccess) {
        const notification = document.createElement('div');
        notification.className = `notification ${isSuccess ? 'success' : 'error'}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            z-index: 1000;
            animation: slideIn 0.5s ease-out;
        `;
        notification.style.backgroundColor = isSuccess ? '#4CAF50' : '#f44336';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.5s ease-out';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        }, 3000);
    }

    // Функция создания праздничного поздравления
    function showCelebration() {
        const celebration = document.createElement('div');
        celebration.className = 'celebration';
        celebration.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            text-align: center;
            z-index: 1000;
            animation: popIn 0.5s ease-out;
        `;
        
        celebration.innerHTML = `
            <h2 style="color: #2196F3; margin-bottom: 20px;">🎉 Ура! Добро пожаловать! 🎉</h2>
            <p style="font-size: 18px; color: #333;">Регистрация прошла успешно!</p>
            <p style="font-size: 16px; color: #666;">Теперь вы часть нашего сообщества 🌟</p>
            <div style="margin-top: 20px;">
                <span style="font-size: 24px;">🎈 🎊 🎯 🎪</span>
            </div>
        `;
        
        document.body.appendChild(celebration);
        
        // Конфетти эффект
        for (let i = 0; i < 50; i++) {
            createConfetti();
        }
        
        setTimeout(() => {
            celebration.style.animation = 'fadeOut 0.5s ease-out';
            setTimeout(() => {
                document.body.removeChild(celebration);
                window.location.href = '/login';
            }, 500);
        }, 5000);
    }
    
    // Функция создания конфетти
    function createConfetti() {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 10px;
            height: 10px;
            background-color: ${['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'][Math.floor(Math.random() * 5)]};
            left: ${Math.random() * 100}vw;
            top: -10px;
            z-index: 999;
            animation: fall ${Math.random() * 3 + 2}s linear;
        `;
        document.body.appendChild(confetti);
        setTimeout(() => document.body.removeChild(confetti), 5000);
    }
    
    // Добавляем стили анимации
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }
        @keyframes slideOut {
            from { transform: translateX(0); }
            to { transform: translateX(100%); }
        }
        @keyframes popIn {
            0% { transform: translate(-50%, -50%) scale(0); }
            80% { transform: translate(-50%, -50%) scale(1.1); }
            100% { transform: translate(-50%, -50%) scale(1); }
        }
        @keyframes fadeOut {
            to { opacity: 0; }
        }
        @keyframes fall {
            to {
                transform: translateY(100vh) rotate(360deg);
            }
        }
    `;
    document.head.appendChild(style);
    
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = 'red';
                    showNotification('Пожалуйста, заполните все поля', false);
                } else {
                    // Проверка телефона
                    if (input.type === 'tel') {
                        const phoneRegex = /^8\d{10}$/;
                        if (!phoneRegex.test(input.value.replace(/\D/g, ''))) {
                            isValid = false;
                            input.style.borderColor = 'red';
                            showNotification('Неверный формат телефона. Должно быть 11 цифр, начиная с 8', false);
                        }
                    }
                    
                    // Проверка пароля
                    if (input.type === 'password') {
                        if (input.value.length < 4) {
                            isValid = false;
                            input.style.borderColor = 'red';
                            showNotification('Пароль должен быть длиннее 4 символов', false);
                        }
                    }
                    
                    if (isValid) {
                        input.style.borderColor = '#000000';
                    }
                }
            });

            if (isValid) {
                try {
                    const formData = new FormData(form);
                    const submitButton = form.querySelector('button[type="submit"]');
                    submitButton.disabled = true;

                    const response = await fetch(form.action, {
                        method: form.method,
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    const result = await response.json();

                    if (response.ok) {
                        if (form.id === 'registration-form') {
                            showCelebration();
                        } else if (form.id === 'login-form') {
                            if (result.success) {
                                window.location.href = '/profile';
                            } else {
                                showNotification(result.message || 'Неверные данные входа', false);
                            }
                        }
                    } else {
                        showNotification(result.message || 'Ошибка при обработке запроса', false);
                    }
                    submitButton.disabled = false;
                } catch (error) {
                    const submitButton = form.querySelector('button[type="submit"]');
                    submitButton.disabled = false;
                    showNotification('Ошибка соединения с сервером', false);
                    console.error('Ошибка:', error);
                }
            }

        });
        
        // Маска для телефона
        const phoneInputs = form.querySelectorAll('input[type="tel"]');
        phoneInputs.forEach(input => {
            input.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 0) {
                    value = '8' + value.substring(1);
                    if (value.length > 11) {
                        value = value.substring(0, 11);
                    }
                    let formattedValue = '';
                    for (let i = 0; i < value.length; i++) {
                        if (i === 1) formattedValue += ' ';
                        if (i === 4) formattedValue += ' ';
                        if (i === 7) formattedValue += ' ';
                        if (i === 9) formattedValue += ' ';
                        formattedValue += value[i];
                    }
                    e.target.value = formattedValue;
                }
            });
        });
    });
});
