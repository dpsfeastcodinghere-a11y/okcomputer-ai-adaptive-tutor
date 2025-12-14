// GyanNova - Adaptive Learning Platform JavaScript
// Main functionality for interactive learning experience

class EduAIPlatform {
    constructor() {
        this.currentStudent = null;
        this.selectedSubject = null;
        this.diagnosticResults = {};
        this.learningEngine = null;
        this.init();
    }

    init() {
        this.initializeTypewriter();
        this.initializeAnimations();
        this.initializeEventListeners();
        this.initializeCounters();
        this.loadStudentData();
    }

    // Initialize typewriter effect for hero text
    initializeTypewriter() {
        if (document.querySelector('.typewriter')) {
            new Typed('.typewriter', {
                strings: [
                    'Learn Smarter',
                    'Learn Faster',
                    'Learn Better',
                    'Learn with AI'
                ],
                typeSpeed: 80,
                backSpeed: 50,
                backDelay: 2000,
                loop: true,
                showCursor: true,
                cursorChar: '|'
            });
        }
    }

    // Initialize scroll animations
    initializeAnimations() {
        // Animate elements on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target);
                }
            });
        }, observerOptions);

        // Observe all subject cards and feature elements
        document.querySelectorAll('.subject-card, .feature-icon').forEach(el => {
            observer.observe(el);
        });

        // Floating shapes animation
        this.animateFloatingShapes();
    }

    // Animate individual elements
    animateElement(element) {
        if (element.classList.contains('subject-card')) {
            anime({
                targets: element,
                translateY: [50, 0],
                opacity: [0, 1],
                duration: 800,
                easing: 'easeOutCubic',
                delay: Math.random() * 200
            });
        } else if (element.classList.contains('feature-icon')) {
            anime({
                targets: element,
                scale: [0.8, 1],
                rotate: [0, 360],
                duration: 1000,
                easing: 'easeOutElastic(1, .8)'
            });
        }
    }

    // Animate floating shapes in hero section
    animateFloatingShapes() {
        const shapes = document.querySelectorAll('.floating-shape');
        shapes.forEach((shape, index) => {
            anime({
                targets: shape,
                translateY: [0, -20, 0],
                rotate: [0, 360],
                duration: 15000 + (index * 2000),
                loop: true,
                easing: 'easeInOutSine',
                delay: index * 1000
            });
        });
    }

    // Initialize counter animations
    initializeCounters() {
        const counters = document.querySelectorAll('.stats-counter');
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        });

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }

    // Animate counter numbers
    animateCounter(element) {
        const target = parseInt(element.dataset.target);
        const duration = 2000;

        anime({
            targets: { value: 0 },
            value: target,
            duration: duration,
            easing: 'easeOutExpo',
            update: function (anim) {
                element.textContent = Math.round(anim.animatables[0].target.value).toLocaleString();
            }
        });
    }

    // Initialize event listeners
    initializeEventListeners() {
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });

        // Subject card hover effects
        document.querySelectorAll('.subject-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.enhanceCardHover(card);
            });

            card.addEventListener('mouseleave', () => {
                this.resetCardHover(card);
            });
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    // Enhanced card hover effects
    enhanceCardHover(card) {
        anime({
            targets: card,
            scale: 1.05,
            rotateY: 5,
            duration: 300,
            easing: 'easeOutCubic'
        });
    }

    resetCardHover(card) {
        anime({
            targets: card,
            scale: 1,
            rotateY: 0,
            duration: 300,
            easing: 'easeOutCubic'
        });
    }

    // Subject selection handler
    selectSubject(subject) {
        this.selectedSubject = subject;
        this.startAssessment(); // Skip modal
    }

    // Show subject-specific modal
    showSubjectModal(subject) {
        const modal = document.getElementById('diagnosticModal');
        const subjectInfo = this.getSubjectInfo(subject);

        // Update modal content based on subject
        const modalContent = modal.querySelector('.text-center');
        const subjectEmoji = modalContent.querySelector('.text-2xl');
        const subjectName = modalContent.querySelector('h3');
        const subjectDescription = modalContent.querySelector('p');

        subjectEmoji.textContent = subjectInfo.emoji;
        subjectName.textContent = `Start ${subjectInfo.name} Assessment`;
        subjectDescription.textContent = subjectInfo.description;

        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';

        // Animate modal appearance
        anime({
            targets: modal.querySelector('.bg-white'),
            scale: [0.8, 1],
            opacity: [0, 1],
            duration: 300,
            easing: 'easeOutCubic'
        });
    }

    // Get subject information
    getSubjectInfo(subject) {
        const subjects = {
            mathematics: {
                name: 'Mathematics',
                emoji: '📐',
                description: 'We\'ll assess your current math skills across algebra, geometry, and arithmetic to create your personalized learning path.'
            },
            science: {
                name: 'Science',
                emoji: '🔬',
                description: 'Let\'s evaluate your understanding of physics, chemistry, and biology concepts to tailor your learning experience.'
            },
            english: {
                name: 'English',
                emoji: '📚',
                description: 'We\'ll assess your grammar, vocabulary, and comprehension skills to create a customized English learning plan.'
            },
            'social_studies': {
                name: 'Social Studies',
                emoji: '🌍',
                description: 'Let\'s evaluate your knowledge of history, geography, and civics to build your personalized learning journey.'
            },
            hindi: {
                name: 'Hindi',
                emoji: '📖',
                description: 'We\'ll assess your Hindi grammar, literature, and writing skills to create your custom learning path.'
            },
            all: {
                name: 'Complete Assessment',
                emoji: '🎯',
                description: 'Take a comprehensive assessment across all subjects to identify your strengths and areas for improvement.'
            }
        };

        return subjects[subject] || subjects.all;
    }

    // Close modal
    closeModal() {
        const modal = document.getElementById('diagnosticModal');

        anime({
            targets: modal.querySelector('.bg-white'),
            scale: [1, 0.8],
            opacity: [1, 0],
            duration: 200,
            easing: 'easeInCubic',
            complete: () => {
                modal.classList.add('hidden');
                document.body.style.overflow = 'auto';
            }
        });
    }

    // Start diagnostic assessment (Modified: Skips Modal)
    startAssessment() {
        const name = "Student"; // Default name as user requested to skip prompt
        const studentClass = "9"; // Default class
        const weakestSubject = this.selectedSubject || "mathematics";

        // Create student profile
        this.currentStudent = {
            id: `student_${Date.now()}`,
            name: name,
            class: studentClass,
            weakestSubject: weakestSubject,
            subject: this.selectedSubject,
            startTime: new Date()
        };

        // Reset progress explicitly for every new start
        localStorage.setItem('problemsSolved', '0');
        localStorage.setItem('currentStudent', JSON.stringify(this.currentStudent));

        // Redirect to learning page
        window.location.href = 'learning.html';
    }

    // Show loading screen
    showLoadingScreen() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'fixed inset-0 bg-white z-50 flex items-center justify-center';
        loadingDiv.innerHTML = `
            <div class="text-center">
                <div class="w-16 h-16 border-4 border-sage-green border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <p class="text-xl font-semibold text-gray-800">Creating your personalized learning path...</p>
            </div>
        `;
        document.body.appendChild(loadingDiv);
    }

    // Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm ${type === 'error' ? 'bg-red-500 text-white' : 'bg-green-500 text-white'
            }`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Animate in
        anime({
            targets: notification,
            translateX: [300, 0],
            opacity: [0, 1],
            duration: 300,
            easing: 'easeOutCubic'
        });

        // Remove after 3 seconds
        setTimeout(() => {
            anime({
                targets: notification,
                translateX: [0, 300],
                opacity: [1, 0],
                duration: 300,
                easing: 'easeInCubic',
                complete: () => {
                    document.body.removeChild(notification);
                }
            });
        }, 3000);
    }

    // Load student data from localStorage
    loadStudentData() {
        const savedStudent = localStorage.getItem('currentStudent');
        if (savedStudent) {
            this.currentStudent = JSON.parse(savedStudent);
        }
    }

    // Scroll to subjects section
    scrollToSubjects() {
        document.getElementById('subjects').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }

    // Start diagnostic assessment (Modified: Direct Start)
    startDiagnostic() {
        this.selectedSubject = 'all';
        this.startAssessment(); // Skip modal, just go
    }

    // Initialize diagnostic test (placeholder for future implementation)
    initializeDiagnostic() {
        // This will be implemented when we create the diagnostic system
        console.log('Diagnostic system initialized');
    }

    // Performance monitoring
    trackPerformance(action, data = {}) {
        const performanceData = {
            action: action,
            timestamp: new Date().toISOString(),
            student: this.currentStudent?.id,
            subject: this.selectedSubject,
            ...data
        };

        // Store in localStorage for now (in production, this would go to a backend)
        const performanceLog = JSON.parse(localStorage.getItem('performanceLog') || '[]');
        performanceLog.push(performanceData);
        localStorage.setItem('performanceLog', JSON.stringify(performanceLog));
    }
}

// Global functions for HTML onclick handlers
function selectSubject(subject) {
    platform.selectSubject(subject);
}

function closeModal() {
    platform.closeModal();
}

function startAssessment() {
    platform.startAssessment();
}

function scrollToSubjects() {
    platform.scrollToSubjects();
}

function startDiagnostic() {
    platform.startDiagnostic();
}

// Initialize the platform when DOM is loaded
let platform;
document.addEventListener('DOMContentLoaded', () => {
    platform = new EduAIPlatform();

    // Auto-open diagnostic modal on load - DISABLED per request
    // platform.startDiagnostic();

    // Add some additional interactive enhancements
    addScrollEffects();
    addHoverEffects();
});

// Add scroll-based effects
function addScrollEffects() {
    let ticking = false;

    function updateScrollEffects() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;

        // Parallax effect for hero background
        const hero = document.querySelector('.hero-bg');
        if (hero) {
            hero.style.transform = `translateY(${rate}px)`;
        }

        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateScrollEffects);
            ticking = true;
        }
    }

    window.addEventListener('scroll', requestTick);
}

// Add enhanced hover effects
function addHoverEffects() {
    // Button hover effects
    document.querySelectorAll('.btn-primary').forEach(button => {
        button.addEventListener('mouseenter', function () {
            anime({
                targets: this,
                scale: 1.05,
                duration: 200,
                easing: 'easeOutCubic'
            });
        });

        button.addEventListener('mouseleave', function () {
            anime({
                targets: this,
                scale: 1,
                duration: 200,
                easing: 'easeOutCubic'
            });
        });
    });

    // Feature icon hover effects
    document.querySelectorAll('.feature-icon').forEach(icon => {
        icon.addEventListener('mouseenter', function () {
            anime({
                targets: this,
                rotate: '1turn',
                scale: 1.2,
                duration: 600,
                easing: 'easeOutElastic(1, .8)'
            });
        });
    });
}

// Utility functions for future use
const Utils = {
    // Format time duration
    formatDuration(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    },

    // Calculate accuracy percentage
    calculateAccuracy(correct, total) {
        return total > 0 ? Math.round((correct / total) * 100) : 0;
    },

    // Generate random ID
    generateId() {
        return Math.random().toString(36).substr(2, 9);
    },

    // Debounce function for performance
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { EduAIPlatform, Utils };
}