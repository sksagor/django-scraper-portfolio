from celery import shared_task
from django.utils import timezone
from .models import ScrapeTask, PortfolioItem
from .scrapers import fetch_github_repo_metadata
from urllib.parse import urlparse

@shared_task(bind=True)
def run_scrape_task(self, scrape_task_id, github_token=None):
    task = ScrapeTask.objects.get(pk=scrape_task_id)
    try:
        task.mark_running()
        # Simple URL parsing to detect GitHub repo
        parsed = urlparse(task.url)
        if "github.com" in parsed.netloc:
            parts = parsed.path.strip("/").split("/")
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                meta = fetch_github_repo_metadata(owner, repo, token=github_token)
                task.result = meta
                # Optionally, upsert a PortfolioItem
                pi, created = PortfolioItem.objects.update_or_create(
                    github_url=meta["html_url"],
                    defaults={
                        "title": meta["full_name"],
                        "short_description": meta["description"] or "",
                        "extra_data": meta
                    }
                )
                task.status = "SUCCESS"
            else:
                task.status = "FAILED"
                task.error = "Invalid GitHub URL format"
        else:
            # Fallback: minimal GET + parse title/meta (not implemented here)
            task.status = "FAILED"
            task.error = "Non-GitHub scraping not supported yet"
    except Exception as e:
        task.status = "FAILED"
        task.error = str(e)
    finally:
        task.finished_at = timezone.now()
        task.save()