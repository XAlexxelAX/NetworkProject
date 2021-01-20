from django.contrib import admin
from movies import models as movies_models

# Register your models here.
admin.site.register(movies_models.Movie)
admin.site.register(movies_models.Screening)
admin.site.register(movies_models.Ticket)
admin.site.register(movies_models.Hall)