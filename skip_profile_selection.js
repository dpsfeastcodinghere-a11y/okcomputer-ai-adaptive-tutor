document.addEventListener('DOMContentLoaded', function () {
    const step1 = document.getElementById('onboardingStep1');
    if (step1) {
        step1.style.display = 'none';
    }

    const step2 = document.getElementById('onboardingStep2');
    if (step2) {
        step2.classList.remove('hidden');
        step2.style.display = 'block';
    }

    localStorage.setItem('profileType', 'weak');
    localStorage.setItem('studentName', 'Student');
});
