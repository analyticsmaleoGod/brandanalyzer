from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import pandas as pd
from apify_client import ApifyClient


class BaseScraper(ABC):
    """Base class for all platform scrapers."""

    platform_name: str = ""

    def __init__(self, apify_token: str):
        self.client = ApifyClient(apify_token)

    @abstractmethod
    def build_input(self, username: str, date_from: datetime, date_to: datetime) -> dict:
        """Build the Apify actor input payload."""
        pass

    @abstractmethod
    def get_actor_id(self) -> str:
        """Return the Apify actor ID for this platform."""
        pass

    @abstractmethod
    def parse_results(self, raw_items: list, date_from: datetime, date_to: datetime) -> list[dict]:
        """Parse raw Apify results into standardized format."""
        pass

    def scrape(
        self, username: str, date_from: datetime, date_to: datetime, progress_callback=None
    ) -> list[dict]:
        """Run the scraper and return standardized results."""
        actor_id = self.get_actor_id()
        actor_input = self.build_input(username, date_from, date_to)

        if progress_callback:
            progress_callback(f"Starting {self.platform_name} scraper for {username}...")

        try:
            run = self.client.actor(actor_id).call(run_input=actor_input)
            raw_items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())

            if progress_callback:
                progress_callback(f"Processing {len(raw_items)} items from {self.platform_name}...")

            parsed = self.parse_results(raw_items, date_from, date_to)
            return parsed

        except Exception as e:
            if progress_callback:
                progress_callback(f"Error on {self.platform_name}: {str(e)}")
            return []

    @staticmethod
    def safe_int(value, default=0) -> int:
        """Safely convert value to int."""
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def safe_date(value) -> Optional[datetime]:
        """Try to parse various date formats."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(str(value), fmt)
            except ValueError:
                continue
        return None

    @staticmethod
    def calc_engagement_rate(likes, comments, shares, followers=None, views=None) -> float:
        """Calculate engagement rate. Uses views if available, otherwise followers."""
        total_interactions = likes + comments + shares
        denominator = views if views and views > 0 else followers
        if denominator and denominator > 0:
            return round((total_interactions / denominator) * 100, 2)
        return 0.0

    @staticmethod
    def smart_limit(date_from, date_to) -> int:
        """Estimate posts to pull. Apify pulls newest first, so we need enough
        to reach back to date_from from today. ~2 posts/day + 30% buffer."""
        from datetime import datetime as _dt
        today = _dt.now()
        days_back = max((today - date_from).days, 1)
        estimate = int(days_back * 2 * 1.3)
        return max(30, min(estimate, 1000))
