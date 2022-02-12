from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank, SearchVector
from django.shortcuts import render
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .forms import SearchForm
from .models import Document


def search(request):
    results = None

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            vector = SearchVector('url', 'title', 'content')
            query = SearchQuery(form.cleaned_data['search'])

            START_SEL = '&#"_&'
            STOP_SEL = '&_"#&'
            results = Document.objects.annotate(
                rank=SearchRank(vector, query, cover_density=True),
                headline=SearchHeadline('content', query, start_sel=START_SEL, stop_sel=STOP_SEL)
            ).exclude(rank__lte=0.01).order_by('-rank')

            for res in results:
                entries = res.headline.split(START_SEL)
                h = []
                for i, entry in enumerate(entries):
                    if i != 0:
                        h.append(mark_safe('<b>'))

                    if STOP_SEL in entry:
                        a, b = entry.split(STOP_SEL, 1)
                        h.append(a)
                        h.append(mark_safe('</b>'))
                        h.append(b)
                    else:
                        h.append(entry)
                res.headline = h
    else:
        form = SearchForm()

    context = {
        'form': form,
        'results': results
    }
    return render(request, 'se/index.html', context)
