import csv
from jobspy import scrape_jobs
import pandas as pd
import numpy as np
import fitz
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import streamlit as st
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from rapidfuzz import process, fuzz
import pyarrow.parquet as pq
from supabase import create_client, Client
from datetime import datetime
import os

SUPABASE_URL = "https://xzfvrjuxhacdytbvgkcg.supabase.co"
SUPABASE_KEY = os.getenv("key_supa")
TABLE_NAME = "carlos_linkedin_indeed"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# CLEAN FUNCTION
def clean_df(df):
    df = df[['title', 'company', 'location', 'emails', 'job_url', 'date_posted']]
    df = df.rename(columns={
        'title': 'titel',
        'company': 'opdrachtgever',
        'location': 'locatie',
        'emails': 'email',
        'job_url': 'link',
        'date_posted': 'datum_geplaatst'
    })
    return df[df['titel'].str.contains('data', case=False, na=False)]


# SCRAPE INDEED
jobs_indeed = scrape_jobs(
    site_name=["indeed"],
    search_term="data analytics, data science, data analyse, machine learning, data engineer, big data",
    location="Netherlands",
    results_wanted=2000,
    country_indeed="Netherlands"
)

df_indeed = clean_df(pd.DataFrame(jobs_indeed))


# SCRAPE LINKEDIN
jobs_linkedin = scrape_jobs(
    site_name=["linkedin"],
    search_term="data, data analytics, data science, data analyse, machine learning, data engineer, big data",
    location="Netherlands",
    results_wanted=2000,
    linkedin_fetch_description=True
)

df_linkedin = clean_df(pd.DataFrame(jobs_linkedin))


# COMBINE SCRAPED RESULTS
alles = pd.concat([df_indeed, df_linkedin], ignore_index=True)

# Zorg dat id NOOIT bestaat
if "id" in alles.columns:
    alles = alles.drop(columns=["id"])

# Convert date safely
alles["datum_geplaatst"] = pd.to_datetime(alles["datum_geplaatst"], errors="coerce")

def safe_date(x):
    if pd.isna(x):
        return None
    return x.strftime("%Y-%m-%d")

alles["datum_geplaatst"] = alles["datum_geplaatst"].apply(safe_date)

# Clean other values
alles = alles.replace([np.inf, -np.inf], None)
alles = alles.where(pd.notnull(alles), None)

# FETCH EXISTING DATA FROM SUPABASE
existing = supabase.table(TABLE_NAME).select("id, link").execute().data
existing_df = pd.DataFrame(existing) if existing else pd.DataFrame(columns=['id', 'link'])


# DETECT NEW AND EXPIRED
today_str = datetime.now().strftime("%Y-%m-%d")

scraped_links = set(alles["link"].tolist())
db_links = set(existing_df["link"].tolist())

new_links = scraped_links - db_links
expired_links = db_links - scraped_links

new_rows = alles[alles["link"].isin(new_links)]
expired_rows = existing_df[existing_df["link"].isin(expired_links)]


# INSERT NEW ROW
if len(new_rows) > 0:

    # CRUCIAL FIX AGAIN – drop id if present
    if "id" in new_rows.columns:
        new_rows = new_rows.drop(columns=["id"])

    records = new_rows.to_dict(orient="records")
    supabase.table(TABLE_NAME).insert(records).execute()

    print(f"➕ {len(new_rows)} nieuwe vacatures toegevoegd.")

else:
    print("ℹ️ Geen nieuwe vacatures gevonden.")

print("🏁 Klaar!")
