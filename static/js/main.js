/**
 * FILTEC Polyplast — Shared Website Interactions
 * Mobile drawer, inquiry modals, product filters, FAQs
 * All forms → WhatsApp first
 */

// ─────────────────────────────────────────────
// WhatsApp business number (without + or spaces)
// ─────────────────────────────────────────────
const WA_NUMBER = '919437505814';

/** Open WhatsApp with a pre-filled message */
function sendToWhatsApp(message) {
    const url = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
}

/** Helper: get value from element, fallback to '' */
function val(id) {
    const el = document.getElementById(id);
    if (!el) return '';
    if (el.tagName === 'SELECT') {
        return el.options[el.selectedIndex]?.text || '';
    }
    return el.value.trim();
}

// ─────────────────────────────────────────────
// DOM Ready
// ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initDrawer();
    initModals();
    initFaqs();
    initForms();
    initScrollReveal();
});

// ─────────────────────────────────────────────
// Premium Mobile Navigation Drawer
// ─────────────────────────────────────────────
function initDrawer() {
    const menuToggle   = document.getElementById('menuToggle');
    const drawer       = document.getElementById('drawer');
    const drawerBackdrop = document.getElementById('drawerBackdrop');
    const drawerClose  = document.getElementById('drawerClose');

    if (!menuToggle || !drawer) return;

    const toggleDrawer = (open) => {
        if (open) {
            drawer.classList.add('open');
            menuToggle.classList.add('is-active');
            document.body.style.overflow = 'hidden';
        } else {
            drawer.classList.remove('open');
            menuToggle.classList.remove('is-active');
            document.body.style.overflow = '';
        }
    };

    menuToggle.addEventListener('click', () => toggleDrawer(true));
    if (drawerClose)   drawerClose.addEventListener('click',   () => toggleDrawer(false));
    if (drawerBackdrop) drawerBackdrop.addEventListener('click', () => toggleDrawer(false));

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && drawer.classList.contains('open')) toggleDrawer(false);
    });

    // Close on any nav link click
    drawer.querySelectorAll('.drawer-link').forEach(link => {
        link.addEventListener('click', () => toggleDrawer(false));
    });
}

// ─────────────────────────────────────────────
// Product Inquiry Modal
// ─────────────────────────────────────────────
let currentModal = null;

function initModals() {
    const modal = document.getElementById('inquiryModal');
    if (!modal) return;

    const closeBtn  = modal.querySelector('.modal-close');
    const backdrop  = modal.querySelector('.modal-backdrop');

    const closeModal = () => {
        modal.classList.remove('open');
        document.body.style.overflow = '';
        currentModal = null;
    };

    if (closeBtn)  closeBtn.addEventListener('click',  closeModal);
    if (backdrop)  backdrop.addEventListener('click',  closeModal);

    // Expose globally so inline onclick can call it
    window.openInquiryModal = (productName = '') => {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
        currentModal = modal;
        const interestField = document.getElementById('productInterest');
        if (interestField && productName) interestField.value = productName;
    };

    window.closeInquiryModal = closeModal;
}

// ─────────────────────────────────────────────
// FAQ Accordion
// ─────────────────────────────────────────────
function initFaqs() {
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', () => {
            const item     = question.closest('.faq-item');
            const isActive = item.classList.contains('active');

            // Close all
            document.querySelectorAll('.faq-item').forEach(el => {
                el.classList.remove('active');
                const ans = el.querySelector('.faq-answer');
                if (ans) ans.style.maxHeight = null;
            });

            // Open clicked if it wasn't active
            if (!isActive) {
                item.classList.add('active');
                const answer = item.querySelector('.faq-answer');
                if (answer) answer.style.maxHeight = answer.scrollHeight + 'px';
            }
        });
    });
}

// ─────────────────────────────────────────────
// Tab-based Product Filtering
// ─────────────────────────────────────────────
window.filterProducts = (category, btnElement) => {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    document.querySelectorAll('.card-product').forEach(card => {
        const match = category === 'all' || card.getAttribute('data-category') === category;
        if (match) {
            card.style.display  = 'flex';
            card.style.opacity  = '0';
            setTimeout(() => {
                card.style.opacity    = '1';
                card.style.transition = 'opacity 0.3s ease';
            }, 50);
        } else {
            card.style.display = 'none';
        }
    });
};

