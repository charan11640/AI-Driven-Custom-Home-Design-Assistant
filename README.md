# 🏠 AI-Driven Custom Home Design Assistant

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-orange?logo=streamlit)](https://streamlit.io/) [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Create personalized home designs instantly with the power of AI! This Streamlit app leverages Google Gemini and Unsplash APIs to generate detailed home design plans and visual inspirations tailored to your preferences.

---

## 🚀 Project Overview & Architecture

This app provides an interactive web interface for users to generate custom home design plans using generative AI. It supports multiple user scenarios (real estate, renovation, architecture), room-by-room customization, and visual inspiration via Unsplash images.

**Main Components:**
- **`app.py`**: Main Streamlit app, UI, and logic.
- **Google Gemini API**: Generates design plans based on user input.
- **Unsplash API**: Fetches relevant home design images.
- **Session State**: Caches results and manages dynamic room forms.
- **Requirements**: See `requirements.txt` for all dependencies.

**Extensibility:**
- Add new design styles by updating the `style_images` dictionary in `app.py`.
- Integrate other AI models by modifying the `generate_design_idea` function.
- Add new amenities or room types by editing the relevant lists in the UI section.

---

## ✨ Features Table

| Feature                        | Description                                                      |
|-------------------------------|------------------------------------------------------------------|
| AI Design Generation           | Custom plans based on style, size, rooms, and preferences         |
| Room-by-Room Customization     | Add, edit, or remove rooms with specific details                  |
| Scenario Workflows             | Real Estate, Renovation, and Architectural Firm modes             |
| Visual Inspiration             | Fetches Unsplash images based on your design query                |
| Amenities Selection            | Choose from a list of modern amenities                            |
| Floor Plan Upload              | Upload current floor plan (image/PDF) for renovation scenarios    |
| Downloadable Plans             | Export your design as a Markdown file                             |
| Session Caching                | Avoids redundant API calls for repeated queries                   |
| Responsive UI                  | Modern, interactive Streamlit interface                           |

---

## 🖼️ Demo

![Demo Screenshot](https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80)

---

## ⚡ Getting Started

### 1. Clone the Repository

```bash
https://github.com/charan11640/AI-Driven-Custom-Home-Design-Assistant/tree/main
cd AI-Driven-Custom-Home-Design-Assistant-main
```

### 2. Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following content:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
UNSPLASH_ACCESS_KEY=your_unsplash_access_key
```

**Example:**
```env
GOOGLE_API_KEY=AIzaSyD...yourkey...
UNSPLASH_ACCESS_KEY=Qx...yourkey...
```

- **GOOGLE_API_KEY:** Get from [Google AI Studio](https://aistudio.google.com/app/apikey).
- **UNSPLASH_ACCESS_KEY:** Get from [Unsplash Developers](https://unsplash.com/developers).

### 4. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

---

## 🛠️ Usage

1. **Choose a scenario:** Real Estate Development, Home Renovation, or Architectural Firm.
2. **Fill in design preferences:** Style, size, number of rooms, special requirements, and amenities.
3. **Customize rooms:** Add, edit, or remove rooms with specific details.
4. **(Optional) Upload a floor plan** for renovation scenarios.
5. **Generate your design:** View the AI-generated plan and visual inspirations.
6. **Download the plan** as a Markdown file.

---

## 🧩 Requirements

- Python 3.8+
- See `requirements.txt` for Python dependencies:
  - streamlit
  - google-generativeai
  - python-dotenv
  - requests
  - fpdf
  - PyPDF2
  - python-docx

---

## 🔑 Environment Variables

| Variable              | Description                                 |
|----------------------|---------------------------------------------|
| `GOOGLE_API_KEY`     | Google Gemini API key                       |
| `UNSPLASH_ACCESS_KEY`| Unsplash API access key                     |

---

## ❓ FAQ

**Q: Why do I need API keys?**
A: The app uses Google Gemini for AI design generation and Unsplash for images, both of which require API authentication.

**Q: Can I use my own images?**
A: Yes, you can upload your own floor plan images for renovation scenarios.

**Q: How do I add new amenities or room types?**
A: Edit the `amenities` or `room_types` lists in `app.py`.

**Q: Can I export or share my design?**
A: Yes, use the "Save Design Plan" button to download your plan as a Markdown file.

**Q: What if I get API errors?**
A: Double-check your `.env` file and API key validity. Restart the app after changes.

---

## 🤝 How to Contribute

1. Fork this repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request describing your changes

**Ideas for Contribution:**
- Add new design styles or amenities
- Improve UI/UX
- Add support for more file types (e.g., DOCX export)
- Integrate additional AI models
- Add localization/multilanguage support

---

## 🧑‍💻 Extending the App

- **Add new design styles:** Update the `style_images` dictionary in `app.py`.
- **Integrate other AI models:** Modify the `generate_design_idea` function.
- **Add new amenities/room types:** Edit the lists in the UI section.
- **Support more file types:** Add logic for DOCX or PDF export using `python-docx` or `fpdf`.

---

## 🐞 Troubleshooting

- **API Key Errors:**
  - Ensure your `.env` file is present and keys are correct.
  - Restart the app after updating environment variables.
- **Image Loading Issues:**
  - Unsplash API quota may be exceeded or key is missing.
- **PDF Uploads:**
  - PDF preview is not supported, but files are accepted for reference.

---

## 📄 License

[MIT License](LICENSE)

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Google Gemini](https://aistudio.google.com/)
- [Unsplash](https://unsplash.com/) 
