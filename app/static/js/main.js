/**
 * Main JavaScript for Alnitak Constructions Website
 * Core interactions: Navbar, FAQ Accordion, Stats Counter, Projects Filtering, Brochure Modal
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize common interactions
    initMobileNav();
    initFaqAccordion();
    initStatsCounter();
    initProjectFilters();
    initBrochureModalCommon();
    initFlashMessagesDismiss();
});

/**
 * Mobile Navigation Menu drawer
 */
function initMobileNav() {
    const mobileToggle = document.querySelector('.mobile-nav-toggle');
    const navMenu = document.querySelector('.nav-menu-list');
    
    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navMenu.classList.toggle('active');
            
            // Toggle hamburger icon if needed
            const isActive = navMenu.classList.contains('active');
            mobileToggle.innerHTML = isActive ? '&#x2715;' : '&#x2630;'; // X vs Hamburger
        });
        
        // Close menu drawer when clicking outside
        document.addEventListener('click', function(e) {
            if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
                navMenu.classList.remove('active');
                mobileToggle.innerHTML = '&#x2630;';
            }
        });
        
        // Close menu drawer on link clicks
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                mobileToggle.innerHTML = '&#x2630;';
            });
        });
    }
}

/**
 * FAQ Accordion Panel Toggle
 */
function initFaqAccordion() {
    const headers = document.querySelectorAll('.faq-accordion-header');
    
    headers.forEach(header => {
        header.addEventListener('click', function() {
            const item = this.parentElement;
            const isOpen = item.classList.contains('active');
            
            // Close other items
            const allItems = document.querySelectorAll('.faq-accordion-item');
            allItems.forEach(i => {
                i.classList.remove('active');
                const toggle = i.querySelector('.faq-icon-toggle');
                if (toggle) toggle.textContent = '+';
            });
            
            // Toggle current item
            const currentToggle = this.querySelector('.faq-icon-toggle');
            if (!isOpen) {
                item.classList.add('active');
                if (currentToggle) currentToggle.textContent = '−';
            } else {
                item.classList.remove('active');
                if (currentToggle) currentToggle.textContent = '+';
            }
            
            // Update Lenis scroll layout to avoid layout shifts issues
            if (window.lenis) {
                window.lenis.resize();
            }
        });
    });
}

/**
 * Scroll triggered stats counter count-up animation
 */
function initStatsCounter() {
    const statsContainers = document.querySelectorAll('.stat-box-container');
    
    if (statsContainers.length === 0) return;
    
    const countUp = (element) => {
        const target = parseInt(element.getAttribute('data-count'), 10);
        if (isNaN(target)) return;
        
        let start = 0;
        const duration = 2000; // 2 seconds
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Ease out quad formula
            const easeProgress = progress * (2 - progress);
            const currentCount = Math.floor(easeProgress * target);
            
            element.textContent = currentCount + '+';
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.textContent = target + '+';
            }
        };
        
        requestAnimationFrame(animate);
    };
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    countUp(entry.target);
                    observer.unobserve(entry.target); // Animate once
                }
            });
        }, {
            threshold: 0.2
        });
        
        statsContainers.forEach(container => observer.observe(container));
    } else {
        // Fallback for older browsers
        statsContainers.forEach(container => {
            const target = container.getAttribute('data-count');
            container.textContent = target + '+';
        });
    }
}

/**
 * Client-side tab filters for Projects (Homepage and Portfolio)
 */
function initProjectFilters() {
    const tabButtons = document.querySelectorAll('.portfolio-tab-btn');
    const gridItems = document.querySelectorAll('.portfolio-masonry-item');
    
    if (tabButtons.length === 0 || gridItems.length === 0) return;
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active states from all tabs
            tabButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const category = this.getAttribute('data-filter');
            
            gridItems.forEach(item => {
                const itemCategory = item.getAttribute('data-category');
                
                if (category === 'all' || itemCategory === category) {
                    item.style.display = 'block';
                    // Trigger reflow for animations
                    item.style.opacity = '1';
                    item.style.transform = 'scale(1)';
                } else {
                    item.style.display = 'none';
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                }
            });
            
            // Update Lenis scroll boundaries
            if (window.lenis) {
                window.lenis.resize();
            }
        });
    });
}

/**
 * Brochure Modal handlers
 */
function initBrochureModalCommon() {
    window.openBrochureModal = function(e) {
        if (e) e.preventDefault();
        const modal = document.getElementById('brochureModal');
        if (modal) {
            modal.style.display = 'flex';
            setTimeout(() => {
                modal.style.opacity = '1';
                const content = modal.querySelector('.brochure-modal-content');
                if (content) content.style.transform = 'scale(1)';
            }, 10);
            
            // Stop scroll
            if (window.lenis) window.lenis.stop();
            document.body.style.overflow = 'hidden';
        }
    };
    
    window.closeBrochureModal = function() {
        const modal = document.getElementById('brochureModal');
        if (modal) {
            modal.style.opacity = '0';
            const content = modal.querySelector('.brochure-modal-content');
            if (content) content.style.transform = 'scale(0.9)';
            
            setTimeout(() => {
                modal.style.display = 'none';
            }, 300);
            
            // Restore scroll
            if (window.lenis) window.lenis.start();
            document.body.style.overflow = '';
        }
    };
    
    const modal = document.getElementById('brochureModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                window.closeBrochureModal();
            }
        });
    }
}

/**
 * Flash message alerts auto dismissal
 */
function initFlashMessagesDismiss() {
    const messages = document.querySelectorAll('.flash-message');
    messages.forEach(msg => {
        // Dismiss after 4 seconds
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 400);
        }, 4000);
        
        // Manual dismiss on click
        msg.addEventListener('click', function() {
            this.style.opacity = '0';
            setTimeout(() => this.remove(), 400);
        });
    });
}
