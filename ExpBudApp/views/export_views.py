# expbudapp/views/export_views.py
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
import csv
<<<<<<< HEAD
from weasyprint import HTML
=======
#from weasyprint import HTML
>>>>>>> origin/Srinidhi
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import base64

# Helper function to calculate weekly, monthly, quarterly, and yearly date ranges
def get_date_range(period, start_date=None, end_date=None):
    # Use current date as the default if no dates are provided
    if not start_date:
        start_date = datetime.today()
    if not end_date:
        end_date = datetime.today()

    if period == 'weekly':
        start_date = start_date - timedelta(days=start_date.weekday())  # Start of the week
        end_date = start_date + timedelta(days=6)  # End of the week
    elif period == 'monthly':
        start_date = start_date.replace(day=1)  # Start of the month
        end_date = (start_date.replace(month=start_date.month+1, day=1) - timedelta(days=1))  # End of the month
    elif period == 'quarterly':
        # Calculate the start and end of the quarter
        quarter = (start_date.month - 1) // 3 * 3 + 1
        start_date = start_date.replace(month=quarter, day=1)
        end_date = (start_date.replace(month=quarter+3, day=1) - timedelta(days=1))  # End of the quarter
    elif period == 'yearly':
        start_date = start_date.replace(month=1, day=1)  # Start of the year
        end_date = start_date.replace(year=start_date.year+1) - timedelta(days=1)  # End of the year

    return start_date, end_date

# CSV Export View (unchanged)
def export_transactions_to_csv(request):
    # Get query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    period = request.GET.get('period', 'monthly')  # Default to monthly

    # Get the date range based on the selected period
    start_date, end_date = get_date_range(period, start_date, end_date)

    # Fetch transactions from the database (replace with real query)
    transactions = [
        {"date": "2025-01-01", "category": "Groceries", "amount": 100},
        {"date": "2025-02-01", "category": "Groceries", "amount": 150},
        {"date": "2025-03-01", "category": "Transport", "amount": 80},
    ]
    
    # Filter transactions based on query parameters (if needed)
    transactions = [t for t in transactions if start_date <= datetime.strptime(t['date'], "%Y-%m-%d") <= end_date]
    if category:
        transactions = [t for t in transactions if t['category'] == category]

    # Prepare CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    writer = csv.DictWriter(response, fieldnames=["date", "category", "amount"])
    writer.writeheader()
    writer.writerows(transactions)
    return response

# PDF Export View with Weekly, Monthly, Quarterly, Yearly Reports
def export_transactions_to_pdf(request):
    # Get query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    period = request.GET.get('period', 'monthly')  # Default to monthly

    # Get the date range based on the selected period
    start_date, end_date = get_date_range(period, start_date, end_date)

    # Fetch transactions from the database (replace with real query)
    transactions = [
        {"date": "2025-01-01", "category": "Groceries", "amount": 100},
        {"date": "2025-02-01", "category": "Groceries", "amount": 150},
        {"date": "2025-03-01", "category": "Transport", "amount": 80},
    ]
    
    # Filter transactions based on query parameters
    transactions = [t for t in transactions if start_date <= datetime.strptime(t['date'], "%Y-%m-%d") <= end_date]
    if category:
        transactions = [t for t in transactions if t['category'] == category]

    # Prepare the chart (e.g., Pie chart of transaction categories)
    category_data = {}
    for transaction in transactions:
        category_data[transaction['category']] = category_data.get(transaction['category'], 0) + transaction['amount']

    # Create a pie chart
    plt.figure(figsize=(6, 4))
    plt.pie(category_data.values(), labels=category_data.keys(), autopct='%1.1f%%', startangle=90)
    plt.title(f'Transaction Categories Breakdown ({period.capitalize()})')

    # Save the pie chart to a BytesIO object
    chart_image = BytesIO()
    plt.savefig(chart_image, format='png')
    chart_image.seek(0)  # Rewind the BytesIO object to the beginning

    # Base64 encode the image for embedding in the PDF
    chart_base64 = base64.b64encode(chart_image.getvalue()).decode('utf-8')

    # Render HTML for the PDF
    html_content = render_to_string('transactions_pdf_template.html', {
        'transactions': transactions,
        'period': period.capitalize(),
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    })

    # Render the HTML template with the embedded chart
    html_content_with_chart = render_to_string('transactions_pdf_template_with_chart.html', {
        'transactions': transactions,
        'chart_base64': chart_base64,
        'period': period.capitalize(),
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    })

    # Generate the PDF from the HTML content
    pdf_with_chart = HTML(string=html_content_with_chart).write_pdf()

    # Prepare PDF response with embedded chart
    response = HttpResponse(pdf_with_chart, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transactions_{period}_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.pdf"'
    return response
