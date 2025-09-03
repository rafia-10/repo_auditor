# Repo Auditor – GitHub Secret Scanner with LangChain

Repo Auditor is a Python tool that helps you audit GitHub repositories for accidentally committed secrets, like API keys, database passwords, and other sensitive information in .env files.

This project demonstrates custom LangChain tools integrated with a Groq-powered LLM to automate multi-step security checks.

## Features

Download GitHub repositories programmatically.

Scan for .env files and detect potentially sensitive entries.

Fully modular custom tools using LangChain.

Secure secret management via .env files.

## Requirements

All dependencies are already listed in requirements.txt.

If you haven’t installed them yet:

python -m pip install -r requirements.txt

## Setup

### Create conda environment
    conda create -n repo_auditor python=3.11 -y
    conda activate repo_auditor

### Install dependencies
    python -m pip install -r requirements.txt
    
### Add secrets
Create a .env file in the project root:

    GROQ_API_KEY=your_groq_key_here
    GITHUB_TOKEN=your_github_token_here
#### Important: .env is ignored by git to prevent exposing secrets.

## Usage

Run the main script:
  python3 main.py
  
Provide a GitHub repo URL via user input.

The tool will download the repository, scan for .env files, and report any sensitive entries.

## Notes

Built with LangChain for custom tool orchestration.

Tested with Python 3.11, langchain-groq 0.3.7, groq 0.31.0.

Ensure no extra spaces or invisible characters in your .env to avoid Groq 401 errors.


Name: Rafia Kedir
Email: rafiakedir22@gmail.com
