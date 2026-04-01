# 🚀 AI-Powered Job Outreach Automation System

An end-to-end intelligent system that automates job outreach using AI; from lead generation to personalized emails, reply classification, and performance analytics.

---

## 🎯 Problem

Applying to jobs manually is:
- Time-consuming  
- Repetitive  
- Inefficient (low response rates)  

Most candidates send generic applications with no tracking or feedback loop.

---

## 💡 Solution

This system acts as an **AI job outreach engine** that:

✅ Generates personalized cold emails using LLMs  
✅ Sends emails via Gmail API  
✅ Tracks recruiter responses  
✅ Classifies replies (Interested / Not Interested / Follow-up)  
✅ Automates follow-ups  
✅ Displays performance metrics via dashboard  

---

## 🧠 Key Features

### 🔹 AI Personalization Engine
- Uses LLMs to generate customized email intros
- Tailors outreach based on company + role

### 🔹 Automated Email Pipeline
- Gmail API integration (OAuth2)
- Rate limiting + retry logic
- Template-based email generation

### 🔹 Reply Intelligence System
- Fetches recruiter replies from inbox
- Classifies responses using AI:
  - INTERESTED
  - NOT_INTERESTED
  - NEUTRAL
  - NEEDS_FOLLOWUP

### 🔹 Follow-up Automation
- Sends follow-ups after 3 days if no response
- Stops outreach if negative response detected

### 🔹 Analytics Dashboard (Streamlit)
- Total leads
- Emails sent
- Replies received
- Response rate %
- Conversion rate %

---

## 🏗️ Architecture


```text
app/
├── main.py
├── config.py
├── constants.py
├── database/
│   ├── db.py
│   ├── models.py
│   └── crud.py
├── ingestion/
│   ├── csv_loader.py
│   └── job_scraper.py
├── personalization/
│   ├── llm_engine.py
│   └── prompt_templates.py
├── email/
│   ├── email_service.py
│   ├── gmail_client.py
│   └── templates/
├── scheduler/
│   └── followup_scheduler.py
├── tracking/
│   ├── tracker.py
│   ├── reply_parser.py
│   ├── classifier.py
│   ├── metrics.py
│   └── analytics.py
├── dashboard/
│   └── app.py
└── utils/
    ├── logger.py
    ├── helpers.py
    └── resilience.py
```


Leads → Personalization → Email Sending → Inbox Sync
↓
Reply Classification
↓
Metrics Engine
↓
Streamlit Dashboard


---

## 🧰 Tech Stack

- **Backend:** Python  
- **AI:** OpenAI API  
- **Email:** Gmail API (OAuth2)  
- **Dashboard:** Streamlit  
- **Data:** CSV / SQLite  
- **Automation:** Cron / Scheduler  

---

## ⚙️ Installation

```bash
git clone https://github.com/guna-thota/AI-powered-job-outreach-automation-system.git
cd AI-powered-job-outreach-automation-system
pip install -r requirements.txt
🔐 Setup

Create .env file:

OPENAI_API_KEY=your_key
SENDER_EMAIL=your_email

Set up Gmail API:

Enable Gmail API
Download credentials
Generate token.json
▶️ Usage
1. Run Outreach
python scripts/run_outreach.py
2. Process Replies
python scripts/run_followups.py
3. Launch Dashboard
streamlit run app/dashboard/app.py
📊 Example Output
Personalized email generation
Automated follow-ups
Response tracking dashboard
```
---

##🚀 Future Improvements


-LinkedIn automation
-Resume-job matching engine
-Auto-reply generation
-Multi-account scaling

---

##💼 Why This Project Matters

-This project simulates a real-world SaaS system for job automation:
-Combines AI + backend + APIs
-Implements full pipeline (not just scripts)
-Demonstrates system design + scalability

---

##👨‍💻 Author

Guna Durga Prashanth Thota --
Data Engineer 

---


