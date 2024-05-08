# AI-Driven Early Detection System for Dyslexia and ADHD
This project primarily focuses on addressing the issue of early detection of learning disabilities in students, with a specific focus on dyslexia and attention deficit hyperactivity disorder (ADHD).

## Introduction

- This repository contains Python scripts for detecting signs of Dyslexia and ADHD using artificial intelligence (AI) and user activity monitoring.
- The Dyslexia detection script (`Dyselixa.py`) analyzes user-entered sentences for signs of Dyslexia, while the ADHD detection script (`hub.py`) monitors user activity such as keyboard presses and mouse movements to detect signs of ADHD.

### Warning!

Users should only run the hub.py script to run the ADHD system! The hub.py script is intended to launch and manage the ADHD.py script automatically. To ensure proper functionality and coordination between the two scripts, please run the hub.py script to start the ADHD analysis process and avoid running ADHD.py independently

## Motivation

Dyslexia and ADHD are neurodevelopmental disorders that can significantly impact an individual's academic and social functioning. Early detection is crucial for effective intervention and support. This project aims to contribute to early detection efforts by developing a data-driven approach using artificial intelligence.

## Features

- Dyslexia detection script analyzes user-entered sentences for signs of Dyslexia.
- ADHD detection script monitors user activity to detect signs of ADHD.
- Reports are generated in PDF format with analysis results.

## Usage

### Dyslexia Detection Script

1. Ensure you have Python installed on your system.
2. Run `Dyselixa.py`.
3. Follow the prompts to enter the patient's name, ID, and sentences for analysis.
4. View the generated PDF report for Dyslexia analysis results.

### ADHD Detection Script

1. Ensure you have Python installed on your system.
2. Run `hub.py`.
3. The script will start monitoring user activity for a specified duration.
4. View the generated PDF report for ADHD analysis results.

## Getting Started

### Prerequisites

- Python 3.x
- Python libraries: `nltk`, `tqdm`, `fuzzywuzzy`, `reportlab`, `pynput`, `matplotlib`, `webbrowser`, `time`, `sys` & `subprocess`

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/AFLucas-UOM/ARI2131-AI-Driven-Early-Detection-System-for-Dyslexia-and-ADHD.git
   ```
   
## Contributions

Contributions to improve the functionality or add new features are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was developed as part of an academic assignment, as part of the ARI2131 course at the University of Malta.

## Contact

For any inquiries or feedback, please contact [Andrea F. Lucas](mailto:andrealucasmalta@gmail.com).
