from django.contrib import admin

from reviews.models import Ticket, Review, Subscription

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(Subscription)
