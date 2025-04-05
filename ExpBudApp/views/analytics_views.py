# analytics_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F, Value, Case, When, IntegerField
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
from django.utils.dateparse import parse_date
from django.core.cache import cache
from django.http import HttpResponse
from io import BytesIO
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ExpBudApp.models import Transaction, SavingsGoal
from ExpBudApp.serializers import TransactionSerializer  # Assume you have this serializer


class UserAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Cache key for the user analytics data
        cache_key = f"user_{user.id}_analytics_data"

        # Check if the data is in cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        transactions = Transaction.objects.filter(user=user)

        # 🗓️ Optional filters
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
        category = request.query_params.get('category')

        if start_date and end_date:
            transactions = transactions.filter(date__range=(start_date, end_date))
        if category:
            transactions = transactions.filter(category=category)

        # 📅 Monthly Trends
        monthly_data = transactions.annotate(
            month=ExtractMonth('date'),
            year=ExtractYear('date')
        ).values('year', 'month').annotate(
            total_income=Sum(Case(
                When(transaction_type='income', then=F('amount')),
                default=Value(0),
                output_field=IntegerField()
            )),
            total_expense=Sum(Case(
                When(transaction_type='expense', then=F('amount')),
                default=Value(0),
                output_field=IntegerField()
            )),
        ).order_by('year', 'month')

        monthly_labels = []
        monthly_income = []
        monthly_expense = []
        for entry in monthly_data:
            label = f"{entry['month']}/{entry['year']}"
            monthly_labels.append(label)
            monthly_income.append(entry['total_income'])
            monthly_expense.append(entry['total_expense'])

        # 🗓️ Weekly Trends
        weekly_data = transactions.annotate(
            week=ExtractWeek('date'),
            year=ExtractYear('date')
        ).values('year', 'week').annotate(
            total_income=Sum(Case(
                When(transaction_type='income', then=F('amount')),
                default=Value(0),
                output_field=IntegerField()
            )),
            total_expense=Sum(Case(
                When(transaction_type='expense', then=F('amount')),
                default=Value(0),
                output_field=IntegerField()
            )),
        ).order_by('year', 'week')

        weekly_labels = []
        weekly_income = []
        weekly_expense = []
        for entry in weekly_data:
            label = f"Week {entry['week']}, {entry['year']}"
            weekly_labels.append(label)
            weekly_income.append(entry['total_income'])
            weekly_expense.append(entry['total_expense'])

        # 📆 Yearly Summaries
        yearly_data = transactions.annotate(
            year=ExtractYear('date')
        ).values('year').annotate(
            total_income=Sum(Case(
                When(transaction_type='income', then=F('amount')),
                default=Value(0),
                output_field=IntegerField()
            )),
            total_expense=Sum(Case(
                When(transaction_type='expense', then=F('amount')),
                default=Value(0),
                output_field=IntegerField()
            )),
        ).order_by('year')

        yearly_labels = [str(entry['year']) for entry in yearly_data]
        yearly_income = [entry['total_income'] for entry in yearly_data]
        yearly_expense = [entry['total_expense'] for entry in yearly_data]

        # 💰 Total Income and Expenses
        total_income = transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0

        total_expense = transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0

        # 💸 Potential Savings
        potential_savings = total_income - total_expense

        # 🧾 Category Breakdown
        category_data = transactions.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')

        category_labels = [entry['category'] for entry in category_data]
        category_totals = [entry['total'] for entry in category_data]

        # 🎯 Spending Goals Comparison
        savings_goals = SavingsGoal.objects.filter(user=user)
        total_desired_savings = savings_goals.aggregate(total=Sum('target_amount'))['total'] or 0
        actual_savings = potential_savings
        spending_goal_comparison = {
            'desired_savings': total_desired_savings,
            'actual_savings': actual_savings,
            'difference': actual_savings - total_desired_savings
        }

        # Prepare the response data
        response_data = {
            # Chart Data
            'monthly_trends': {
                'labels': monthly_labels,
                'income': monthly_income,
                'expense': monthly_expense
            },
            'weekly_trends': {
                'labels': weekly_labels,
                'income': weekly_income,
                'expense': weekly_expense
            },
            'yearly_trends': {
                'labels': yearly_labels,
                'income': yearly_income,
                'expense': yearly_expense
            },
            'category_breakdown': {
                'labels': category_labels,
                'values': category_totals
            },
            # Summary
            'total_income': total_income,
            'total_expense': total_expense,
            'potential_savings': potential_savings,
            'spending_goal_comparison': spending_goal_comparison
        }

        # Cache the response data for future requests
        cache.set(cache_key, response_data, timeout=3600)  # Cache timeout of 1 hour

        return Response(response_data)


# CSV Export Function
class ExportCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)

        # 🗓️ Optional filters
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
        category = request.query_params.get('category')

        if start_date and end_date:
            transactions = transactions.filter(date__range=(start_date, end_date))
        if category:
            transactions = transactions.filter(category=category)

        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Category', 'Amount', 'Transaction Type'])  # Headers
        
        # Write transaction data to CSV
        for transaction in transactions:
            writer.writerow([transaction.date, transaction.category, transaction.amount, transaction.transaction_type])
        
        return response


# PDF Export Function
class ExportPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)

        # 🗓️ Optional filters
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
        category = request.query_params.get('category')

        if start_date and end_date:
            transactions = transactions.filter(date__range=(start_date, end_date))
        if category:
            transactions = transactions.filter(category=category)

        # Create a PDF response
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "Transaction Report")

        # Define the y-position for data rows
        y_position = 730

        # Add headers
        p.drawString(100, y_position, "Date")
        p.drawString(200, y_position, "Category")
        p.drawString(300, y_position, "Amount")
        p.drawString(400, y_position, "Transaction Type")
        y_position -= 20

        # Add transaction data to the PDF
        for transaction in transactions:
            p.drawString(100, y_position, str(transaction.date))
            p.drawString(200, y_position, transaction.category)
            p.drawString(300, y_position, str(transaction.amount))
            p.drawString(400, y_position, transaction.transaction_type)
            y_position -= 20

            if y_position < 40:  # If we run out of space, create a new page
                p.showPage()
                y_position = 750

        p.showPage()
        p.save()

        # Return the PDF file as a response
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

