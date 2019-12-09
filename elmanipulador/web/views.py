from django.http import Http404
from django.shortcuts import render
from .models import Article


def home(request):
    articles = Article.objects.all()
    main_article = articles[0]
    return render(request, 'home.html', {
        'main': main_article,
        'articles': articles[1:]
    })

def article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'article.html', {'article': article})
