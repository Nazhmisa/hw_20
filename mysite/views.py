from django.views.generic import TemplateView
from datetime import datetime

class ShopIndexView(TemplateView):
    template_name = 'shopapp/shop-index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_running'] = datetime.now()
        context['products'] = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
            ('Tablet', 499),
            ('Watch', 299),
        ]
        return context