/**
 * Exam Dashboard Logic
 * Handles session initiation and UI feedback
 */

const startExam = (examId) => {
    const confirmation = confirm(`Are you ready to start Exam #${examId}? Your timer will begin immediately.`);
    
    if (confirmation) {
        // Find the specific card
        const card = document.getElementById(`exam-card-${examId}`);
        const button = card.querySelector('.btn-start-exam');
        
        // Visual Feedback: Loading State
        button.innerText = "Loading...";
        button.style.opacity = "0.7";
        button.disabled = true;

        setTimeout(() => {
            alert("Redirecting to Secure Exam Browser Environment...");
            // In a real app: window.location.href = `/exam-session/${examId}`;
        }, 1200);
    }
};

// Add a subtle entrance animation to stat cards
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.stat-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });
});

