document.addEventListener('DOMContentLoaded', function() {
    const messageElements = document.querySelectorAll('.message-card');

    messageElements.forEach(function(el) {
        setTimeout(function() {
            el.classList.add('fade-out');
            
            el.addEventListener('transitionend', function() {
                el.remove();
            });
        }, 4000); 
    });
});