"""Streamlit dashboard for outreach monitoring."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.database import crud
from app.database.db import get_session, init_db
from app.tracking.metrics import calculate_metrics

st.set_page_config(page_title="AI Outreach Dashboard", layout="wide")
st.title("📬 AI Outreach Intelligence Dashboard")

init_db()
with get_session() as session:
    leads = crud.list_leads(session)

metrics = calculate_metrics(leads)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Leads", int(metrics["total_leads"]))
c2.metric("Emails Sent", int(metrics["emails_sent"]))
c3.metric("Replies", int(metrics["replies"]))
c4.metric("Response Rate", f"{metrics['response_rate']:.2f}%")
c5.metric("Interested Conversion", f"{metrics['conversion_rate']:.2f}%")

st.divider()
left, right = st.columns(2)
left.metric("Follow-up Effectiveness", f"{metrics['followup_effectiveness']:.2f}%")
right.metric("Interested Leads", int(metrics["interested"]))

st.subheader("Lead Table")
if leads:
    df = pd.DataFrame([lead.__dict__ for lead in leads])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No leads found. Run ingestion/outreach first.")
