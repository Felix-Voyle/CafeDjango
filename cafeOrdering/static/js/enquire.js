document.addEventListener("DOMContentLoaded", function() {
    var slides1 = document.querySelectorAll('.slides1 .coffee');
    var slides2 = document.querySelectorAll('.slides2 .event');
    var slides3 = document.querySelectorAll('.slides3 .food');
    var index1 = 0;
    var index2 = 0;
    var index3 = 0;

    function changeSlide1() {
        slides1[index1].classList.remove('d-block');
        slides1[index1].classList.add('d-none');
        index1 = (index1 + 1) % slides1.length;
        slides1[index1].classList.remove('d-none');
        slides1[index1].classList.add('d-block');
        slides1[index1].style.opacity = 0; 
        setTimeout(function() {
            slides1[index1].style.opacity = 1; 
        }, 50); 
    }

    function changeSlide2() {
        slides2[index2].classList.remove('d-block');
        slides2[index2].classList.add('d-none');
        index2 = (index2 + 1) % slides2.length;
        slides2[index2].classList.remove('d-none');
        slides2[index2].classList.add('d-block');
        slides2[index2].style.opacity = 0; 
        setTimeout(function() {
            slides2[index2].style.opacity = 1; 
        }, 50); 
    }

    function changeSlide3() {
        slides3[index3].classList.remove('d-block');
        slides3[index3].classList.add('d-none');
        index3 = (index3 + 1) % slides3.length;
        slides3[index3].classList.remove('d-none');
        slides3[index3].classList.add('d-block');
        slides3[index3].style.opacity = 0; 
        setTimeout(function() {
            slides3[index3].style.opacity = 1; 
        }, 50); 
    }

    setInterval(function() {
        changeSlide1();
        setTimeout(changeSlide2, 2000); 
        setTimeout(changeSlide3, 4000); 
    }, 6000); 

    changeSlide1();
        setTimeout(changeSlide2, 2000); 
        setTimeout(changeSlide3, 4000);
    
});