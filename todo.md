# Unified AI Agent Dashboard - Development Plan

## 1. Project Setup &amp; File Creation
- [x] Create `todo.md`: Outline all development stages.
- [x] Create `app.py`: Main Flask application file.
- [x] Create `index.html`: Main HTML template for the dashboard.
- [x] Create `style.css`: CSS for styling, including dark/light modes.
- [x] Create `script.js`: JavaScript for interactivity (form submission, theme toggle).
- [x] Create `requirements.txt`: List all Python dependencies.
- [x] Create `render.yaml`: Configuration for deployment on Render.
- [x] Create `.env`: For storing secret API keys locally.
- [x] Create `prompts.py`: To store and manage agent-specific system prompts.

## 2. Backend Development (Flask)
- [ ] **Update `app.py`:**
    - [ ] Import necessary libraries (`os`, `requests`, `pydub`, `speech_recognition`, `pytesseract`, `PIL`, `PyPDF2`).
    - [ ] Import `AGENT_PROMPTS` from `prompts.py`.
    - [ ] Define a dictionary for LLM API endpoints and required keys.
    - [ ] Implement helper function for audio transcription (`.wav` to text).
    - [ ] Implement helper function for image OCR (`.png`, `.jpg` to text).
    - [ ] Implement helper function for PDF text extraction.
    - [ ] Implement the main `/process` endpoint logic:
        - [ ] Receive `model`, `agent`, `text_input`, and uploaded files.
        - [ ] Prioritize and process input: audio -> image -> file -> text.
        - [ ] Select the correct system prompt from `AGENT_PROMPTS`.
        - [ ] Construct the payload for the selected LLM API.
        - [ ] Send the request to the LLM API with the correct headers.
        - [ ] Handle API responses and errors gracefully.
        - [ ] Return the AI's response as JSON.

## 3. Frontend Development &amp; Integration
- [ ] **Update `script.js`:**
    - [ ] Ensure the `fetch` call correctly sends all form data (including files) to the `/process` endpoint.
    - [ ] Implement logic to display a loading indicator while waiting for the response.
    - [ ] Render the AI's response in the output box, formatting it correctly (e.g., handling newlines).
    - [ ] Display any errors returned from the backend.
- [ ] **Update `index.html`:**
    - [ ] Ensure all form elements have the correct `name` attributes for backend processing.
    - [ ] Refine the layout and styling as needed.

## 4. Testing &amp; Deployment
- [ ] Install all dependencies from `requirements.txt`.
- [ ] Run the Flask application locally to test all features:
    - [ ] Test model and agent selection.
    - [ ] Test all input types (text, audio, image, PDF).
    - [ ] Verify that responses from different models are displayed correctly.
- [ ] Deploy to Render using the `render.yaml` configuration.
- [ ] Test the live application.