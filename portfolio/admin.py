from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PortfolioItem, ScrapeTask

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "github_url", "created_at")
    search_fields = ("title", "github_url")

@admin.register(ScrapeTask)
class ScrapeTaskAdmin(admin.ModelAdmin):
    list_display = ("url", "status", "created_at")
    readonly_fields = ("started_at", "finished_at", "result", "error")