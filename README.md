# Multimodal Smart Receptionist

## Overview
The **Multimodal Smart Receptionist** is an AI-powered system that automates front desk operations using **Deep Learning, NLP, and Speech Recognition**. It efficiently handles **visitor interactions, identity verification, and real-time query resolution**, making it a superior alternative to traditional receptionists.

## Features
- **Face Recognition**: Uses **128D facial feature vectors** and **SVM classification** for **97.5% accurate identity verification**.
- **Automated Voice Interaction (AVI)**: Processes user queries via **speech recognition and NLP**, powered by the **LLaMA-2 model**.
- **Multi-Factor Authentication**: Ensures high security with **face verification and secure data storage**.
- **Real-Time Adaptability**: Handles variations in **lighting, background, expressions, and camera noise**.
- **High Accuracy**: Achieves **98.25% response accuracy**, making it fast, reliable, and intelligent.

## Tech Stack
- **Programming Language**: Python
- **Libraries & Frameworks**:
  - OpenCV (Face detection & image processing)
  - Dlib & Face Recognition (Facial feature extraction)
  - Scikit-learn (SVM classification & model training)
  - SpeechRecognition & pyttsx3 (Voice processing)
  - SpaCy (NLP for named entity extraction)
  - LLaMA-2 (LLM for real-time AI-driven responses)

## System Workflow
1. **Face Detection & Recognition**
   - Captures a live video frame (10 seconds) and detects faces.
   - Extracts **128D feature vectors** and computes the **mean vector** for stable recognition.
   - Matches the feature vector with stored identities using an **SVM model**.

2. **Automated Voice Interaction**
   - Uses **Speech Recognition** to process user commands.
   - Extracts names and intent using **NLP (SpaCy)**.
   - Integrates with **LLaMA-2 APIs** for real-time responses.
   - Converts text responses into speech via **pyttsx3**.

3. **Security & Authentication**
   - Implements **multi-factor authentication** with face verification.
   - Ensures **data encryption & secure user identity storage**.

4. **Handling Variance**
   - Uses **mean feature computation** to reduce variations caused by **pose, lighting, and expressions**.
   - Enhances accuracy with **optimized SVM parameters (C & gamma tuning, Grid Search, and k-Fold Cross-Validation)**.

## Dataset Preparation
- Captures **different backgrounds, lighting conditions, and face alignments** to improve robustness.

## Results & Performance
- **Face Recognition Accuracy**: 97.5%
- **Speech Recognition & Response Accuracy**: 98.25%
- **Faster identity verification & query handling compared to traditional methods**.

## Installation & Usage
### Prerequisites
- Python 3.x
- Install dependencies:
  ```bash
  pip install opencv-python dlib face-recognition numpy scikit-learn SpeechRecognition pyttsx3 spacy
  ```
- Download the required **face detection model**:
  ```bash
  python -m spacy download en_core_web_sm
  ```

### Running the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/aakriti1613/multimodal-smart-receptionist.git
   ```
2. Navigate to the project folder:
   ```bash
   cd Smart_Receptionist
   ```
3. Run the script:
   ```bash
   JARVIS.py
   ```

## Future Enhancements
- **Multilingual Support**: Expanding to support multiple languages.
- **Gesture & Emotion Recognition**: Enhancing user interaction.
- **Cloud Integration**: Secure and scalable database storage.  

## License
This project is licensed under the **MIT License**.

---
### 🚀 **A Smarter Way to Manage Front Desks with AI!**

