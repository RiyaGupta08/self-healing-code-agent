# 🧠 Self-Healing Code Agent (Python Debugging System)

The Self-Healing Code Agent is an intelligent full-stack web application designed to simplify the debugging process in Python programming. Debugging is often one of the most time-consuming and frustrating parts of development, especially for beginners who struggle to interpret error messages and identify the root cause of issues. This project aims to address that problem by automatically detecting, analyzing, and fixing common Python errors with minimal human effort.

The system combines rule-based techniques with machine learning to provide accurate and efficient solutions. Instead of just identifying errors, it goes a step further by suggesting fixes, applying the most suitable correction, and verifying whether the corrected code works as expected. This makes the system not only a debugging tool but also a learning assistant for developers.

---

## 🚀 Key Features

The application is capable of detecting both syntax and runtime errors in Python code. It intelligently classifies errors using machine learning models and generates multiple possible fixes for each issue. These fixes are then ranked based on confidence, simplicity, and past success rates, ensuring that the most effective solution is selected.

A unique aspect of the system is its semantic memory, implemented using FAISS. This allows the application to learn from previous debugging experiences and improve its recommendations over time. Additionally, all fixes are tested in a sandboxed environment to ensure safety and correctness before being returned to the user.

The system also includes smart typo detection, automatically correcting common mistakes such as misspelled keywords (e.g., `retrun` to `return`). Despite its advanced capabilities, the application maintains a fast response time of approximately 1–3 seconds.

---

## 🏗️ Project Structure

The project is organized into separate frontend and backend components to ensure modularity and scalability. The frontend is responsible for providing a clean and interactive user interface, while the backend handles all core logic, including error detection, classification, and fix generation.

```
self-healing-code-agent/
│
├── frontend/        # React-based user interface
├── backend/         # FastAPI backend and debugging engine
├── screenshots/     # Application screenshots
│   ├── input.png
│   └── output.png
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Technology Stack

The frontend of the application is built using React and TypeScript, providing a responsive and user-friendly interface. Tailwind CSS is used for styling to ensure a clean and modern design.

The backend is developed using FastAPI, a high-performance Python framework. Machine learning functionality is implemented using Scikit-learn, while FAISS is used to build a semantic memory system that improves the system over time.

---

## ⚙️ Installation and Setup

To run the project locally, start by cloning the repository:

```
git clone https://github.com/RiyaGupta08/self-healing-code-agent.git
cd self-healing-code-agent
```

Next, set up the backend by installing the required dependencies and running the server:

```
cd backend
pip install -r requirements.txt
python api_backend.py
```

The backend will start running at `http://localhost:8000`.

After that, set up the frontend:

```
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## 🔄 How the System Works

The workflow of the system begins when a user enters Python code into the interface. This code is sent to the backend through an API request, where it undergoes a two-stage error detection process.

First, the system checks for syntax errors using Python’s Abstract Syntax Tree (AST). Then, it executes the code in a controlled environment to detect runtime errors. Once the error is identified, a machine learning model classifies it into a specific category.

Based on this classification, the system generates multiple possible fixes. These fixes are ranked using a combination of machine learning confidence, historical success rates, and simplicity. The best fix is selected and applied, and the corrected code is tested in a sandbox environment to ensure it works correctly.

Finally, the fixed code is returned to the frontend and displayed to the user.

---

## 📸 Application Preview

Below are sample screenshots demonstrating how the system processes and fixes code errors:

### Input Code
<img width="880" height="411" alt="Screenshot 2026-04-21 114241" src="https://github.com/user-attachments/assets/d0a83e2b-f03c-4763-97b9-02a9c572359b" />



### Output Code
<img width="889" height="322" alt="Screenshot 2026-04-21 114254" src="https://github.com/user-attachments/assets/f17972c7-2508-4867-ad4c-a4cc3a525692" />



---

## 📊 Performance

The system demonstrates strong performance across different types of errors. It achieves approximately 95% accuracy for syntax errors, around 88% accuracy for typo-related issues, and about 82% accuracy for runtime errors. The average response time remains between 1 to 3 seconds, making it efficient for real-time usage.

---

## 📌 Future Scope

The current implementation focuses on Python, but the system can be extended to support additional programming languages such as Java, C++, and JavaScript. Future improvements may include integration with IDEs like Visual Studio Code, the use of advanced AI models such as large language models, and deployment on cloud platforms for scalability.

---
