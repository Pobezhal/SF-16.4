from celery import shared_task
import time
from celery import shared_task
from .models import User, Post, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import date, timedelta


@shared_task
def send_mail_news():
    pass
#Реализовать рассылку уведомлений подписчикам после создания новости пока не удается. Надо думать еще неделю.


@shared_task
def week_notify():

    start = date.today() - timedelta(7)
    finish = date.today()
    categories = Category.objects.all()

    for category in categories:
        list_of_posts = Post.objects.filter(post_time__range=(start, finish), category=category.pk)
        subscribers_emails = set(Category.objects.filter(id = category.pk).values_list("subscribers__email", flat = True))

        if list_of_posts:
            html_content = render_to_string('daily_post.html', {'posts': list_of_posts, 'category': category.category_name})

            msg = EmailMultiAlternatives(
                subject=f'Новости за неделю',
                from_email='bossdb90@yandex.ru',
                to=subscribers_emails,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

