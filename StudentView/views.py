from django.shortcuts import render
from FacultyView.models import Student
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.

present = set()


def add_manually_post(request):
    student_roll = request.POST["student-name"]
    student = Student.objects.get(s_roll=student_roll)
    present.add(student)
    return HttpResponseRedirect("/submitted")


def submitted(request):
    return render(request, "StudentView/Submitted.html")


@csrf_exempt
def api_mark_attendance(request):
    """API endpoint for remote scanners to mark attendance.

    Accepts POST with JSON body like: { "roll": "S123" }
    or form-encoded data with key 'roll' or 'code'.

    This view is CSRF-exempt to allow external scanners (ngrok/remote)
    to POST without a browser CSRF token. Keep this in development only
    or protect it with a shared secret in production.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    # Try JSON body first, fall back to POST params
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except Exception:
        data = {}

    if not data:
        data = request.POST

    roll = data.get("roll") or data.get("s_roll") or data.get("code")
    if not roll:
        return JsonResponse({"error": "roll (or code) is required"}, status=400)

    try:
        student = Student.objects.get(s_roll=roll)
    except Student.DoesNotExist:
        return JsonResponse({"error": "student not found"}, status=404)

    present.add(student)
    return JsonResponse({"success": True, "roll": roll})
