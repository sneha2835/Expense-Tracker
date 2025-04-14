from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from io import BytesIO
import csv
from reportlab.pdfgen import canvas
from ExpBudApp.models import Transaction
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader



class ExportTransactionsCSV(APIView):
    """
    Export user transactions to CSV format.
    URL: /export/csv/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')

        # Create the HTTP response with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Time', 'Amount', 'Category', 'Merchant', 'Payment Method', 'Description'])

        for txn in transactions:
            writer.writerow([
                txn.transaction_date,
                txn.transaction_time,
                txn.amount,
                txn.category,
                txn.merchant_name or '',
                txn.payment_method,
                txn.transaction_description or ''
            ])

        return response


class ExportTransactionsPDF(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')

        # Step 1: Prepare Pie Chart (Category -> Sum of Amounts)
        category_totals = {}
        for txn in transactions:
            category_totals[txn.category] = category_totals.get(txn.category, 0) + float(txn.amount)

        # Generate pie chart image
        pie_buffer = BytesIO()
        if category_totals:
            labels = list(category_totals.keys())
            sizes = list(category_totals.values())

            plt.figure(figsize=(4, 4))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title('Expense Distribution by Category')
            plt.tight_layout()
            plt.savefig(pie_buffer, format='PNG')
            plt.close()
            pie_buffer.seek(0)

        # Step 2: Build PDF
        pdf_buffer = BytesIO()
        p = canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter
        p.setFont("Helvetica", 12)
        p.drawString(200, height - 40, "Transaction History")

        # Draw pie chart image on PDF
        if category_totals:
            image = ImageReader(pie_buffer)
            p.drawImage(image, 150, height - 300, width=300, height=300)

        # Draw transaction table below chart
        y = height - 320
        p.setFont("Helvetica", 10)
        for txn in transactions:
            line = f"{txn.transaction_date} | ₹{txn.amount} | {txn.category} | {txn.payment_method}"
            p.drawString(40, y, line)
            y -= 20
            if y < 40:
                p.showPage()
                y = height - 40
                p.setFont("Helvetica", 10)

        p.save()
        pdf_buffer.seek(0)

        # Step 3: Return the file as download
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transactions_with_chart.pdf"'
        return response