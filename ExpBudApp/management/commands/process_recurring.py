from django.core.management.base import BaseCommand
from ExpBudApp.models import RecurringTransaction, Transaction
from django.utils.timezone import now
from datetime import timedelta
import calendar

class Command(BaseCommand):
    help = 'Processes recurring transactions and creates corresponding Transaction entries.'

    def handle(self, *args, **kwargs):
        today = now().date()
        recurring_transactions = RecurringTransaction.objects.filter(next_due_date__lte=today)

        for rt in recurring_transactions:
            # 1. Create actual transaction
            Transaction.objects.create(
                user=rt.user,
                amount=rt.amount,
                category=rt.category,
                transaction_date=today,
                transaction_description=f"[Recurring] {rt.category}",
                payment_method=rt.payment_method,
                merchant_name=rt.merchant_name,
            )

            # 2. Update next_due_date based on frequency
            if rt.frequency == 'Daily':
                next_due = rt.next_due_date + timedelta(days=1)
            elif rt.frequency == 'Weekly':
                next_due = rt.next_due_date + timedelta(weeks=1)
            elif rt.frequency == 'Monthly':
                month = rt.next_due_date.month + 1 if rt.next_due_date.month < 12 else 1
                year = rt.next_due_date.year if rt.next_due_date.month < 12 else rt.next_due_date.year + 1
                day = min(rt.next_due_date.day, calendar.monthrange(year, month)[1])
                next_due = rt.next_due_date.replace(year=year, month=month, day=day)
            elif rt.frequency == 'Yearly':
                next_due = rt.next_due_date.replace(year=rt.next_due_date.year + 1)
            else:
                continue

            # 3. Save the updated next_due_date
            rt.next_due_date = next_due
            rt.save()

        self.stdout.write(self.style.SUCCESS(f"Processed {recurring_transactions.count()} recurring transactions."))
