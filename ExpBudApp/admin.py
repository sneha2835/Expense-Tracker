from django.contrib import admin
from .models import User, Budget, Transaction, RecurringTransaction


admin.site.register(User)
admin.site.register(Budget)
admin.site.register(Transaction)
admin.site.register(RecurringTransaction)