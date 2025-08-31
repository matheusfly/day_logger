# Daily Task Journal

A Python-based desktop application for tracking and managing daily tasks and activities with time blocks.

## 🌟 Features

- **Intuitive GUI Interface** - Built with Tkinter for a clean, dark-themed user experience
- **Time Block Management** - Organize tasks into Morning, Mid-day, and Evening blocks
- **Time Tracking** - Record start and end times for each activity block
- **Data Persistence** - Automatically saves entries in organized daily, weekly, and monthly logs
- **Dark Mode** - Eye-friendly dark theme for comfortable use

## 📋 Requirements

- Python >= 3.12
- Dependencies:
  - python-dateutil >= 2.8.3
  - dataclasses >= 0.6
  - pathlib >= 1.1.0
  - pydantic >= 2.2.0
  - jsonschema >= 4.16.0

## 🚀 Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Or use Poetry:
```bash
poetry install
```

## 💻 Usage

Run the application:
```bash
python task_journal.py
```

The interface provides three main time blocks:
- 🌅 Morning Tasks
- ☀️ Mid-day Tasks
- 🌙 Evening Tasks

For each block:
1. Enter the start and end times
2. Add your tasks in the text area
3. Click "💾 Save Journal" to store your entries
4. Use "🗑️ Clear All" to reset the form

## 📁 Project Structure

```
.
├── task_journal.py          # Main GUI application
├── journal_processor.py     # Core processing logic
├── pyproject.toml          # Project configuration
├── requirements.txt        # Dependencies
└── day_logger/            
    ├── journal_data_manager.py
    ├── models/
    │   └── timeblock.py    # TimeBlock data model
    ├── processors/
    │   └── data_processor.py
    └── utils/
        ├── formatters.py
        └── helpers.py
```

## 💾 Data Storage

Journal entries are stored in the `work-logs` directory with the following structure:
```
work-logs/
├── YYYY/
    ├── daily/    # Daily journal entries
    ├── weekly/   # Weekly summaries
    └── monthly/  # Monthly reports
```

## 🧪 Testing

Run tests using pytest:
```bash
pytest
```

Test coverage includes:
- Journal data management
- TimeBlock model functionality
- Main application features

## 🛠️ Development

The project uses:
- Poetry for dependency management
- Pytest for testing
- Type hints for better code reliability
- Modern Python features (Python 3.12+)

## 📝 License

This project is licensed under the terms of the MIT license.
