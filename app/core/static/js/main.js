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
function scrollToElement(elementId, offset = 80) {
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

// Update menu items with hash links (local page anchors)
document.querySelectorAll('.menu-item[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href').substring(1);
    scrollToElement(targetId);
    });
});

// Handle dropdown menu items with hash fragments
document.querySelectorAll('a[href*="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        const currentPath = window.location.pathname;
        
        // Check if this is a link to the current page with a hash
        if (href.includes(currentPath + '#') || href.startsWith('#')) {
            e.preventDefault();
            
            // Extract the hash part
            const hashIndex = href.indexOf('#');
            const targetId = href.substring(hashIndex + 1);
            
            if (targetId) {
                scrollToElement(targetId);
            }
        }
        // If it's a link to a different page with hash, let it navigate normally
        // The target page will handle the scroll offset when it loads
    });
});

// Handle hash in URL on page load (for direct links with hash)
if (window.location.hash) {
    // Wait a bit for the page to fully load
    setTimeout(() => {
        const targetId = window.location.hash.substring(1);
        scrollToElement(targetId);
    }, 500);
}
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
    const file = $('#file');
    
    // Basic validation
    if(!name.val() || !company.val() || !email.val() || !phone.val() || !service_type.val() || !message.val()) {
        alert("모든 필수 항목을 입력해주세요.");
        return false;
    }
    
    // File validation
    if(!file[0].files || file[0].files.length === 0) {
        alert("파일을 첨부해주세요.");
        return false;
    }
    
    // Create form data for submission (for file upload support)
    const formData = new FormData($('#quoteRequestForm')[0]);
    
    // Add CSRF token manually for FormData
    const csrfToken = $('[name=csrfmiddlewaretoken]').val();
    if (csrfToken) {
        formData.set('csrfmiddlewaretoken', csrfToken);
        console.log('CSRF token added:', csrfToken.substring(0, 10) + '...');
    } else {
        console.error('CSRF token not found!');
        alert('CSRF token not found. Please refresh the page and try again.');
        submitBtn.prop("disabled", false).text("견적 문의");
        return false;
    }
    
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

// File upload handling for quote request modal
$(document).ready(function() {
    $('#file').on('change', function() {
        const fileInput = this;
        const uploadArea = $('#file-upload-area');
        const placeholder = $('#upload-placeholder');
        const fileSelected = $('#file-selected');
        const fileName = $('#file-name');
        
        if (fileInput.files && fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const fileSize = (file.size / 1024 / 1024).toFixed(2); // Size in MB
            
            // Update UI to show selected file
            placeholder.addClass('hidden');
            fileSelected.removeClass('hidden');
            
            // Display file name with size
            fileName.text(`${file.name} (${fileSize}MB)`);
            
            // Change upload area styling to indicate file is selected
            uploadArea.removeClass('border-gray-300 bg-muted')
                     .addClass('border-primary bg-primary/5');
            
        } else {
            // Reset to original state if no file selected
            placeholder.removeClass('hidden');
            fileSelected.addClass('hidden');
            fileName.text('');
            
            // Reset upload area styling
            uploadArea.removeClass('border-primary bg-primary/5')
                     .addClass('border-gray-300 bg-muted');
        }
    });
    
    // Reset file upload UI when modal is closed
    $(document).on('click', '#closeQuoteModal', function() {
        // Reset file input and UI
        $('#file').val('');
        $('#upload-placeholder').removeClass('hidden');
        $('#file-selected').addClass('hidden');
        $('#file-name').text('');
        $('#file-upload-area').removeClass('border-primary bg-primary/5')
                              .addClass('border-gray-300 bg-muted');
    });
    
    // Also reset when form is successfully submitted
    const originalCloseQuoteModal = window.closeQuoteModal;
    window.closeQuoteModal = function() {
        // Reset file upload UI
        $('#file').val('');
        $('#upload-placeholder').removeClass('hidden');
        $('#file-selected').addClass('hidden');
        $('#file-name').text('');
        $('#file-upload-area').removeClass('border-primary bg-primary/5')
                              .addClass('border-gray-300 bg-muted');
        
        // Call original function
        if (originalCloseQuoteModal) {
            originalCloseQuoteModal();
        }
    };
});

