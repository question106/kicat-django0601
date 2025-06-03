// Moved from base.html inline <script> (Tailwind config)
window.tailwind = window.tailwind || {};
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: 'rgb(113 6 0)', // Red color from design1-5-sharp.html
                primaryDark: '#af0a00', // Darker version of primary
                secondary: '#d09101', // Black from design1-5-sharp.html
                secondaryDark: '#af0a00', // Darker version of secondary
                accent: '#71060026', // Keeping the bright accent color
                accentDark: '#b9e005', // Darker version of accent
                muted: '#F0F4F9', // Light background
                mutedForeground: '#64748B', // Text color for descriptions
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
            borderRadius: {
                'none': '0',
                'sm': '0px',
                DEFAULT: '0px',
                'md': '0px',
                'lg': '0px',
                'xl': '0px',
                'full': '0px',
            },
        },
    },
};

$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});



// Lucide Icon initialization

// Global function to close the quote modal
function closeQuoteModal() {
    const quoteRequestModal = document.getElementById('quoteRequestModal');
    if (quoteRequestModal) {
        quoteRequestModal.classList.remove('fade-in');
        quoteRequestModal.classList.add('fade-out');
        document.body.classList.remove('overflow-hidden');
        
        setTimeout(() => {
            quoteRequestModal.classList.add('hidden');
            quoteRequestModal.classList.remove('fade-out');
        }, 300);
    }
}

