# AI-Powered Job Outreach Automation System

Production-ready modular outreach platform with Gmail sending, OpenAI personalization/classification, follow-up scheduling, reply intelligence, and Streamlit analytics.

## Architecture

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

## Features

- CSV lead ingestion into structured domain/DB entities.
- Personalized intro generation via OpenAI API.
- Jinja2 email templates for cold and follow-up messages.
- Gmail API OAuth2 integration for send + inbox sync.
- Follow-up logic after 3 days if no reply.
- Full event logging with statuses and metadata.
- Retry + rate limiting to improve reliability and avoid spam signals.
- Reply classification (`INTERESTED`, `NOT_INTERESTED`, `NEUTRAL`, `NEEDS_FOLLOWUP`).
- Metrics engine: response rate, conversion rate, follow-up effectiveness.
- Streamlit dashboard for live campaign analytics.

## Setup

1. Create Python 3.10+ virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment:
   ```bash
   cp .env.example .env
   ```
4. Add Gmail OAuth `credentials.json` downloaded from Google Cloud Console.
5. Update `.env` values.

## Gmail API notes

- Enable **Gmail API** in your Google Cloud project.
- Configure OAuth consent screen.
- Create OAuth client credentials for desktop app.
- First run will open browser auth flow and create `token.json`.

## Running pipelines

### Initial outreach send

```bash
python -m scripts.run_outreach
```

### Follow-up scheduler (3-day rule)

```bash
python -m scripts.run_followups
```

### Inbox sync + reply classification

```bash
python -m scripts.run_tracking_sync
```

Pipeline flow:

`Gmail Inbox → Reply Parser → OpenAI Classifier → Lead Status Update → Metrics`

## Streamlit dashboard

```bash
streamlit run app/dashboard/app.py
```

Dashboard includes:
- Total leads
- Emails sent
- Replies
- Response rate %
- Interested conversion %
- Follow-up effectiveness %
- Full lead table

## Example CSV format

`data/leads.csv`

```csv
name,email,company,role,tier,status
Alice Johnson,alice@example.com,Acme Inc,Backend Engineer,A,NOT_SENT
Bob Smith,bob@example.com,Globex,Data Engineer,B,NOT_SENT
```

## Extensibility

- Add providers in `ingestion/job_scraper.py`.
- Support HTML emails by extending `gmail_client.py` MIME construction.
- Replace SQLite with Postgres by changing `DATABASE_URL`.
- Add webhook/IMAP ingestion adapters inside `tracking/reply_parser.py`.
