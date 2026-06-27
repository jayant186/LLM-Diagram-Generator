# LLM Diagram Generator

LLM Diagram Generator is an AI-powered full-stack web application that converts unstructured text and PDF documents into interactive workflow diagrams. It uses Google's Gemini API to extract workflow information, generates Mermaid diagrams, and allows users to edit, preview, and export diagrams in real time.

---

## Features

* Convert text into interactive flowcharts
* Convert PDF documents into diagrams
* AI-powered workflow extraction using Gemini
* Automatic Mermaid diagram generation
* Editable Mermaid code with live preview
* Export diagrams as PNG
* Export diagrams as SVG
* Responsive React frontend
* Flask REST API backend

---

## Tech Stack

### Frontend

* React.js
* Vite
* Mermaid.js
* html-to-image

### Backend

* Flask
* Python
* Google Gemini API
* PyPDF

---

## Project Architecture

```text
                Text / PDF
                     │
                     ▼
            Flask Backend
                     │
                     ▼
        Google Gemini API
                     │
                     ▼
      Workflow Extraction
                     │
                     ▼
        Mermaid Generation
                     │
                     ▼
        React Frontend
                     │
                     ▼
        Interactive Diagram
```

---

## Project Workflow

```text
Text / PDF
      │
      ▼
Extract Text (PDF)
      │
      ▼
Gemini Workflow Extraction
      │
      ▼
Nodes & Relationships
      │
      ▼
Mermaid Code Generation
      │
      ▼
Interactive Visualization
```

---

## Screenshots

### Home Page

![Home](Screenshots/Home.png)

---

### Generated Diagram

![Diagram](Screenshots/Demo_Output.png)

---

### Editable Mermaid Code

![Editor](Screenshots/Editable_Mermaid_Code.png)

---

### Exported Diagram

![Flowchart](Screenshots/Flowchart.svg)

---

## Installation

### Clone the repository

```bash
git clone https://github.com/jayant186/LLM-Diagram-Generator.git
cd LLM-Diagram-Generator
```

### Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate        # macOS/Linux

pip install -r requirements.txt

python app.py
```

Backend runs at:

```
http://localhost:5000
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## Environment Variables

Create a `.env` file inside the `backend` folder.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Future Improvements

* Additional diagram types
* RAG-based workflow extraction
* Multi-page PDF support
* Drag-and-drop diagram editing
* User authentication
* Cloud storage integration

---

## License

This project is intended for educational and portfolio purposes.