document.addEventListener('DOMContentLoaded', function() {
// Lucide icon initialization
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}

// Mobile menu functionality
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const closeMobileMenu = document.getElementById('close-mobile-menu');

// Language switcher functionality - with mobile support
const languageDropdownButton = document.getElementById('language-dropdown-button');
const languageDropdown = document.getElementById('language-dropdown');

if (languageDropdownButton) {
    languageDropdownButton.addEventListener('click', function(e) {
    e.preventDefault();
    
    // Check if the screen is mobile sized (less than 768px)
    if (window.innerWidth < 768) {
        // On mobile, show the mobile menu instead
        if (mobileMenu) {
        mobileMenu.classList.add('show');
        document.body.classList.add('overflow-hidden');
        }
    } else {
        // On desktop, toggle language dropdown
        if (languageDropdown) {
        languageDropdown.classList.toggle('show');
        }
    }
    });
}

// Close language dropdown when clicking outside
document.addEventListener('click', function(e) {
    if (languageDropdown && languageDropdownButton) {
    if (!languageDropdownButton.contains(e.target) && !languageDropdown.contains(e.target)) {
        languageDropdown.classList.remove('show');
    }
    }
});

// Handle language option selection
const languageOptions = document.querySelectorAll('.language-option');
if (languageOptions.length > 0) {
    languageOptions.forEach(option => {
    option.addEventListener('click', function(e) {
        e.preventDefault();
        const lang = this.getAttribute('data-lang');
        const currentLanguage = document.getElementById('current-language');
        if (currentLanguage) {
        currentLanguage.textContent = this.textContent;
        }
        
        // Here you would normally change the language of the site
        console.log('Language changed to:', lang);
        
        // Close the dropdown
        if (languageDropdown) {
        languageDropdown.classList.remove('show');
        }
    });
    });
}

// Toggle mobile menu when hamburger button is clicked
if (mobileMenuToggle && mobileMenu) {
    mobileMenuToggle.addEventListener('click', function() {
    mobileMenu.classList.add('show');
    document.body.classList.add('overflow-hidden'); // Prevent scrolling
    });
}

// Close mobile menu when the close button is clicked
if (closeMobileMenu && mobileMenu) {
    closeMobileMenu.addEventListener('click', function() {
    closeMenu();
    });
}

// Close mobile menu when clicking on the dark overlay (outside the menu)
if (mobileMenu) {
    mobileMenu.addEventListener('click', function(e) {
    if (e.target === mobileMenu) {
        closeMenu();
    }
    });
}

// Close mobile menu when a navigation link is clicked
if (mobileMenu) {
    const mobileNavLinks = mobileMenu.querySelectorAll('a[href^="#"]');
    mobileNavLinks.forEach(link => {
    link.addEventListener('click', function() {
        closeMenu();
    });
    });
}

// Function to close the mobile menu with animation
function closeMenu() {
    mobileMenu.classList.remove('show');
    // Only remove overflow-hidden after animation completes
    setTimeout(() => {
    document.body.classList.remove('overflow-hidden');
    }, 400); // Match this with the animation duration
}

// Service tabs functionality
const tabTriggers = document.querySelectorAll('.tab-trigger');

tabTriggers.forEach(trigger => {
    trigger.addEventListener('click', function() {
    // Deactivate all tabs
    tabTriggers.forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    // Activate the clicked tab
    this.classList.add('active');
    const tabId = trigger.getAttribute('data-tab');
    document.getElementById(tabId + '-tab').classList.add('active');
    });
});

// Language tabs functionality
const languageTabTriggers = document.querySelectorAll('.language-tab-trigger');

languageTabTriggers.forEach(trigger => {
    trigger.addEventListener('click', function() {
    // Deactivate all language tabs
    languageTabTriggers.forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.language-tab-content').forEach(content => content.classList.remove('active'));
    
    // Activate the clicked language tab
    this.classList.add('active');
    const tabId = trigger.getAttribute('data-tab');
    document.getElementById(tabId + '-tab').classList.add('active');
    });
    });

// Accordion functionality
const accordionTriggers = document.querySelectorAll('.accordion-trigger');

accordionTriggers.forEach(trigger => {
    trigger.addEventListener('click', function() {
    // Toggle chevron icon
    const chevron = this.querySelector('.chevron');
    chevron.style.transform = chevron.style.transform === 'rotate(180deg)' ? 'rotate(0deg)' : 'rotate(180deg)';
    
    // Toggle content visibility
    const content = this.nextElementSibling;
    content.style.display = content.style.display === 'block' ? 'none' : 'block';
    });
});

// Mobile bottom menu functionality
const mobileMenuItems = document.querySelectorAll('.mobile-bottom-menu .menu-item');
const regularMenuItems = Array.from(mobileMenuItems).filter(item => !item.classList.contains('quote-request-link'));

// Remove default active state from all menu items
mobileMenuItems.forEach(item => {
    if (!item.classList.contains('quote-request-link')) {
    item.classList.remove('active');
    }
});

// Add click event listeners to regular menu items
regularMenuItems.forEach(item => {
    item.addEventListener('click', function() {
    if (!this.classList.contains('quote-request-link')) {
        // Remove active class from all menu items
        mobileMenuItems.forEach(menuItem => menuItem.classList.remove('active'));
        // Add active class to the clicked menu item
        this.classList.add('active');
    }
    });
});

// Handle quote request button in mobile menu and other places
// Select all quote request buttons and links
const quoteRequestBtns = document.querySelectorAll('.quote-request-btn, .quote-request-link');
const quoteRequestModal = document.getElementById('quoteRequestModal');
const closeQuoteModalBtn = document.getElementById('closeQuoteModal');

// Function to open the quote modal
function openQuoteModal(e) {
    e.preventDefault();
    if (quoteRequestModal) {
        // Reset the service type dropdown
        $('#service_type').html('<option value="">먼저 서비스 카테고리를 선택하세요</option>');
        
        // Show the modal
        quoteRequestModal.classList.remove('hidden');
        quoteRequestModal.classList.add('fade-in');
        document.body.classList.add('overflow-hidden');
    }
}

// Add click event listeners to all quote request buttons and links
if (quoteRequestBtns.length > 0) {
    quoteRequestBtns.forEach(btn => {
    btn.addEventListener('click', openQuoteModal);
    });
}

// Add click event listener to close button
if (closeQuoteModalBtn) {
    closeQuoteModalBtn.addEventListener('click', closeQuoteModal);
}

// Close modal when clicking outside the modal content
if (quoteRequestModal) {
quoteRequestModal.addEventListener('click', function(e) {
    if (e.target === quoteRequestModal) {
    closeQuoteModal();
    }
});
}

// Close modal when pressing Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && quoteRequestModal && !quoteRequestModal.classList.contains('hidden')) {
    closeQuoteModal();
    }
});

