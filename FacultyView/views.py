from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Student
import qrcode
import socket
import pandas as pd
from datetime import datetime
from StudentView.views import present


def qrgenerator():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]

    link = f"http://{ip}:8000/add_manually"

    # Function to generate and display a QR code
    def generate_qr_code(link):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("FacultyView/static/FacultyView/qrcode.png")

    generate_qr_code(link)


def faculty_view(request):
    if request.method == "POST":
        student_roll = request.POST["student_id"]
        student = Student.objects.get(s_roll=student_roll)
        if student in present:
            present.remove(student)
        return HttpResponseRedirect("/")

    else:
        qrgenerator()
        return render(
            request,
            "FacultyView/FacultyViewIndex.html",
            {
                "students": present,
            },
        )


def add_manually(request):
    students = Student.objects.all().order_by("s_roll")
    return render(
        request,
        "StudentView/StudentViewIndex.html",
        {
            "students": students,
        },
    )

def export_attendance_excel(request):
    # Create a DataFrame from the present students
    data = {
        'Roll Number': [student.s_roll for student in present],
        'First Name': [student.s_fname for student in present],
        'Last Name': [student.s_lname for student in present],
        'Branch': [student.s_branch for student in present],
        'Year': [student.s_year for student in present],
        'Section': [student.s_section for student in present],
        'Date': [datetime.now().strftime('%Y-%m-%d')] * len(present),
        'Time': [datetime.now().strftime('%H:%M:%S')] * len(present)
    }
    
    df = pd.DataFrame(data)
    
    # Create the HTTP response with Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=attendance_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    # Write the DataFrame to Excel
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response
