document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('supportForm');
    form.addEventListener('submit', e => {
      e.preventDefault();
      const name    = form.name.value.trim();
      const email   = form.email.value.trim();
      const message = form.message.value.trim();
      if (!name || !email || !message) return;
  
      const mailto = 
        `mailto:studysphereru@gmail.com` +
        `?subject=${encodeURIComponent('Поддержка StudySphere - ' + name)}` +
        `&body=${encodeURIComponent(`От: ${name}\nEmail: ${email}\n\n${message}`)}`;
  
      window.location.href = mailto;
    });
  });
  