// ─────────────────────────────────────────────
// WhatsApp submit animation helper
// ─────────────────────────────────────────────
function animateSubmitBtn(btn, loadingText, doneCallback) {
    if (!btn) { doneCallback(); return; }
    const originalHTML = btn.innerHTML;
    btn.disabled  = true;
    btn.innerHTML = loadingText;

    setTimeout(() => {
        doneCallback();
        btn.innerHTML = `<span style="display:inline-flex;align-items:center;gap:8px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
            </svg>Sent via WhatsApp!</span>`;
        btn.style.background = 'linear-gradient(135deg,#25D366,#128C7E)';

        setTimeout(() => {
            btn.disabled         = false;
            btn.innerHTML        = originalHTML;
            btn.style.background = '';
        }, 2500);
    }, 700);
}

// ─────────────────────────────────────────────
// ① CONTACT PAGE FORM  (#contactPageForm)
// ─────────────────────────────────────────────
function handleContactForm(form) {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!form.checkValidity()) { form.reportValidity(); return; }

        const name     = val('contactName');
        const email    = val('contactEmail');
        const phone    = val('contactPhone');
        const company  = val('companyName');
        const inquiry  = val('inquiryType');
        const message  = val('contactMessage');

        const text =
`📩 *FILTEC — B2B INQUIRY*

👤 Name: ${name}
📱 Phone: ${phone}
📧 Email: ${email}
🏢 Company: ${company}
📋 Inquiry: ${inquiry}

💬 Message:
${message}`;

        const btn = form.querySelector('button[type="submit"]');
        animateSubmitBtn(btn, '⏳ Saving Lead...', () => {
            const formData = new FormData();
            formData.append('name', name);
            formData.append('email', email);
            formData.append('phone', phone);
            formData.append('message', `[Company: ${company}, Purpose: ${inquiry}] ${message}`);
            
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfToken) {
                formData.append('csrfmiddlewaretoken', csrfToken.value);
            }

            fetch('/contact/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                sendToWhatsApp(text);
                form.reset();
            })
            .catch(err => {
                console.error("Error saving lead:", err);
                sendToWhatsApp(text);
                form.reset();
            });
        });
    });
}

// ─────────────────────────────────────────────
// ② PRODUCT MODAL FORM  (#modalInquiryForm)
// ─────────────────────────────────────────────
function handleModalForm(form) {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!form.checkValidity()) { form.reportValidity(); return; }

        const name    = val('modalName');
        const email   = val('modalEmail');
        const phone   = val('modalPhone');
        const product = val('productInterest');
        const message = val('modalMessage');

        const text =
`🔧 *FILTEC — PRODUCT INQUIRY*

👤 Name: ${name}
📱 Phone: ${phone}
📧 Email: ${email}
📦 Product: ${product}

💬 Details:
${message}`;

        const btn = form.querySelector('button[type="submit"]');
        animateSubmitBtn(btn, '⏳ Saving Lead...', () => {
            const formData = new FormData();
            formData.append('name', name);
            formData.append('email', email);
            formData.append('phone', phone);
            formData.append('message', `[Product Interest: ${product}] ${message}`);

            // Find csrf token in index.html (it is in inquiryModal form)
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfToken) {
                formData.append('csrfmiddlewaretoken', csrfToken.value);
            }

            fetch('/contact/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                sendToWhatsApp(text);
                form.reset();
                if (window.closeInquiryModal) window.closeInquiryModal();
            })
            .catch(err => {
                console.error("Error saving lead:", err);
                sendToWhatsApp(text);
                form.reset();
                if (window.closeInquiryModal) window.closeInquiryModal();
            });
        });
    });
}

