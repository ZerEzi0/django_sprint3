from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


NUMBER_OF_POSTS = 5


def filter_posts() -> QuerySet[Post]:
    """
    Возвращает QuerySet опубликованных постов,
    отфильтрованных по дате публикации и категории.
    :return: QuerySet опубликованных постов
    """
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает запрос на главную страницу блога.
    :param request: HttpRequest
    :return: HttpResponse с шаблоном главной страницы и списком постов
    """
    template = 'blog/index.html'
    post_list: QuerySet[Post] = filter_posts()[:NUMBER_OF_POSTS]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Обрабатывает запрос на страницу детального просмотра поста.
    :param request: HttpRequest
    :param post_id: ID поста
    :return: HttpResponse с шаблоном детального просмотра поста и самим постом
    """
    template = 'blog/detail.html'
    post: Post = get_object_or_404(filter_posts(), pk=post_id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """
    Обрабатывает запрос на страницу категории.
    :param request: HttpRequest
    :param category_slug: Slug категории
    :return: HttpResponse с шаблоном категории и списком постов в категории
    """
    template = 'blog/category.html'
    category: Category = get_object_or_404(
        Category, is_published=True, slug=category_slug
    )
    post_list: QuerySet[Post] = filter_posts().filter(category=category)
    context: dict[str, Category | QuerySet[Post]] = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