// Awards Carousel functionality (for cases.html)
document.addEventListener('DOMContentLoaded', function() {
    const awardsCarousel = document.querySelector('.carousel-inner');
    const prevBtn = document.querySelector('.carousel-prev');
    const nextBtn = document.querySelector('.carousel-next');
    const indicators = document.querySelectorAll('.carousel-indicator');
    
    if (!awardsCarousel || !prevBtn || !nextBtn) return; // Exit if elements not found
    
    let currentIndex = 0;
    
    function getVisibleItems() {
        const allItems = document.querySelectorAll('.carousel-item');
        const visibleItems = [];
        
        allItems.forEach(item => {
            const computedStyle = window.getComputedStyle(item);
            if (computedStyle.display !== 'none') {
                visibleItems.push(item);
            }
        });
        
        return visibleItems;
    }
    
    function getTotalVisibleItems() {
        return getVisibleItems().length;
    }
    
    function updateCarousel() {
        const totalItems = getTotalVisibleItems();
        
        // Ensure currentIndex is within bounds
        if (currentIndex >= totalItems) {
            currentIndex = 0;
        } else if (currentIndex < 0) {
            currentIndex = totalItems - 1;
        }
        
        const translateValue = -currentIndex * 100 + '%';
        awardsCarousel.style.transform = `translateX(${translateValue})`;
        
        // Update indicators - only show indicators for visible items
        indicators.forEach((indicator, index) => {
            indicator.classList.remove('active', 'bg-primary');
            indicator.classList.add('bg-gray-300');
            
            // Hide indicators that don't correspond to visible items
            if (index < totalItems) {
                indicator.style.display = 'block';
            } else {
                indicator.style.display = 'none';
            }
        });
        
        // Set active indicator
        if (indicators[currentIndex]) {
            indicators[currentIndex].classList.remove('bg-gray-300');
            indicators[currentIndex].classList.add('active', 'bg-primary');
        }
    }
    
    // Previous button click
    prevBtn.addEventListener('click', () => {
        const totalItems = getTotalVisibleItems();
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel();
    });
    
    // Next button click
    nextBtn.addEventListener('click', () => {
        const totalItems = getTotalVisibleItems();
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    });
    
    // Indicator clicks
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            const totalItems = getTotalVisibleItems();
            if (index < totalItems) {
                currentIndex = index;
                updateCarousel();
            }
        });
    });
    
    // Touch events for swipe functionality
    let touchStartX = 0;
    let touchEndX = 0;
    
    awardsCarousel.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });
    
    awardsCarousel.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        if (touchEndX < touchStartX - swipeThreshold) {
            // Swipe left (next)
            nextBtn.click();
        } else if (touchEndX > touchStartX + swipeThreshold) {
            // Swipe right (previous)
            prevBtn.click();
        }
    }
    
    // Handle window resize to recalculate visible items
    window.addEventListener('resize', () => {
        // Reset to first slide on resize to avoid issues
        currentIndex = 0;
        updateCarousel();
    });
    
    // Initialize carousel
    updateCarousel();
});

