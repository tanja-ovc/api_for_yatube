from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True),
    group = models.ForeignKey(
        'Group', on_delete=models.CASCADE, related_name='posts',
        blank=True, null=True)

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    # кто подписывается
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='подписчик'
    )
    # на кого подписываются
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='подписан(а) на'
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'following'],
                       name='unique_subscription')]
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        follow_str = f'Подписка {self.user} на {self.following}'
        return follow_str
