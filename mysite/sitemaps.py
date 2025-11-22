from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from shopapp.models import Product


class ShopSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Product.objects.filter(archived=False)


class SiteSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ["about-me"]

    def location(self, obj):
        return reverse(obj)


sitemaps = {
    "shop": ShopSitemap,
    "site": SiteSitemap,
}