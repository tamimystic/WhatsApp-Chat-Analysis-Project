## App Live Link: https://tamimystic-whatsapp-chat-analyzer.streamlit.app/

# WhatsApp Chat Analyzer

A complete **Streamlit-based data analysis web application** that analyzes exported WhatsApp chat files and generates meaningful insights using data visualization and text analysis techniques.

---

## Overview

WhatsApp Chat Analyzer helps users understand communication patterns inside WhatsApp chats.  
It supports **group and individual chat analysis**, providing statistics, timelines, word usage, emoji usage, and activity heatmaps in an interactive web interface.

---

## Features

### Top Statistics
- Total number of messages
- Total number of words
- Total media shared
- Total links shared

---

### Timeline Analysis
- **Monthly Timeline** – Messages by month and year
- **Daily Timeline** – Messages sent per day

---

### Activity Analysis
- Most busy **day of the week**
- Most busy **month**
- **Weekly activity heatmap** (Day vs Hour message intensity)

---

### Text Analysis
- Word Cloud after removing stopwords and noise
- Most frequently used words

---

### Emoji Analysis
- Most commonly used emojis
- Emoji distribution using pie chart

---

### User Analysis (Group Chats Only)
- Most active users
- Percentage contribution of each user

---

## Technologies Used

- **Python**
- **Streamlit** – Web Application Framework
- **Pandas** – Data Manipulation & Analysis
- **Matplotlib** – Data Visualization
- **Seaborn** – Advanced Visualizations
- **WordCloud** – Word Cloud Generation
- **urlextract** – URL Extraction
- **emoji** – Emoji Detection & Analysis

---

## Input Requirements

- Export WhatsApp chat **without media**
- File format must be `.txt`
- Supported languages: English / Banglish

---

## How to Run the Project

### Clone the Repository
```bash
1. git clone https://github.com/tamimystic/WhatsApp-Chat-Analysis-Project.git
2. cd WhatsApp-Chat-Analyzer
3. pip install -r requirements.txt
4. streamlit run app.py

-------------------------------------------
Author
MD. Tamim Hossain
B.Sc in Computer Science & Engineering