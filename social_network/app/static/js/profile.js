function updateProfile(event) {
    event.preventDefault();
    
    const formData = new FormData(document.getElementById('profileForm'));
    
    fetch('/update_profile', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Профиль успешно обновлен');
            setTimeout(() => location.reload(), 1500);
        } else {
            showNotification('Ошибка при обновлении профиля', 'error');
        }
    })
    .catch(() => {
        showNotification('Произошла ошибка', 'error');
    });
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 3000);
}
