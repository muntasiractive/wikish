![Wikish Banner](https://raw.githubusercontent.com/muntasiractive/wikish/main/docs/banner.png)

<div align="center">

# WikiSH 🌐
## Terminal Wikipedia Reader

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange.svg)

WikiSH is a powerful command-line interface (CLI) tool that lets you search and read Wikipedia articles directly from your terminal.  
It features a clean, rich interface and integrates with AI to provide concise summaries of long articles.

</div>

---

## ✨ Features

- 🔍 **Fast Search**: Instantly search Wikipedia for any topic.
- 📖 **Terminal Reader**: Read full Wikipedia articles with beautiful Markdown formatting and a pager for easy navigation.
- 🤖 **AI Summarization**: Generate 300-word summaries of any article using Llama 3 via Replicate.
- 🎨 **Rich UI**: Utilizes `rich` for a vibrant terminal experience with tables, panels, and colored output.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Replicate API Token](https://replicate.com/account/api-tokens) (optional, for summaries)

### Installation

#### 📦 Recommended: Using pipx
The easiest way to install WikiSH and have it work immediately is using `pipx`. This handles the system PATH automatically.

```bash
pipx install wikish
```

#### 🐍 Standard: Using pip
You can also install it directly from PyPI or GitHub:

```bash
# From PyPI
pip install wikish

# Or from GitHub
pip install git+https://github.com/yourusername/wikish.git
```

> [!IMPORTANT]
> **Windows Users**: If the `wikish` command is not recognized after installation, you likely need to add your Python Scripts folder to your system's PATH. 
> 
> 1. Run `pip show wikish` to find where it is installed.
> 2. Add the `Scripts` folder (e.g., `...\Python314\Scripts`) to your Environment Variables.
> 3. Restart your terminal.

---

## 🛠 Usage

Once installed, you can launch WikiSH from anywhere:

```bash
wikish
```

Or search for a specific topic directly:

```bash
wikish "Quantum Physics"
```

### ⌨️ Navigation

- **Article Selection**: Enter the index number from the search results to read an article.
- **Reading**: Use arrow keys or Space/PageDown to scroll. Press `q` to exit the pager.
- **Actions**:
  - `s`: Generate an AI summary.
  - `n`: Return to search results.
  - `q`: Quit the application.

---

## ⚙️ Configuration

Create a `.env` file in your project or set the environment variable:
```env
REPLICATE_API_TOKEN=your_token_here
```
*(Optional: Only needed for AI-powered summaries)*

---

## 📂 Project Structure

```text
wikish/
├── src/                # Source code
│   └── wikish/         # Core package
│       ├── ai.py
│       ├── cli.py
│       ├── models.py
│       ├── search.py
│       └── utils.py
├── main.py             # Entry point (for local dev)
├── pyproject.toml      # Build system and dependencies
├── .env                # Environment variables (secret)
└── requirements.txt    # legacy dependency list
```

## 📦 Dependencies

- `typer`: For CLI argument parsing.
- `rich`: For beautiful terminal formatting.
- `nlpia2-wikipedia`: For accessing Wikipedia content.
- `replicate`: For AI-powered summaries.
- `python-dotenv`: For managing environment variables.
- `mdv`: For terminal markdown viewing.

---

## 📝 License

This project is open-source and available under the MIT License.
