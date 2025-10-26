const searchBtn = document.getElementById('searchBtn');
const searchBar = document.getElementById('searchBar');
const contentArea = document.getElementById('contentArea');
const dashboardBtn = document.getElementById('dashboardBtn');
const dashboard = document.getElementById('dashboard');

// Tracking data
let totalQuestions = 0;
let correctAnswers = 0;
let topicStats = {}; // store weak topics

// Topic database
const topics = {
    addition: {
        explanation: "Addition means putting things together.",
        example: "Example: 3 + 2 = 5",
        question: "What is 7 + 4?",
        answer: 11
    },
    subtraction: {
        explanation: "Subtraction means taking away.",
        example: "Example: 9 - 5 = 4",
        question: "What is 12 - 7?",
        answer: 5
    },
    multiplication: {
        explanation: "Multiplication means repeated addition.",
        example: "Example: 3 × 4 = 12",
        question: "What is 6 × 5?",
        answer: 30
    },
    division: {
        explanation: "Division means splitting into equal parts.",
        example: "Example: 8 ÷ 2 = 4",
        question: "What is 20 ÷ 5?",
        answer: 4
    }
};

// Handle Search
searchBtn.addEventListener('click', () => {
    const topic = searchBar.value.trim().toLowerCase();

    dashboard.style.display = "none"; // hide dashboard
    if (topic === "") {
        contentArea.innerHTML = "<p>Please enter a topic to search.</p>";
        return;
    }

    if (topics[topic]) {
        const data = topics[topic];
        contentArea.innerHTML = `
            <h2>${topic.charAt(0).toUpperCase() + topic.slice(1)}</h2>
            <p><strong>Explanation:</strong> ${data.explanation}</p>
            <p><strong>${data.example}</strong></p>
            <h3>Try This:</h3>
            <p>${data.question}</p>
            <input type="number" id="userAnswer" placeholder="Enter your answer">
            <button id="checkBtn">Check Answer</button>
            <p id="feedback"></p>
        `;

        const checkBtn = document.getElementById('checkBtn');
        checkBtn.addEventListener('click', () => {
            const userAnswer = parseInt(document.getElementById('userAnswer').value);
            const feedback = document.getElementById('feedback');
            totalQuestions++;

            if (userAnswer === data.answer) {
                correctAnswers++;
                feedback.textContent = "✅ Correct! Great job!";
                feedback.style.color = "green";
            } else {
                feedback.textContent = `❌ Oops! The correct answer is ${data.answer}.`;
                feedback.style.color = "red";
                topicStats[topic] = (topicStats[topic] || 0) + 1;
            }

            updateDashboard();
        });
    } else {
        contentArea.innerHTML = `
            <p>Sorry, MathTutor AI doesn’t know about <strong>${topic}</strong> yet.</p>
            <p>Try topics like: <em>addition, subtraction, multiplication, division</em>.</p>
        `;
    }
});

// Handle Dashboard Button
dashboardBtn.addEventListener('click', () => {
    dashboard.style.display = "block";
    contentArea.innerHTML = ""; // clear main area
    updateDashboard();
});

// Function to update dashboard
let progressChart = null; // to store the chart instance

function updateDashboard() {
    const accuracy = totalQuestions > 0 ? ((correctAnswers / totalQuestions) * 100).toFixed(1) : 0;

    document.getElementById('totalQ').textContent = totalQuestions;
    document.getElementById('correctQ').textContent = correctAnswers;
    document.getElementById('accuracy').textContent = `${accuracy}%`;

    // Weak topics
    let weakList = Object.keys(topicStats).filter(t => topicStats[t] > 1);
    document.getElementById('weakTopics').textContent = weakList.length > 0 ? weakList.join(", ") : "None";

    // 🎨 Update Chart
    const ctx = document.getElementById('progressChart').getContext('2d');

    const data = {
        labels: ['Correct', 'Incorrect'],
        datasets: [{
            data: [correctAnswers, totalQuestions - correctAnswers],
            backgroundColor: ['#28a745', '#dc3545']
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Your Accuracy Overview',
                    font: { size: 16 }
                }
            }
        }
    };

    // Destroy old chart before creating a new one (to avoid duplicates)
    if (progressChart) {
        progressChart.destroy();
    }
    progressChart = new Chart(ctx, config);
}

