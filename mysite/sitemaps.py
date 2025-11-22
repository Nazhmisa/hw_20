
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from shopapp.models import Product

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['shopapp:shop_index']  

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(archived=False)

    def lastmod(self, obj: Product):
        return obj.created_at

sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
}