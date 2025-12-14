// ========================================
// QUICK FIX: Remove Profile Selection Modal
// ========================================
// Add this script at the END of learning.html, before </body>

document.addEventListener('DOMContentLoaded', function () {
    // Hide profile selection step (Ram/Rahul)
    const step1 = document.getElementById('onboardingStep1');
    if (step1) {
        step1.style.display = 'none';
    }

    // Show subject selection step directly
    const step2 = document.getElementById('onboardingStep2');
    if (step2) {
        step2.classList.remove('hidden');
        step2.style.display = 'block';
    }

    // Set a default profile (optional - prevents errors)
    localStorage.setItem('profileType', 'weak'); // Default to Ram profile
    localStorage.setItem('studentName', 'Student');

    console.log('✅ Profile selection skipped - going straight to subject selection');
});
