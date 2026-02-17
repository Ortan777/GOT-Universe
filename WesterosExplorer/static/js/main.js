// Main JavaScript for Westeros Explorer

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Westeros Explorer loaded!');
    
    // Initialize tooltips
    initTooltips();
    
    // Add smooth scrolling
    initSmoothScroll();
    
    // Add hover effects
    initHoverEffects();
});

// Tooltips for character cards
function initTooltips() {
    const cards = document.querySelectorAll('.character-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function(e) {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function(e) {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Hover effects for buttons
function initHoverEffects() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-signin');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// Character search function (to be implemented)
function searchCharacters(query) {
    console.log('Searching for:', query);
    // Will implement later
}

// Filter by house
function filterByHouse(houseId) {
    if (houseId) {
        window.location.href = '/characters/?house=' + houseId;
    } else {
        window.location.href = '/characters/';
    }
}

// View character details
function viewCharacter(characterId) {
    window.location.href = '/characters/' + characterId + '/';
}

// Toggle mobile menu
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Add mobile menu button if needed
if (window.innerWidth <= 768) {
    const nav = document.querySelector('.nav-container');
    const menuButton = document.createElement('button');
    menuButton.innerHTML = '☰';
    menuButton.className = 'mobile-menu-btn';
    menuButton.onclick = toggleMobileMenu;
    nav.appendChild(menuButton);
}