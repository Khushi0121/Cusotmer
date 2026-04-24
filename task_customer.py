import pandas as pd
import re
from collections import Counter
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


df_global = None



def clean_text(text):
    text = str(text)

    text = re.sub(r"<.*?>", " ", text)
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


def classify_ticket(text):
    text = text.lower()

    if any(word in text for word in ["failed", "error", "bad", "delayed", "refund"]):
        return "Complaint"

    if any(word in text for word in ["need", "want", "reset"]):
        return "Request"

    if any(word in text for word in ["how", "what", "know"]):
        return "Query"

    return "Other"



def process_file(file_path="customer.csv"):
    global df_global

 
    df = pd.read_csv(file_path, on_bad_lines="skip")
    total_records = len(df)


    df = df.dropna(subset=["text", "customer_id"])


    df = df[df["text"].astype(str).str.strip() != ""]


    df["text"] = df["text"].apply(clean_text)


    df["category"] = df["text"].apply(classify_ticket)

    processed_records = len(df)
    failed_records = total_records - processed_records

    
    df_global = df

   
    df.to_csv("cleaned_customer.csv", index=False)

    logging.info(f"Processed: {processed_records}, Failed: {failed_records}")
    logging.info("Saved cleaned data to cleaned_customer.csv")

    return processed_records, failed_records


def get_stats():
    if df_global is None:
        return {"error": "Run /ingest first"}

    category_counts = df_global["category"].value_counts().to_dict()


    all_text = " ".join(df_global["text"])
    words = all_text.split()


    stopwords = {
        "the", "is", "and", "to", "my", "i", "for", "of", "a", "in",
        "need", "help", "want", "know"
    }

    filtered_words = [word for word in words if word not in stopwords]


    word_freq = Counter(filtered_words)
    top_keywords = [word for word, _ in word_freq.most_common(5)]

    return {
        "total_records": len(df_global),
        "category_distribution": category_counts,
        "top_keywords": top_keywords
    }


def search_tickets(query):
    if df_global is None:
        return {"error": "Run /ingest first"}

    results = df_global[df_global["text"].str.contains(query, case=False)]

    return results[["ticket_id", "text", "category"]].to_dict(orient="records")



def filter_category(category):
    if df_global is None:
        return {"error": "Run /ingest first"}

    results = df_global[df_global["category"] == category]

    return results[["ticket_id", "text", "category"]].to_dict(orient="records")


def summarize_complaints():
    if df_global is None:
        return {"error": "Run /ingest first"}

    complaints = df_global[df_global["category"] == "Complaint"]["text"]

    summary = []

    if any("payment" in text for text in complaints):
        summary.append("Multiple users reported payment failures")

    if any("refund" in text for text in complaints):
        summary.append("Refund delays are common")

    if any("delayed" in text or "bad" in text for text in complaints):
        summary.append("Users unhappy with response time")

    return {"summary": summary}