from django.contrib import admin

from reviews.models import Ticket, Review, Subscription


class TicketAdmin(admin.ModelAdmin):

    list_display = ["title", "user", "time_created"]
    list_filter = ["user"]


class ReviewAdmin(admin.ModelAdmin):

    list_display = ["headline", "rating", "user", "time_created"]
    list_filter = ["user"]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Subscription)
