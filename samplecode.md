```
from django.db.models import Q

def search_results(request):
    query = request.GET.get('query')  # Assuming the search query is passed as a GET parameter

    if query:
        search_terms = query.split()  # Splitting the query into individual search terms
        query_filters = Q()

        for term in search_terms:
            query_filters &= Q(field1__icontains=term) | Q(field2__icontains=term)

        queryset = YourModel.objects.filter(query_filters)

        # Additional filtering or sorting if needed
        # ...

        context = {
            'query': query,
            'results': queryset,
        }
        return render(request, 'search_results.html', context)

    return render(request, 'search.html')

```
