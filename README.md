# TaskMaster

A minimalist, high-performance, and dependency-free desktop To-Do List application built with pure Python and Tkinter. TaskMaster implements a structured Model-View-Controller (MVC) architecture to ensure responsive states, safe local asset handling, and seamless workflow organization.

![TaskMaster Window Placeholder](https://via.placeholder.com/900x600?text=TaskMaster+Desktop+UI+Layout)

## 🚀 Key Features

* **Complete Task Life-Cycle:** Instantly create, edit, update, or permanently delete tasks.
* **Persistent Storage:** Fully automated JSON storage serialization targeted directly at `data/tasks.json`.
* **Zero Dependencies:** Engineered using Python 3 built-in frameworks (`tkinter`, `json`, `datetime`). No complex initialization or external pip environments needed.
* **Smart Filter & Query:** Instantly lookup items using the real-time title/description keyword search index or isolate pending vs. completed workflows.
* **Automated Data Backups:** Secures active records inside timestamped backups (`data/backups/`) after every modification, keeping up to 5 history slots to eliminate risks of data corruption.

## 🛠 Project Structure

```text
TaskMaster/
│
├── data/
│   ├── tasks.json             # Live database persistence
│   └── backups/               # Automated timestamped fallback trees
│
├── edit_window.py             # Sub-View UI module
├── main.py                    # Root Window View & App Controller
├── task_manager.py            # Object Model & State Serialization Engine
├── requirements.txt           # Standard ecosystem definitions
└── index.html                 # Academic Showcase Platform (GitHub Pages)