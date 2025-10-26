# 🧮 MathTutor AI — Intelligent Learning Assistant

MathTutor AI is a smart, interactive web app that helps users **learn math topics step-by-step** using **AI + Machine Learning**.  
It explains concepts in simple terms, gives practice questions, tracks performance, and adjusts question difficulty based on response time and accuracy.  
Users can also **import question banks or PDFs**, **search topics**, and **view their progress dashboard**.

---

## 🚀 Features

### 🎓 Learning & Teaching
- Search for any math topic using the built-in search bar.  
- AI explains the topic in **easy, beginner-friendly language** with examples.  
- Generates **practice questions** related to the topic.

### 📊 Smart Progress Tracking
- Tracks user performance:
  - Total questions attempted  
  - Correct answers  
  - Accuracy percentage  
  - Weak topics
- Displays progress visually using **Chart.js** doughnut charts.

### 🧠 Adaptive Learning
- Uses **response time**, **accuracy**, and **hints used** to adjust difficulty level dynamically.  
- Provides personalized feedback and suggestions.

### 📂 Question Bank Import
- Allows importing **custom question banks** or **PDFs**.  
- The system reads and organizes them into topic-wise sections for easier learning.

### 🖥️ Clean & Responsive Front-End
- Built using **HTML, CSS, and JavaScript**.  
- Dashboard view for user stats.  
- Topic view for explanations, examples, and practice questions.

---

## 🏗️ Project Structure
MathTutorAI/
│
├── index.html # Main UI (search, topic display, dashboard)
├── style.css # Styling for layout, dashboard, and charts
├── script.js # Handles UI logic, events, and chart updates
└── README.md # This file


---

## how it works
User searches topic → Frontend sends query to backend
        ↓
   Backend uses AI to explain & generate example
        ↓
   Frontend displays explanation + questions
        ↓
   User answers → Time & accuracy tracked
        ↓
   Dashboard updates → AI adjusts next question difficulty
