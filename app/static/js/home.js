/**
 * Home Page JavaScript - Hero Slider & Testimonials Track Controls
 */

document.addEventListener('DOMContentLoaded', function() {
    initHeroSlider();
    initTestimonialSlider();
});

/**
 * Custom Hero Slideshow Slider
 */
function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slider-slide');
    const dots = document.querySelectorAll('.hero-slider-dot');
    const prevBtn = document.querySelector('.hero-slider-arrow-prev');
    const nextBtn = document.querySelector('.hero-slider-arrow-next');
    
    if (slides.length === 0) return;
    
    let currentIndex = 0;
    const intervalTime = 6000; // 6 seconds
    let slideInterval;
    
    function changeSlide(index) {
        // Handle out of bounds
        if (index >= slides.length) index = 0;
        if (index < 0) index = slides.length - 1;
        
        // Remove active from all
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        // Add active to targeted
        slides[index].classList.add('active');
        if (dots[index]) dots[index].classList.add('active');
        
        currentIndex = index;
    }
    
    function nextSlide() {
        changeSlide(currentIndex + 1);
    }
    
    function prevSlide() {
        changeSlide(currentIndex - 1);
    }
    
    function startTimer() {
        clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, intervalTime);
    }
    
    // Wire up events
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            nextSlide();
            startTimer(); // reset auto advance timer
        });
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            prevSlide();
            startTimer(); // reset auto advance timer
        });
    }
    
    dots.forEach((dot, idx) => {
        dot.addEventListener('click', function() {
            changeSlide(idx);
            startTimer(); // reset auto advance timer
        });
    });
    
    // Start slider
    changeSlide(0);
    startTimer();
}

/**
 * Testimonials Scroll-Snap Slider Controls
 */
function initTestimonialSlider() {
    const prevBtn = document.querySelector('.testimonials-controls .testimonial-ctrl-btn:first-child');
    const nextBtn = document.querySelector('.testimonials-controls .testimonial-ctrl-btn:last-child');
    const track = document.querySelector('.testimonials-track');
    
    if (!track || !prevBtn || !nextBtn) return;
    
    nextBtn.addEventListener('click', function() {
        const slideWidth = track.querySelector('.testimonials-slide-wrapper').offsetWidth;
        track.scrollBy({
            left: slideWidth + 32, // slide width + grid gap
            behavior: 'smooth'
        });
    });
    
    prevBtn.addEventListener('click', function() {
        const slideWidth = track.querySelector('.testimonials-slide-wrapper').offsetWidth;
        track.scrollBy({
            left: -(slideWidth + 32),
            behavior: 'smooth'
        });
    });
}
