/**
 * FILTEC Polyplast - Shared Website Interactions
 * Mobile drawer, inquiry modals, product filters, and FAQs
 */

document.addEventListener('DOMContentLoaded', () => {
    initDrawer();
    initModals();
    initFaqs();
    initForms();
    initScrollReveal();
});

/**
 * Mobile Navigation Drawer
 */
function initDrawer() {
    const menuToggle = document.getElementById('menuToggle');
    const drawer = document.getElementById('drawer');
    const drawerBackdrop = document.getElementById('drawerBackdrop');
    const drawerClose = document.getElementById('drawerClose');

    if (!menuToggle || !drawer) return;

    const toggleDrawer = (open) => {
        if (open) {
            drawer.classList.add('open');
            document.body.style.overflow = 'hidden';
        } else {
            drawer.classList.remove('open');
            document.body.style.overflow = '';
        }
    };

    menuToggle.addEventListener('click', () => toggleDrawer(true));
    drawerClose.addEventListener('click', () => toggleDrawer(false));
    drawerBackdrop.addEventListener('click', () => toggleDrawer(false));

    // Close drawer when clicking a link
    const drawerLinks = drawer.querySelectorAll('.drawer-link');
    drawerLinks.forEach(link => {
        link.addEventListener('click', () => toggleDrawer(false));
    });
}

/**
 * Inquiry & Contact Modals
 */
let currentModal = null;

function initModals() {
    const modal = document.getElementById('inquiryModal');
    if (!modal) return;

    const closeBtn = modal.querySelector('.modal-close');
    const backdrop = modal.querySelector('.modal-backdrop');

    const closeModal = () => {
        modal.classList.remove('open');
        document.body.style.overflow = '';
        currentModal = null;
    };

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    // Global listeners for elements triggering inquiry modals
    window.openInquiryModal = (productName = '') => {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
        currentModal = modal;

        // Pre-fill the product interest field if present
        const interestField = document.getElementById('productInterest');
        if (interestField && productName) {
            interestField.value = productName;
        }
    };

    window.closeInquiryModal = closeModal;
}

/**
 * FAQ Accordion
 */
function initFaqs() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const item = question.closest('.faq-item');
            const isActive = item.classList.contains('active');
            
            // Close all items
            document.querySelectorAll('.faq-item').forEach(el => {
                el.classList.remove('active');
                const ans = el.querySelector('.faq-answer');
                if (ans) ans.style.maxHeight = null;
            });
            
            // Toggle active item
            if (!isActive) {
                item.classList.add('active');
                const answer = item.querySelector('.faq-answer');
                if (answer) {
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                }
            }
        });
    });
}

/**
 * Tab-based Product Filtering
 */
window.filterProducts = (category, btnElement) => {
    const productCards = document.querySelectorAll('.card-product');
    const tabButtons = document.querySelectorAll('.tab-btn');

    // Update active button styling
    if (btnElement) {
        tabButtons.forEach(btn => btn.classList.remove('active'));
        btnElement.classList.add('active');
    }

    productCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        if (category === 'all' || cardCategory === category) {
            card.style.display = 'flex';
            // Subtle fade-in animation
            card.style.opacity = '0';
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transition = 'opacity 0.3s ease';
            }, 50);
        } else {
            card.style.display = 'none';
        }
    });
};

/**
 * Form submissions with user feedback
 */
function initForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Display alert of successful submission
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn ? submitBtn.innerHTML : 'Submit';
            
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = 'Sending Inquiry...';
            }
            
            // Simulate API request
            setTimeout(() => {
                if (submitBtn) {
                    submitBtn.innerHTML = 'Success!';
                    submitBtn.style.backgroundColor = '#2e7d32'; // Green
                }
                
                alert('Thank you! Your B2B inquiry has been sent successfully. Our team will contact you within 24 hours.');
                
                setTimeout(() => {
                    form.reset();
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalText;
                        submitBtn.style.backgroundColor = ''; // Reset to CSS
                    }
                    if (currentModal) {
                        window.closeInquiryModal();
                    }
                }, 1000);
            }, 1200);
        });
    });
}

// Fade out preloader on load
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        preloader.classList.add('fade-out');
    }
});

/**
 * Custom Scroll Reveal Animation using Intersection Observer
 */
function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal');
    if (reveals.length === 0) return;

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -20px 0px'
    });

    reveals.forEach(el => revealObserver.observe(el));
}
