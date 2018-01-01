from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from crawler.models import news


def get_list_by_page(request):
    news_list=news.objects.order_by('-createTime')
    paginator=Paginator(news_list,15)

    page=request.GET.get('page')
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)

    return result