import pandas as pd
import logging
import re
from sqlalchemy import create_engine

class ReviewETLPipeline:
    def __init__(self, input_path, output_path, db_url):
        self.input_path = input_path
        self.output_path = output_path
        self.db_url = db_url
        self.df = None

    def setup_logging(self):
        logging.basicConfig(filename="review_etl.log", level=logging.INFO)

    def extract(self):
        logging.info("Extracting data...")
        self.df = pd.read_csv(self.input_path)

    def clean_text(self, text):
        if pd.isna(text):
            return ""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def transform(self):
        logging.info("Cleaning data...")
        self.df = self.df.dropna(subset=["review_text", "rating"])
        self.df["review_text"] = self.df["review_text"].apply(self.clean_text)
        self.df["review_date"] = pd.to_datetime(self.df["review_date"], errors="coerce")
        self.df = self.df[self.df["review_date"].notna()]
        self.df["review_length"] = self.df["review_text"].str.len()

    def load(self):
        logging.info("Saving to Parquet...")
        self.df.to_parquet(self.output_path, index=False)

        logging.info("Writing to database...")
        engine = create_engine(self.db_url)
        self.df.to_sql("product_reviews", engine, if_exists="replace", index=False)

    def run(self):
        try:
            self.setup_logging()
            logging.info("Pipeline started")
            self.extract()
            self.transform()
            self.load()
            logging.info("Pipeline completed successfully.")
        except Exception as e:
            logging.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    pipeline = ReviewETLPipeline(
        input_path="data/product_reviews.csv",
        output_path="cleaned_reviews.parquet",
        db_url="sqlite:///reviews.db"
    )
    pipeline.run()
