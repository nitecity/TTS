# 🗣️ Text To Speech CLI Tool (Powered by ElevenLabs)

This document describes a simple **command-line tool** that uses [ElevenLabs.io](https://elevenlabs.io) to convert text into speech. The tool allows you to generate speech **without accessing the ElevenLabs website** directly.

---

## 🛠 Installation

1. **Install Python**
   Download and install Python from the official website:
   👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Clone The Repository**
   Cloen the repository in your computer:
   ```bash
   git clone https://github.com/nitecity/TTS.git
   ```

2. **Install Required Packages**
   Open your terminal and run:

   ```bash
   pip install colorama
   pip install playsound
   ```

3. **Get Your ElevenLabs API Key**
   Sign in to ElevenLabs and generate your API token from:
   👉 [API Keys Page](https://elevenlabs.io/app/settings/api-keys)

---

## 🚀 How to Use

When you run the script for the **first time**, you will be prompted to enter your `API Key`. This key is stored securely in a `.env` file and won’t be required again unless deleted or changed.

Once the setup is complete, you'll see a prompt showing usage instructions and available voice options.

### 📌 Command Examples

* **Text only**

  ```
  > Hello World!
  ```

* **Use a specific voice**

  ```
  > sarah ;; Hello World!
  ```

* **Add a new voice manually**

  ```
  > add ;; ethan ;; g5CIjZEefAph4nQFvHAz
  ```
