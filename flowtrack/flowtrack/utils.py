from django.core.paginator import Paginator


def paginObjects(request, objects, count, page_key="page"):
    paginator = Paginator(objects, count)
    page_number = request.GET.get(page_key, 1)
    objects = paginator.get_page(page_number)

    start_page = max(objects.number - 2, 1)
    end_page = min(objects.number + 2, paginator.num_pages)
    if objects.number <= 2 and paginator.num_pages >= 5:
        page_range = range(1, 6)
    else:
        page_range = range(start_page, end_page + 1)

    return objects, page_range
