![MGB Logo](./images/mgb-logo.png)

# CAIBILS Mongan LLM Workshop

Welcome to the CAIBILS Mongan LLM Workshop repository. This project is part of a training module focused on large language models (LLMs) and their applications. The core components of this repository are Jupyter notebooks designed to guide users through various concepts and practical implementations.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python**: Version 3.12 or higher.
- **Azure CLI**: Required for authentication with Azure services.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/v-mourajr/mongan_llm_workshop.git
   cd mongan_llm_workshop
   ```

2. **Install Dependencies**:
   It's recommended to use a virtual environment to manage dependencies:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Azure Authentication**:
   Log in to your Azure account:
   ```bash
   az login
   ```
   This command will open a browser window for authentication. Ensure you have the necessary permissions to access the required Azure resources.

4. **Environment Variables**:
   Copy the example environment file and update it with your configurations:
   ```bash
   cp .env_example .env
   ```
   Edit the `.env` file to include your specific settings.

## Jupyter Notebooks Overview

The primary content of this repository consists of the following Jupyter notebooks:

1. **1_chat_models_basic.ipynb**:
   - *Description*: Introduces basic concepts of chat models, including setup and simple interactions.
   - *Key Topics*:
     - Overview of chat models.
     - Setting up a chat model environment.
     - Basic usage examples.

2. **2_rag_embedding.ipynb**:
   - *Description*: Explores Retrieval-Augmented Generation (RAG) and embedding techniques.
   - *Key Topics*:
     - Introduction to RAG.
     - Understanding embeddings.
     - Implementing RAG with embedding models.

## Recommended Development Environment

For an optimal experience, we recommend using [Visual Studio Code (VS Code)](https://code.visualstudio.com/) with the following extensions:

- **Python Extension**: Provides rich support for Python, including IntelliSense and debugging.
  - *Installation*:
    1. Open VS Code.
    2. Navigate to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or by pressing `Ctrl+Shift+X`.
    3. Search for "Python" and install the extension published by Microsoft.

- **Jupyter Extension**: Enables support for Jupyter notebooks within VS Code.
  - *Installation*:
    1. After installing the Python extension, search for "Jupyter" in the Extensions view.
    2. Install the extension published by Microsoft.

These extensions enhance the development experience by providing features like code completion, interactive debugging, and seamless notebook integration.

## Running the Notebooks

To execute the Jupyter notebooks:

1. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```
   This command will open the Jupyter Notebook interface in your default web browser.

2. **Open a Notebook**:
   In the Jupyter interface, navigate to the desired notebook (e.g., `1_chat_models_basic.ipynb`) and click to open it.

3. **Run Cells**:
   Execute the code cells sequentially by selecting each cell and clicking the "Run" button or by pressing `Shift + Enter`.

## Contributing

Contributions to this project are welcome. If you have suggestions for improvements or encounter any issues, please open an issue or submit a pull request.

## License

Developed by the Center for AI and Biomedical Informatics of the Learning Healthcare System (CAIBILS). 

---

By following this guide, you should be well-equipped to explore and utilize the resources provided in the Mongan LLM Workshop repository. Happy coding! 