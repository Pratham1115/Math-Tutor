
let progressData = [];
progressData.push({
  score: data.score,
  accuracy: data.accuracy
});

let currentQuestion = {};

updateChart();


async function getQuestion() {
  document.getElementById("result").innerText = "";
  document.getElementById("explanation").style.display = "none";

  const topic = document.getElementById("topic").value;
  const url = topic
    ? `http://127.0.0.1:5000/get_question?topic=${topic}`
    : "http://127.0.0.1:5000/get_question";

  const res = await fetch(url);
  const data = await res.json();

  currentQuestion = data;
  document.getElementById("question").innerText = data.question;
  document.getElementById("answer").value = "";
}


async function submitAnswer() {
  const answer = document.getElementById("answer").value.trim();

  if (!answer) {
    alert("Please enter an answer first!");
    return;
  }

  const res = await fetch("http://127.0.0.1:5000/submit_answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_answer: answer,
      correct_answer: currentQuestion.answer,
      id: currentQuestion.id
    }),
  });

  const data = await res.json();

  document.getElementById("result").innerText = data.result;
  document.getElementById("explanation").style.display = "block";
  typeWriterEffect("💡 " + data.explanation, "explanation");

  document.getElementById("score").innerText = data.score;
  document.getElementById("accuracy").innerText = data.accuracy + "%";
  document.getElementById("difficulty").innerText = data.next_difficulty;
}

function typeWriterEffect(text, elementId) {
  let i = 0;
  const element = document.getElementById(elementId);
  element.innerText = "";
  const speed = 25;
  function type() {
    if (i < text.length) {
      element.innerText += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  }
  type();
}

window.onload = getQuestion;
const ctx = document.getElementById('progressChart').getContext('2d');
const progressChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: 'Accuracy (%)',
        data: [],
        borderWidth: 2,
        borderColor: 'blue',
        fill: false
      }
    ]
  },
  options: {
    scales: {
      y: { beginAtZero: true, max: 100 }
    }
  }
});

function updateChart() {
  progressChart.data.labels.push(progressChart.data.labels.length + 1);
  progressChart.data.datasets[0].data.push(progressData[progressData.length - 1].accuracy);
  progressChart.update();
}
