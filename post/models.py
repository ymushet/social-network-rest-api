from django.db import models


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey('user.CustomUser',
                               related_name='posts',
                               on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey('user.CustomUser',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'post')
