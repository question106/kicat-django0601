from django.db import connection
from django.db.utils import ProgrammingError

def service_categories(request):
    try:
        # Check if the table exists first
        from quotes.models import ServiceCategory
        
        # Test if we can query the table
        categories = ServiceCategory.objects.all()
        return {
            'service_categories': categories
        }
    except (ProgrammingError, Exception) as e:
        # Table doesn't exist, is empty, or other database error
        # This prevents 500 errors during migrations or with empty DB
        return {
            'service_categories': []
        }