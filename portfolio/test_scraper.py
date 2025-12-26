from django.test import TestCase
from portfolio.scrapers import fetch_github_repo_metadata

class ScraperTests(TestCase):
    def test_fetch_github_repo_metadata(self):
        # Use a known public repo (note: rate limits apply)
        meta = fetch_github_repo_metadata("psf", "requests", token=None)
        self.assertIn("full_name", meta)
        self.assertEqual(meta["full_name"].lower(), "psf/requests")
        self.assertIsInstance(meta["stars"], int)