from quotes.models import ServiceCategory

def service_categories(request):
    try:
        return {
            'service_categories': ServiceCategory.objects.all()
        }
    except Exception:
        # Return empty queryset if table doesn't exist or other database error
        return {
            'service_categories': []
        }