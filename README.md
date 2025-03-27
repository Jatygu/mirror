# 🪞 Mirror.py

**A personal reflection and data visualization tool for ChatGPT users.**  
Organize, rediscover, and interact with your past conversations using keyword analysis, topic clustering, and rich terminal visuals.

---

## 🌟 What It Does

Mirror.py helps you make sense of your ChatGPT history — the ideas, inspirations, routines, and reflections you've accumulated over time.  
It reads your exported `.json` file and gives you a colorful, interactive summary right in your terminal.

---

## 🧠 Features

- 📊 **Top Keywords** — See the most common words from all your conversation titles
- 🗂️ **Topic Clustering** — Automatically groups your chats into categories like:
  - Music & Licensing
  - Career & Jobs
  - Automation & AI
  - Creative Flow
  - Inner Alignment
- 🔁 **Repetition Detection** — Find conversations you’ve started more than once
- 🎁 **Joy of Rediscovery** — Suggests old gems you may have forgotten
- 🔍 **Search Tool** — Quickly look up conversations using any word or phrase
- 🎨 **Rich Visual Layout** — Uses the `rich` Python library to display a dashboard-like layout with panels and colors

---

## 🛠️ How to Use It

### 1. Export Your ChatGPT Data
- Go to [chat.com](https://chat.com)
- Settings → Data Controls → Export data → Download the `.zip`
- Extract the `conversations.json` file

### 2. Run Mirror.py

```bash
python Mirror.py
