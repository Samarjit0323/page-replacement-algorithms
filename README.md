# 📟 Virtual Memory Management: Page Replacement Simulator

An interactive, lightweight web application built with **Streamlit** to simulate and visualize Operating System page replacement algorithms. This tool provides a step-by-step vertical mapping of how an OS manages physical memory frames.



## 🚀 Features

* **Perfect Grid Visualization:** Custom CSS-aligned vertical grid showing exactly how pages occupy memory slots.
* **Three Core Algorithms:**
    * **FIFO (First-In, First-Out):** Replaces the oldest page in memory.
    * **LRU (Least Recently Used):** Replaces the page that hasn't been used for the longest time.
    * **Optimal:** The theoretical best algorithm; replaces the page that won't be used for the longest time in the future.
* **Live Metrics:** Real-time calculation of **Total Page Faults** and **Page Fault Rate** using native Streamlit metrics.
* **Dynamic Configuration:** Interactive sidebar to modify reference strings and frame counts (1-10 slots).
* **Color-Coded Feedback:**
    * 🟦 **Blue:** Current Input Page.
    * 🟥 **Red Border:** Page Fault (indicates the specific frame being replaced).
    * ⬜ **Gray:** Memory Hit (page already present in RAM).

## 🛠️ Tech Stack

* **Python 3.13**
* **Streamlit** (UI Framework)
* **Pandas** (Data Logic)
* **HTML5/CSS3** (Custom Grid Layout)

## 📥 Installation & Usage

1. **Fork the repo**
2. **Clone the project:**
   ```bash
   git clone "https://github.com/Samarjit0323/page-replacement-algorithms"
   cd page-replacement-algorithms
   
3. **Install Dependencies:**
    ```bash
    pip install requirements.txt

4. **Run the App:**
    ```bash
    streamlit run app.py
