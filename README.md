# IELTSEvaL: Your AI-Powered IELTS Writing Evaluator

IELTSEvaL is a cost-effective, AI-powered evaluation tool that provides detailed feedback on your IELTS writing tasks. It helps you improve your writing skills and boost your IELTS score—all for free!

[Link to the working demo](https://ieltseval.streamlit.app/)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Modules Overview](#modules-overview)
- [Contributing](#contributing)
- [License](#license)

## Features

- Evaluate IELTS Writing Task 1 (Academic and General Training) and Task 2 responses.
- Receive detailed feedback on each evaluation criterion:
  - Task Response
  - Coherence & Cohesion
  - Lexical Resource
  - Grammatical Range & Accuracy
- Get suggestions to improve your writing skills.
- User-friendly Streamlit interface.

## Prerequisites

- Python 3.7 or higher
- A Google API Key with access to PaLM API (for `ChatGoogleGenerativeAI`).
- Prompt template for the language model.
- Encrypted knowledge files containing IELTS evaluation criteria.
- Required Python packages (listed in `requirements.txt`).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ieltseval.git
   cd ieltseval
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Setup

### 1. Provide the Google API Key

- Create a `.streamlit` directory in the root folder if it doesn't exist.

  ```bash
  mkdir .streamlit
  ```

- Create a `secrets.toml` file inside the `.streamlit` directory.

  ```bash
  touch .streamlit/secrets.toml
  ```

- Add your Google API Key to `secrets.toml`:

  ```toml
  GOOGLE_API_KEY = "your_google_api_key_here"
  ```

### 2. Provide the Prompt Template

- In the same `secrets.toml` file, add your prompt template:

  ```toml
  prompt_template = """
  [Your prompt template here]
  """
  ```

### 3. Provide the Encryption Key

- Add the encryption key used to encrypt the knowledge files:

  ```toml
  encryption_key = "your_encryption_key_here"
  ```

### 4. Add the Knowledge Files

- Place the encrypted knowledge files in the `tasks` directory:

  ```
  tasks/
  ├── Academic_IELTS_Writing_Task_1_Band_Descriptors.json.enc
  ├── General_Training_IELTS_Writing_Task_1_Band_Descriptors.json.enc
  └── IELTS_Writing_Task_2_Band_Descriptors.json.enc
  ```

- **Note:** The knowledge files are encrypted. You need to generate the encryption key and encrypt the files if not provided.

### 5. Encrypting Knowledge Files (If Needed)

If you have the plaintext JSON files and need to encrypt them:

- Run the `encryptc.py` script in the `tasks` directory to encrypt your JSON files.

  ```bash
  python tasks/encryptc.py
  ```

- This script will generate an encryption key and encrypt the specified JSON files, saving them with a `.enc` extension.

- **Important:** Store the generated encryption key safely and add it to your `secrets.toml` file as shown above.

## Usage

- Run the Streamlit app:

  ```bash
  streamlit run app.py
  ```

- Open the provided local URL in your web browser.

- **How It Works:**

  1. **Select the IELTS Writing Task** (Task 1 Academic, Task 1 General Training, or Task 2).
  2. **Enter the Task Question** and **your response**.
  3. Click **"Evaluate Response"** to receive detailed feedback.
  4. **Review your feedback** and see what to improve!

- **Note:** This app is not affiliated with the official IELTS organization. It is designed as a supportive tool for self-evaluation and improvement.

## Directory Structure

```
├── .streamlit/
│   └── secrets.toml
├── modules/
│   ├── api_key_utils.py
│   ├── llm_pipeline.py
│   ├── markdown_to_docx.py
│   └── ui_components.py
├── tasks/
│   ├── encryptc.py
│   ├── Academic_IELTS_Writing_Task_1_Band_Descriptors.json.enc
│   ├── General_Training_IELTS_Writing_Task_1_Band_Descriptors.json.enc
│   └── IELTS_Writing_Task_2_Band_Descriptors.json.enc
├── app.py
└── requirements.txt
```

## Modules Overview

- **app.py**: The main Streamlit application file.
- **modules/**
  - **api_key_utils.py**: Utility functions for handling API keys.
  - **llm_pipeline.py**: Sets up the language model pipeline using LangChain and Google Generative AI.
  - **markdown_to_docx.py**: Converts markdown text to a DOCX file.
  - **ui_components.py**: Contains functions for displaying UI components in Streamlit.
- **tasks/**
  - **encryptc.py**: Script to encrypt the knowledge JSON files.
  - **[Encrypted JSON Files]**: Encrypted IELTS band descriptors used by the app.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

---

**Please Note**: This app is *not* affiliated with the official IELTS organization. It is designed as a supportive tool for self-evaluation and improvement.

