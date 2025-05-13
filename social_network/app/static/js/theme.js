// document.addEventListener('DOMContentLoaded', function() {
//     const themeToggle = document.getElementById('theme-toggle');
//     const body = document.body;
    
//     if (localStorage.getItem('theme') === 'dark') {
//         body.classList.add('dark-theme');
//     }
    
//     if (themeToggle) {
//         themeToggle.textContent = localStorage.getItem('theme') === 'dark' ? '☀️' : '🌙';
        
//         themeToggle.addEventListener('click', function() {
//             body.classList.toggle('dark-theme');
//             localStorage.setItem('theme', body.classList.contains('dark-theme') ? 'dark' : 'light');
//             themeToggle.textContent = body.classList.contains('dark-theme') ? '☀️' : '🌙';
//         });
//     }
// });
