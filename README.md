# 🛡️ GitHub Dependency Auditor & Security Scanner

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Security](https://img.shields.io/badge/Security-Safety_Check-red.svg)
![Parser](https://img.shields.io/badge/Parser-AST_Analysis-green.svg)

## 🚀 Project Overview

This tool is a comprehensive **automated dependency auditor** designed for Python projects. It programmatically clones any public GitHub repository, performs static code analysis to extract imported libraries, and immediately scans those dependencies for known security vulnerabilities (CVEs).

Unlike simple text scanners, this engine utilizes Python's **Abstract Syntax Tree (AST)** module to accurately parse code structure, ensuring that only actual imports are detected, avoiding false positives from comments or docstrings.

## ⚡ Key Features

* **📥 Automated Cloning:** Handles temporary repository downloading and cleanup via `GitPython`.
* **🧠 Advanced Static Analysis:** Uses `ast` parsing to identify both direct (`import x`) and specific (`from x import y`) imports, ensuring high precision compared to Regex solutions.
* **🔒 Integrated Security Pipeline:** Automatically generates a `requirements.txt` and runs a **Safety Check** to flag vulnerable packages against known security databases.
* **⏱️ Performance Benchmarking:** Tracks and reports execution time for the analysis phase.
* **🧹 Smart Cleanup:** Automatically removes temporary files and directories post-analysis to keep the workspace clean.

## 🛠️ How It Works

The script executes a 5-step pipeline:

1.  **Clone:** Fetches the target source code from GitHub.
2.  **Walk & Parse:** Recursively iterates through all `.py` files.
3.  **Extract:** parses the code into an AST to identify import nodes. 
4.  **Generate:** Compiles a sorted list of unique libraries into `requirements.txt`.
5.  **Audit:** Cross-references the list with the Safety DB for security flaws.

## 📂 Project Structure

```text
PythonProject2/
│
├── proiectgithub.py       # 🧠 Main Engine (Analysis & Security Logic)
├── requirements.txt       # 📄 Dependencies required to run this tool
└── README.md              # 📖 Project Documentation
💻 Installation & Usage
1. Prerequisites
Ensure you have the necessary libraries installed (GitPython and safety).

Bash
git clone [https://github.com/your-username/PythonProject2.git](https://github.com/your-username/PythonProject2.git)
cd PythonProject2
pip install -r requirements.txt
(Note: The requirements.txt for this tool must include GitPython and safety)

2. Running the Tool
Execute the script by passing the target GitHub URL as an argument:

Bash
python proiectgithub.py [https://github.com/target-user/target-repo.git](https://github.com/target-user/target-repo.git)
📊 Sample Output
Plaintext
Downloading repository from [https://github.com/test/repo](https://github.com/test/repo)...
Repository downloaded successfully.

Analyzing imported libraries...
Time elapsed for analysis: 0.45 seconds

Imported Libraries:
flask
numpy
pandas
requests

Generating requirements.txt...
Checking for known security vulnerabilities...

No security issues found.
Cleaning up downloaded repository...
Cleanup successful.
🧩 Technologies Used
Python 3 - Core logic.

AST (Abstract Syntax Tree) - For high-precision source code parsing.

GitPython - For programmatic git operations.

Safety - For vulnerability scanning and compliance checking.

OS & Shutil - For file system manipulation.

👨‍💻 Author
Developed by Paul Nicolae Nicoara.
