
![MGB Logo](./images/transmart-logo.png)

# i2b2 tranSMART LLM Workshop: Using LLM to Search for Patient Notes

Welcome to the **i2b2 tranSMART LLM Workshop** repository. This project is part of a hands-on training module focused on **Large Language Models (LLMs)** and their application to clinical informatics and patient note analysis. You’ll work through Jupyter notebooks that demonstrate **Retrieval-Augmented Generation (RAG)**, semantic search, embeddings, and structured clinical summarization using local LLMs.

---

## ✅ Prerequisites

Please ensure the following are installed on your machine:

- **Python**: Version 3.12 or higher  
- **Visual Studio Code (VS Code)**  
- **Ollama CLI** (for local LLM inference)  

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/v-mourajr/i2b2-llm-workshop.git
cd i2b2-llm-workshop
````

### 2. Create and Activate a Virtual Environment

```bash

#Create the Environment on MacOS/Linux or Windows:
python3 -m venv i2b2_llm

# Activate On MacOS/Linux:
source i2b2_llm/bin/activate  

# Activate On Windows: 
.\i2b2_llm\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Model Setup with Ollama

We use **Qwen2**, a local open LLM, for this workshop.

### 1. Download and Install Ollama

* Visit [https://ollama.com/download](https://ollama.com/download)
* Choose your operating system and follow the installation steps
* After installation, open a terminal and verify:

```bash
ollama -v
```

### 2. Pull the Qwen2 Model

Run this command to download the model locally:

```bash
ollama pull qwen2
```

Once downloaded, the model can be used via LangChain using:

```python
from langchain_ollama import ChatOllama
model = ChatOllama(model="qwen2")
```

---

## 💻 Recommended Development Environment: Visual Studio Code

We recommend using [Visual Studio Code (VS Code)](https://code.visualstudio.com/) with the following extensions:

### 1. Install VS Code

* Download and install: [https://code.visualstudio.com/](https://code.visualstudio.com/)

### 2. Install Required Extensions

* Open VS Code
* Go to the **Extensions panel** (`Ctrl+Shift+X` or click the Extensions icon)
* Install:

  * **Python** (by Microsoft)
  * **Jupyter** (by Microsoft)

These enable full support for notebooks inside VS Code.

---

## ▶️ Running the Notebooks in VS Code

You’ll run all notebooks **inside VS Code**, not in your browser.

### 1. Open Visula Studio Code

### 2. Open a Notebook

* In VS Code, navigate to the desired `.ipynb` file (e.g., `1_chat_models_basic.ipynb`)
* Click to open it

### 3. Select Python Kernel

* At the top right of the notebook interface, select the Python interpreter from your virtual environment (e.g., `i2b2_llm`)

### 4. Run Cells

* Run individual cells with `Shift + Enter`, or click **Run All** in the top menu

---

## 📘 Notebooks Overview

### 1. `1_chat_models_basic.ipynb`

* **Learn the basics of chat-based LLMs** using system and user messages
* Includes structured prompts and inference using Qwen2 locally

### 2. `2_rag_embedding.ipynb`

* **Hands-on implementation of RAG** using FAISS and local embeddings
* Perform similarity search with score filtering

### 3. `3_rag_chromadb.ipynb`

* **Full RAG pipeline using ChromaDB** and Maximal Marginal Relevance (MMR)
* Structured summarization from retrieved notes using a local LLM

---

## 📜 License

Developed by the **Center for AI and Biomedical Informatics for the Learning Healthcare System (CAIBILS)** at Massachusetts General Brigham.

---

By following this guide, you’ll be ready to explore and apply cutting-edge LLM techniques to real-world patient notes using open tools and models.
**Let’s build smarter healthcare together.**


