from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import PortfolioItem, ScrapeTask
from .tasks import run_scrape_task

def index(request):
    # Show CV summary, capabilities, and portfolio items
    items = PortfolioItem.objects.order_by("-created_at")
    context = {
        "profile": {
            "name": "Your Name",
            "headline": "Senior Python Developer",
            "cv_url": "/static/your_cv.pdf",
            "services": ["Backend development", "Data engineering", "Automation", "Testing"],
            "core_capabilities": ["Python", "Django", "Flask", "AsyncIO", "Testing", "Docker"],
            "libraries": ["requests", "beautifulsoup4", "pandas", "sqlalchemy", "pytest"],
        },
        "portfolio_items": items,
    }
    return render(request, "portfolio/index.html", context)

def project_detail(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk)
    return render(request, "portfolio/detail.html", {"item": item})

def new_scrape(request):
    if request.method == "POST":
        url = request.POST.get("url")
        trigger = request.POST.get("triggered_by", "manual")
        task = ScrapeTask.objects.create(url=url, triggered_by=trigger)
        # pass GitHub token from env for higher rate limits if available
        from django.conf import settings
        github_token = getattr(settings, "GITHUB_TOKEN", None)
        run_scrape_task.delay(task.id, github_token=github_token)
        return redirect(reverse("portfolio:task_detail", args=[task.id]))
    return render(request, "portfolio/new_scrape.html")

def task_detail(request, pk):
    task = get_object_or_404(ScrapeTask, pk=pk)
    return render(request, "portfolio/task_detail.html", {"task": task})

def task_history(request):
    # Fetch all tasks, newest first
    tasks = ScrapeTask.objects.all().order_by('-created_at')
    return render(request, "portfolio/task_history.html", {"tasks": tasks})