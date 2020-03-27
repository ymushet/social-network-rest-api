from django.db import models


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey('user.CustomUser',
                               related_name='posts',
                               on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} {self.created_at}'

    def like_post(self, user_id):
        like, _ = self.like_set.update_or_create(user_id=user_id,
                                                 defaults={'liked': True})
        return like

    def unlike_post(self, user_id):
        like = self.like_set.filter(user_id=user_id).first()
        if like is not None:
            like.liked = False
            like.save()


class Like(models.Model):
    user = models.ForeignKey('user.CustomUser',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')
        # likes that were 'liked again' or recently created will be displayed first
        ordering = ('updated_at',)

    def __str__(self):
        return f'{self.post.id}, user {self.user.id}, liked {self.liked}'
