// Дождемся полной загрузки DOM перед выполнением скриптов
document.addEventListener('DOMContentLoaded', function() {
  // Бургер-меню
  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  const authButtons = document.querySelector('.auth-buttons');
  
  if (burger && nav) {
    burger.addEventListener('click', function() {
      nav.classList.toggle('nav-active');
      if (authButtons) {
        authButtons.classList.toggle('auth-active');
      }
      burger.classList.toggle('burger-active');
      document.body.classList.toggle('no-scroll');
    });
  }

  // Плавный скролл
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href !== "#" && document.querySelector(href)) {
        e.preventDefault();
        document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
        
        // Закрываем мобильное меню при клике на ссылку
        if (nav && nav.classList.contains('nav-active')) {
          nav.classList.remove('nav-active');
          if (authButtons) {
            authButtons.classList.remove('auth-active');
          }
          if (burger) {
            burger.classList.remove('burger-active');
          }
          document.body.classList.remove('no-scroll');
        }
      }
    });
  });

  // Анимация при скролле
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('appear');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.feature-card, .step, .timeline-item').forEach(el => {
    if (el) observer.observe(el);
  });

  // FAQ Accordion
  const faqItems = document.querySelectorAll('.faq-item');
  
  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    
    if (question) {
      question.addEventListener('click', () => {
        // Close all other items
        faqItems.forEach(otherItem => {
          if (otherItem !== item && otherItem.classList.contains('active')) {
            otherItem.classList.remove('active');
          }
        });
        
        // Toggle current item
        item.classList.toggle('active');
      });
    }
  });
  
  // Close FAQ when clicking outside
  document.addEventListener('click', function(event) {
    if (!event.target.closest('.faq-question') && !event.target.closest('.faq-answer')) {
      faqItems.forEach(item => {
        item.classList.remove('active');
      });
    }
  });
});