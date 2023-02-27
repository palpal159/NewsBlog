from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    """Модель содержащая в себе объекты всех авторов"""
    auth_rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.auth_rating = 0
        posts = Post.objects.filter(author=self)
        for post in posts:
            self.auth_rating += post.rating_post * 3
            comments = Comment.objects.filter(post=post)
            for comment in comments:
                self.auth_rating += comment.rating_comment
            own_comments = Comment.objects.filter(user=self.user)
            for own_comment in own_comments:
                self.auth_rating += own_comment.rating_comment

        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    """Категории новостей/статей - темы, которые они отображают.
    Имеет единственное поле: Название категории. Поле должно быть уникальным"""
    name_category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='SubscribersCategory')

    def __str__(self):
        return f'{self.name_category}'


class SubscribersCategory(models.Model):
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    """Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    Каждый объект может иметь одну или несколько категорий."""
    NEWS = 'NE'
    ARTICLE = 'AR'
    TYPE = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2, choices=TYPE, default=ARTICLE)
    date_time_post = models.DateTimeField(auto_now_add=True)
    categories_post = models.ManyToManyField(Category, through='PostCategory')
    title_post = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.FloatField(default=0.0)

    def like_post(self):
        self.rating_post += 1
        self.save()

    def dislike_post(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text_post[:144] + '...'

    def __str__(self):
        return self.title_post

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.pk})


class PostCategory(models.Model):
    """Промежуточная модель для связи многие ко многим"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title_post}: {self.category.name_category}'


class Comment(models.Model):
    comment_text = models.TextField(default="Текст комментария")
    comment_date = models.DateTimeField(auto_now_add=True)
    rating_comment = models.FloatField(default=0.0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like_comment(self):
        self.rating_comment += 1
        self.save()

    def dislike_comment(self):
        self.rating_comment -= 1
        self.save()
