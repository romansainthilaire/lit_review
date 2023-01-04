from django.db import models
from django.conf import settings


class Ticket(models.Model):

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="book_covers")
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):

    RATING_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.OneToOneField(to=Ticket, on_delete=models.CASCADE, related_name="review")
    headline = models.CharField(max_length=128)
    rating = models.SmallIntegerField(choices=RATING_CHOICES)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by")

    class Meta:
        unique_together = ["user", "followed_user"]

    def __str__(self):
        return f"{self.user.username} → {self.followed_user.username}"