// Awards Modal functionality
document.addEventListener('DOMContentLoaded', function() {
    const awardsModal = document.getElementById('awardsModal');
    const closeAwardsModalBtn = document.getElementById('closeAwardsModal');
    const awardModalImage = document.getElementById('awardModalImage');
    const awardModalTitle = document.getElementById('awardModalTitle');
    const awardModalDate = document.getElementById('awardModalDate');
    const awardModalLocation = document.getElementById('awardModalLocation');
    const awardModalDescription = document.getElementById('awardModalDescription');
    
    // Function to open awards modal
    function openAwardsModal(imageData) {
        if (awardsModal) {
            // Populate modal content
            awardModalImage.src = imageData.image;
            awardModalImage.alt = imageData.title;
            awardModalTitle.textContent = imageData.title;
            awardModalDate.textContent = imageData.date || imageData.description; // Fallback to description if no date
            awardModalLocation.textContent = imageData.location || ''; // Location if available
            awardModalDescription.textContent = imageData.description || '';
            
            // Show modal
            awardsModal.classList.remove('hidden');
            awardsModal.classList.add('animate-fade-in');
            document.body.classList.add('overflow-hidden');
            
            // Reinitialize Lucide icons for the modal
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }
    
    // Function to close awards modal
    function closeAwardsModal() {
        if (awardsModal) {
            awardsModal.classList.add('hidden');
            awardsModal.classList.remove('animate-fade-in');
            document.body.classList.remove('overflow-hidden');
        }
    }
    
    // Add click event listeners to all carousel image wrappers
    document.addEventListener('click', function(e) {
        const imageWrapper = e.target.closest('.carousel-image-wrapper');
        if (imageWrapper) {
            e.preventDefault();
            
            const imageData = {
                image: imageWrapper.dataset.image,
                title: imageWrapper.dataset.title,
                description: imageWrapper.dataset.description,
                date: imageWrapper.dataset.date,
                location: imageWrapper.dataset.location
            };
            
            openAwardsModal(imageData);
        }
    });
    
    // Close modal when close button is clicked
    if (closeAwardsModalBtn) {
        closeAwardsModalBtn.addEventListener('click', closeAwardsModal);
    }
    
    // Close modal when clicking outside the modal content
    if (awardsModal) {
        awardsModal.addEventListener('click', function(e) {
            if (e.target === awardsModal) {
                closeAwardsModal();
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
            if (awardsModal && !awardsModal.classList.contains('hidden')) {
                closeAwardsModal();
            }
        }
    });
});

// Translation Process Carousel functionality (for service-translation.html)
document.addEventListener('DOMContentLoaded', function() {
    const processCarousel = document.getElementById('processCarousel');
    const processItems = document.querySelectorAll('#processCarousel .carousel-item');
    const processDotsContainer = document.getElementById('carouselDots');
    const processPrevBtn = document.getElementById('prevBtn');
    const processNextBtn = document.getElementById('nextBtn');
    
    if (!processCarousel || !processPrevBtn || !processNextBtn || !processDotsContainer) return; // Exit if elements not found
    
    // Prevent duplicate initialization
    if (processDotsContainer.hasAttribute('data-initialized')) return;
    processDotsContainer.setAttribute('data-initialized', 'true');
    
    let processCurrentIndex = 0;
    const processTotalItems = processItems.length;
    
    // Clear existing dots (in case of duplicate scripts)
    processDotsContainer.innerHTML = '';
    
    // Generate dots with different styles for special steps
    for (let i = 0; i < processTotalItems; i++) {
        const dot = document.createElement('button');
        // Steps 1-2 are special (larger, pill shape), Steps 3-8 are normal (small, round)
        if (i <= 1) {
            // Special steps 1-2: larger pill shape
            dot.className = `w-6 h-3 rounded-full ${i === 0 ? 'bg-secondary' : 'bg-gray-300'} transition-colors`;
        } else {
            // Normal steps 3-8: small round dots
            dot.className = `w-3 h-3 rounded-full ${i === 0 ? 'bg-primary' : 'bg-gray-300'} transition-colors`;
        }
        dot.addEventListener('click', () => goToProcessSlide(i));
        processDotsContainer.appendChild(dot);
    }
    
    function updateProcessCarousel() {
        // Ensure currentIndex is within bounds
        if (processCurrentIndex >= processTotalItems) {
            processCurrentIndex = 0;
        } else if (processCurrentIndex < 0) {
            processCurrentIndex = processTotalItems - 1;
        }
        
        const translateValue = -processCurrentIndex * 100 + '%';
        processCarousel.style.transform = `translateX(${translateValue})`;
        
        // Update dots with different styles for special steps
        const dots = processDotsContainer.querySelectorAll('button');
        dots.forEach((dot, index) => {
            if (index === processCurrentIndex) {
                // Active state: different colors for special vs normal steps
                dot.classList.remove('bg-gray-300');
                if (index <= 1) {
                    dot.classList.add('bg-secondary'); // Special steps use secondary color
                } else {
                    dot.classList.add('bg-primary');   // Normal steps use primary color
                }
            } else {
                // Inactive state: all steps use gray
                dot.classList.remove('bg-primary', 'bg-secondary');
                dot.classList.add('bg-gray-300');
            }
        });
        
        // Show/hide badge based on current step
        const badges = document.querySelectorAll('[id*="sameDayBadge"]');
        badges.forEach(badge => {
            if (processCurrentIndex <= 1) { // Steps 1-2 (indices 0-1) - special steps
                badge.style.display = 'block';
            } else { // Steps 3-8 (indices 2-7) - normal steps
                badge.style.display = 'none';
            }
        });
    }
    
    function goToProcessSlide(index) {
        processCurrentIndex = index;
        updateProcessCarousel();
    }
    
    // Previous button click
    processPrevBtn.addEventListener('click', () => {
        processCurrentIndex = (processCurrentIndex - 1 + processTotalItems) % processTotalItems;
        updateProcessCarousel();
    });
    
    // Next button click
    processNextBtn.addEventListener('click', () => {
        processCurrentIndex = (processCurrentIndex + 1) % processTotalItems;
        updateProcessCarousel();
    });
    
    // Touch events for swipe functionality
    let processeTouchStartX = 0;
    let processTouchEndX = 0;
    
    processCarousel.addEventListener('touchstart', (e) => {
        processeTouchStartX = e.changedTouches[0].screenX;
    });
    
    processCarousel.addEventListener('touchend', (e) => {
        processTouchEndX = e.changedTouches[0].screenX;
        handleProcessSwipe();
    });
    
    function handleProcessSwipe() {
        const swipeThreshold = 50;
        if (processTouchEndX < processeTouchStartX - swipeThreshold) {
            // Swipe left (next)
            processNextBtn.click();
        } else if (processTouchEndX > processeTouchStartX + swipeThreshold) {
            // Swipe right (previous)
            processPrevBtn.click();
        }
    }
    
    // Auto-advance carousel (optional)
    const autoAdvanceInterval = setInterval(() => {
        processCurrentIndex = (processCurrentIndex + 1) % processTotalItems;
        updateProcessCarousel();
    }, 5000);
    
    // Stop auto-advance when user interacts
    [processPrevBtn, processNextBtn].forEach(btn => {
        btn.addEventListener('click', () => {
            clearInterval(autoAdvanceInterval);
        });
    });
    
    // Initialize carousel
    updateProcessCarousel();
});

// Tab functionality for service translation page
document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    if (tabBtns.length === 0) return; // Exit if no tabs found
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            
            // Remove active class from all buttons and set inactive styles
            tabBtns.forEach(b => {
                b.classList.remove('active', 'bg-primary', 'text-white');
                b.classList.add('bg-transparent', 'text-gray-600');
                // Update hover classes for inactive state
                b.classList.remove('hover:bg-primary-dark');
                b.classList.add('hover:bg-gray-200', 'hover:text-gray-800');
            });
            
            // Add active class to clicked button and set active styles
            btn.classList.add('active', 'bg-primary', 'text-white');
            btn.classList.remove('bg-transparent', 'text-gray-600');
            // Update hover classes for active state
            btn.classList.remove('hover:bg-gray-200', 'hover:text-gray-800');
            btn.classList.add('hover:bg-primary-dark');
            
            // Hide all tab contents
            tabContents.forEach(content => {
                content.style.display = 'none';
                content.classList.remove('active');
            });
            
            // Show target tab content
            const targetContent = document.getElementById(targetTab + '-tab');
            if (targetContent) {
                targetContent.style.display = 'block';
                targetContent.classList.add('active');
            }
        });
    });
});