// Partners Modal functionality
const partnersModalBtn = document.getElementById('partnersModalBtn');
const partnersModal = document.getElementById('partnersModal');
const closePartnersModal = document.getElementById('closePartnersModal');

// Function to open the partners modal
function openPartnersModal(e) {
    e.preventDefault();
    if (partnersModal) {
    partnersModal.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
    }
}

// Function to close the partners modal
function closePartnersModalFunc() {
    if (partnersModal) {
    partnersModal.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
    }
}

// Add click event listener to partners modal button
if (partnersModalBtn) {
    partnersModalBtn.addEventListener('click', openPartnersModal);
}

// Add click event listener to close button
if (closePartnersModal) {
    closePartnersModal.addEventListener('click', closePartnersModalFunc);
}

// Close modal when clicking outside the modal content
if (partnersModal) {
    partnersModal.addEventListener('click', function(e) {
    if (e.target === partnersModal) {
        closePartnersModalFunc();
    }
    });
}

// Close modal when pressing Escape key (update existing handler)
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
    if (quoteRequestModal && !quoteRequestModal.classList.contains('hidden')) {
        closeQuoteModal();
    }
    if (partnersModal && !partnersModal.classList.contains('hidden')) {
        closePartnersModalFunc();
    }
    }
});

// Track active menu items based on scroll position
const sections = {
    services: document.getElementById('services'),
    languages: document.getElementById('languages'),
    pricing: document.getElementById('pricing'),
    'case-studies': document.getElementById('case-studies'), 
    faq: document.getElementById('faq'),
    contact: document.getElementById('contact')
};

window.addEventListener('scroll', function() {
    // Get the current scroll position (add some offset to avoid triggering right at the top)
    const scrollPosition = window.scrollY + 100; // Small offset for better detection
    
    // First remove active class from all menu items
    mobileMenuItems.forEach(item => {
    if (!item.classList.contains('quote-request-link')) {
        item.classList.remove('active');
    }
    });
    
    // Find which section is currently in view
    let foundActiveSection = false;
    for (const [id, section] of Object.entries(sections)) {
    if (section) {
        const sectionTop = section.offsetTop;
        const sectionBottom = sectionTop + section.offsetHeight;
        
        // Check if we're currently in this section
        if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
        foundActiveSection = true;
        
        // Update active menu item for this section
        mobileMenuItems.forEach(item => {
            const href = item.getAttribute('href');
            if (href === `#${id}`) {
            item.classList.add('active');
            }
        });
        break;
        }
    }
    }
    
    // If no section is active, ensure all menu items are inactive
    if (!foundActiveSection) {
    mobileMenuItems.forEach(item => {
        if (!item.classList.contains('quote-request-link')) {
        item.classList.remove('active');
    }
    });
}
});

// Add resize event listener to handle screen size changes
window.addEventListener('resize', function() {
    // If window is resized to desktop size and mobile menu is open, close it
    if (window.innerWidth >= 768 && mobileMenu && mobileMenu.classList.contains('show')) {
    closeMenu();
    }
    
    // If window is resized to mobile and language dropdown is open, close it
    if (window.innerWidth < 768 && languageDropdown && languageDropdown.classList.contains('show')) {
    languageDropdown.classList.remove('show');
    }
});

// Trigger scroll handler on page load to set initial active state
window.dispatchEvent(new Event('scroll'));
});


// 견적서 요청 모달 통역, 번역, 기타 서비스 탭 버튼 클릭 시 탭 내용 변경
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active', 'bg-primary', 'text-white', 'border-primary', 'font-medium', 'shadow-sm'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button
            button.classList.add('active', 'bg-primary', 'text-white', 'border-primary', 'font-medium', 'shadow-sm');

            // Show corresponding content
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
});

// Modal functionality for carousel images
document.addEventListener('DOMContentLoaded', function() {
// ... existing image modal code ...
});

