from fastapi import FastAPI
import logging

from task_customer import (
    process_file,
    get_stats,
    search_tickets,
    filter_category,
    summarize_complaints
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()
@app.post("/ingest")
def ingest():
    file_path = "customer.csv"

    logger.info(f"Starting ingestion from file: {file_path}")

    processed, failed = process_file(file_path)

    logger.info(f"Ingest complete → processed: {processed}, failed: {failed}")

    return {
        "message": "Data ingested successfully",
        "records_processed": processed,
        "records_failed": failed
    }

@app.get("/stats")
def stats():
    logger.info("Stats endpoint called")
    return get_stats()

@app.get("/search")
def search(q: str):
    logger.info(f"Search query: {q}")
    return search_tickets(q)
-
@app.get("/category/{category}")
def category(category: str):
    logger.info(f"Filter category: {category}")
    return filter_category(category)

@app.get("/summary")
def summary():
    logger.info("Summary requested")
    return summarize_complaints()