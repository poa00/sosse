from collections import OrderedDict
import json
from urllib.parse import urlparse, parse_qs, quote_plus

from django.conf import settings
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .forms import SearchForm
from .models import Document, FavIcon, SearchEngine, SearchHistory, remove_accent
from .search import add_headlines, get_documents


def human_nb(nb):
    unit = ('', 'k', 'M', 'G', 'T', 'P')
    unit_no = 0

    while nb > 1000:
        nb /= 1000
        unit_no += 1
    return '%i%s' % (nb, unit[unit_no])


def format_url(request, params):
    parsed_url = urlparse(request.get_full_path())
    query_string = parse_qs(parsed_url.query)
    for k, v in query_string.items():
        query_string[k] = v[0]

    for param in params.split('&'):
        val = None
        if '=' in param:
            key, val = param.split('=', 1)
        else:
            key = param

        if val:
            query_string[key] = val
        else:
            query_string.pop(key, None)

    qs = '&'.join([f'{k}={v}' for k, v in query_string.items()])
    return parsed_url._replace(query=qs).geturl()


def get_pagination(request, paginated):
    context = {}
    if paginated and paginated.has_previous():
        context.update({
            'page_first': format_url(request, 'p='),
            'page_previous': format_url(request, 'p=%i' % paginated.previous_page_number()),
        })
    if paginated and paginated.has_next():
        context.update({
            'page_next': format_url(request, 'p=%i' % paginated.next_page_number()),
            'page_last': format_url(request, 'p=%i' % paginated.paginator.num_pages)
        })
    return context


def get_context(ctx):
    ctx.update({
        'settings': settings,
    })
    return ctx


def search(request):
    results = None
    paginated = None
    q = None

    form = SearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data['q']
        redirect_url = SearchEngine.should_redirect(q)
        SearchHistory.save_history(request, q)

        if redirect_url:
            return redirect(redirect_url)

        has_query, results, query = get_documents(request, form)
        paginator = Paginator(results, form.cleaned_data['ps'])
        page_number = request.GET.get('p')
        paginated = paginator.get_page(page_number)
        paginated = add_headlines(paginated, query)
    else:
        form = SearchForm()

    sosse_langdetect_to_postgres = OrderedDict()
    for key, val in sorted(settings.SOSSE_LANGDETECT_TO_POSTGRES.items(), key=lambda x: x[1]['name']):
        if not Document.objects.filter(lang_iso_639_1=key).exists():
            continue
        sosse_langdetect_to_postgres[key] = val

    for r in paginated:
        if form.cleaned_data['c']:
            r.link = r.get_absolute_url()
            r.extra_link = r.url
        else:
            r.link = r.url
            r.extra_link = r.get_absolute_url()

    extra_link_txt = 'cached'
    if form.cleaned_data['c']:
        extra_link_txt = 'source'

    context = get_context({
        'hide_title': True,
        'form': form,
        'results': results,
        'results_count': human_nb(len(results)),
        'paginated': paginated,
        'has_query': has_query,
        'q': q,
        'title': q,
        'sosse_langdetect_to_postgres': sosse_langdetect_to_postgres,
        'extra_link_txt': extra_link_txt
    })
    context.update(get_pagination(request, paginated))
    return render(request, 'se/index.html', context)


def word_stats(request):
    results = None
    form = SearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data['q']
        q = remove_accent(q)
        _, doc_query, _ = get_documents(request, form, True)
        doc_query = doc_query.values('vector')

        # Hack to obtain final SQL query, as described there:
        # https://code.djangoproject.com/ticket/17741#comment:4
        sql, params = doc_query.query.sql_with_params()
        cursor = connection.cursor()
        cursor.execute('EXPLAIN ' + sql, params)
        raw_query = cursor.db.ops.last_executed_query(cursor, sql, params)
        raw_query = raw_query[len('EXPLAIN '):]

        results = Document.objects.raw('SELECT 1 AS id, word, ndoc FROM ts_stat(%s) ORDER BY ndoc DESC, word ASC LIMIT 100', (raw_query,))
        results = [(e.word, human_nb(e.ndoc), format_url(request, 'q=%s %s' % (q, e.word))[len('/word_stats'):]) for e in list(results)]
        results = json.dumps(results)

    return HttpResponse(results, content_type='application/json')


def prefs(request):
    supported_langs = json.dumps(Document.get_supported_lang_dict())
    context = get_context({
        'title': 'Preferences',
        'supported_langs': supported_langs
    })
    return render(request, 'se/prefs.html', context)


def favicon(request, favicon_id):
    fav = get_object_or_404(FavIcon, id=favicon_id)
    return HttpResponse(fav.content, content_type=fav.mimetype)


def history(request):
    page_size = int(request.GET.get('ps', settings.SOSSE_DEFAULT_PAGE_SIZE))
    page_size = min(page_size, settings.SOSSE_MAX_PAGE_SIZE)

    history = SearchHistory.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(history, page_size)
    page_number = int(request.GET.get('p', 1))
    paginated = paginator.get_page(page_number)

    context = {
        'title': 'Search history',
        'paginated': paginated
    }
    context.update(get_pagination(request, paginated))
    return render(request, 'se/history.html', context)


def opensearch(request):
    context = {
        'url': request.build_absolute_uri('/').rstrip('/')
    }
    return render(request, 'se/opensearch.xml', context, content_type='application/xml')


def search_redirect(request):
    context = {
        'url': request.build_absolute_uri('/'),
        'q': quote_plus(request.GET.get('q', ''))
    }
    return render(request, 'se/search_redirect.html', context)


class SELoginView(LoginView):
    template_name = 'admin/login.html'