// Custom scrolling with padding adjustment
document.addEventListener('DOMContentLoaded', function() {
// Function to scroll to element with offset
function scrollToElement(elementId, offset = 30) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;
    
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
        }

// Update the service button click handler
const serviceButtons = document.querySelectorAll('button[onclick*="#services"]');
serviceButtons.forEach(button => {
    button.setAttribute('onclick', '');
    button.addEventListener('click', function() {
    scrollToElement('services');
    });
});

// Update menu items with hash links
document.querySelectorAll('.menu-item[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href').substring(1);
    scrollToElement(targetId);
    });
});
});

 // Section fade-in animation
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in-section class to all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        if (!section.classList.contains('fade-in-section')) {
        section.classList.add('fade-in-section');
        }
    });
    
    // Function to check if element is in viewport
    function checkIfInView() {
        const sections = document.querySelectorAll('.fade-in-section');
        sections.forEach(section => {
        // Get section's position relative to the viewport
        const rect = section.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        
        // Check if section is in view (partial visibility is enough)
        const isInView = (
            rect.top <= windowHeight * 0.75 && // Section has entered 75% from the top
            rect.bottom >= 0 // Bottom of section is not above the viewport
        );
        
        if (isInView) {
            section.classList.add('is-visible');
        }
        });
    }
    
    // Run on initial load
    checkIfInView();
    
    // Run on scroll
    window.addEventListener('scroll', checkIfInView, { passive: true });
    
    // Run on resize
    window.addEventListener('resize', checkIfInView, { passive: true });
});


// jQuery modal
$(document).on('click', '#js-quote-request-btn', function(e) {
    e.preventDefault();
    const submitBtn = $('#js-quote-request-btn');
    const name = $('#name');
    const company = $('#company');
    const email = $('#email');
    const phone = $('#phone');
    const service_type = $('#service_type');
    const message = $('#message');
    
    // Basic validation
    if(!name.val() || !company.val() || !email.val() || !phone.val() || !service_type.val() || !message.val()) {
        alert("모든 필수 항목을 입력해주세요.");
        return false;
    }
    
    // Create form data for submission (for file upload support)
    const formData = new FormData($('#quoteRequestForm')[0]);
    
    // Disable button and show loading state
    submitBtn.prop("disabled", true).text("제출 중...");
    
    $.ajax({
        type: 'POST',
        url: $('#quoteRequestModal').attr('data-url'),  // Get URL from data attribute
        data: formData,
        processData: false,  // Important for FormData
        contentType: false,  // Important for FormData
        success: function(response) {
            if(response.status === "success") {
                // Close modal using the global function
                closeQuoteModal();
                
                // Reset form
                $('#quoteRequestForm')[0].reset();
                $('#service_type').html('<option value="">먼저 서비스 카테고리를 선택하세요</option>');
                
                // Show success message
                alert("견적 요청이 성공적으로 접수되었습니다.");
            }
            submitBtn.prop("disabled", false).text("견적 요청하기");
        },
        error: function(error) {
            console.warn(error);
            alert("오류가 발생했습니다. 다시 시도해 주세요.");
            submitBtn.prop("disabled", false).text("견적 요청하기");
        }
    });
});

// Handle Service Category Change to populate Service Types
$(document).on('change', '#service_category', function() {
    const categoryId = $(this).val();
    const serviceTypeSelect = $('#service_type');
    
    // Reset the service type dropdown
    serviceTypeSelect.html('<option value="">먼저 서비스 카테고리를 선택하세요</option>');
    
    if (categoryId) {
        // Disable the dropdown while loading
        serviceTypeSelect.prop('disabled', true);
        
        // Get service types for this category via AJAX
        $.ajax({
            url: '/quotes/get_service_types/',
            data: { 'category_id': categoryId },
            success: function(data) {
                // Enable the dropdown
                serviceTypeSelect.prop('disabled', false);
                
                // If we have service types, populate the dropdown
                if (data.service_types && data.service_types.length > 0) {
                    $.each(data.service_types, function(i, type) {
                        serviceTypeSelect.append($('<option>', {
                            value: type.id,
                            text: type.name
                        }));
                    });
                } else {
                    serviceTypeSelect.html('<option value="">이 카테고리에는 세부 유형이 없습니다</option>');
                }
            },
            error: function() {
                serviceTypeSelect.prop('disabled', false);
                serviceTypeSelect.html('<option value="">서비스 유형을 불러오는데 실패했습니다</option>');
            }
        });
    }
});