// ─────────────────────────────────────────────
// ③ PARTNER APPLICATION FORM  (#partnerApplicationForm)
// ─────────────────────────────────────────────
function handlePartnerForm(form) {
    if (form.dataset.waHandled) return;
    form.dataset.waHandled = 'true';

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!form.checkValidity()) { form.reportValidity(); return; }

        const name         = val('partnerFullName');
        const designation  = val('partnerDesignation');
        const phone        = val('partnerPhone');
        const email        = val('partnerEmail');
        const company      = val('partnerCompany');
        const city         = val('partnerCity');
        const state        = val('partnerState');
        const years        = val('partnerYearsOp');
        
        // Dynamically collect selected business types
        const bizTypesArray = [];
        form.querySelectorAll('input[name="businessType"]:checked').forEach(cb => {
            bizTypesArray.push(cb.value);
        });
        const bizType = bizTypesArray.join(', ') || 'Not Specified';

        // Dynamically collect selected product lines
        const productsArray = [];
        form.querySelectorAll('input[name="productLines"]:checked').forEach(cb => {
            productsArray.push(cb.value);
        });
        const products = productsArray.join(', ') || 'Not Specified';

        // Fallbacks for optional fields
        const territory    = val('partnerTerritory') || 'Not Specified';
        const volume       = val('partnerVolume') || 'Not Specified';
        const brands       = val('partnerCurrentBrands') || 'None';
        const warehouse    = val('partnerWarehouse') || 'No';
        const message      = val('partnerMessage') || 'No message provided';

        const text =
`🤝 *FILTEC PARTNER APPLICATION*

*Personal Info*
👤 Name: ${name}
💼 Role: ${designation}
📱 Phone: ${phone}
📧 Email: ${email}

*Business Info*
🏢 Company: ${company}
🏭 Type: ${bizType}
📍 Location: ${city}, ${state}
📅 Experience: ${years}

*Territory & Products*
🗺️ Territory: ${territory}
📦 Volume: ${volume}
🔧 Products: ${products}

*Additional*
🏷️ Current Brands: ${brands}
Store Warehouse: ${warehouse}

💬 Message:
${message}`;

        const btn = form.querySelector('button[type="submit"]');
        animateSubmitBtn(btn, '⏳ Saving Application...', () => {
            const formData = new FormData();
            formData.append('company_name', company);
            formData.append('contact_person', `${name} (${designation})`);
            formData.append('email', email);
            formData.append('phone', phone);
            formData.append('city', `${city}, ${state}`);
            formData.append('warehouse', warehouse.toLowerCase() === 'yes' ? 'yes' : 'no');
            formData.append('experience', `[BizType: ${bizType}, Years: ${years}, Territory: ${territory}, Volume: ${volume}, Products: ${products}, Brands: ${brands}]`);
            formData.append('message', message);

            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfToken) {
                formData.append('csrfmiddlewaretoken', csrfToken.value);
            }

            fetch('/partner/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                sendToWhatsApp(text);
                form.reset();
            })
            .catch(err => {
                console.error("Error saving application:", err);
                sendToWhatsApp(text);
                form.reset();
            });
        });
    });
}

// ─────────────────────────────────────────────
// Main form dispatcher — routes each form to its handler
// ─────────────────────────────────────────────
function initForms() {
    const contactForm = document.getElementById('contactPageForm');
    if (contactForm) handleContactForm(contactForm);

    const modalForm = document.getElementById('modalInquiryForm');
    if (modalForm) handleModalForm(modalForm);

    const partnerForm = document.getElementById('partnerApplicationForm');
    if (partnerForm) handlePartnerForm(partnerForm);
}

// ─────────────────────────────────────────────
// Preloader fade-out on page load
// ─────────────────────────────────────────────
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    if (preloader) preloader.classList.add('fade-out');
});

// ─────────────────────────────────────────────
// Scroll Reveal — Intersection Observer
// ─────────────────────────────────────────────
function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    if (!reveals.length) return;

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -20px 0px' });

    reveals.forEach(el => observer.observe(el));
}

// ─────────────────────────────────────────────
// Sticky Navbar Scroll Shadow
// ─────────────────────────────────────────────
(function initStickyNav() {
    const header = document.querySelector('header');
    if (!header) return;

    const onScroll = () => {
        if (window.scrollY > 10) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // Run on load in case page is already scrolled
})();
