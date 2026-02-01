from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student, Group, Attendance
import json
from datetime import datetime


# =========================
# HTML VIEWS (TEMPLATES)
# =========================

def home(request):
    """Main dashboard page"""
    groups = Group.objects.prefetch_related('students').all()
    total_students = Student.objects.count()
    recent_attendance = Attendance.objects.select_related('student').order_by('-date')[:10]

    context = {
        'groups': groups,
        'total_students': total_students,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'home.html', context)


def group_detail(request, group_id):
    """Detail page for a group with students and attendance"""
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all().prefetch_related('attendance_set')

    context = {
        'group': group,
        'students': students,
    }
    return render(request, 'detail.html', context)


def students_list(request):
    """List of all students"""
    students = Student.objects.select_related('group').all()

    context = {
        'students': students,
    }
    return render(request, 'students_list.html', context)


# =========================
# API VIEWS (REST)
# =========================

@require_http_methods(["GET"])
def api_students_list(request):
    """GET /api/students/"""
    students = Student.objects.select_related('group').all()

    data = [
        {
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "student_id": s.student_id,
            "group": {
                "id": s.group.id if s.group else None,
                "name": s.group.name if s.group else None,
            }
        }
        for s in students
    ]

    return JsonResponse({
        "status": "success",
        "count": len(data),
        "data": data
    })


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def api_attendance(request):
    """
    GET    /api/attendance/        -> list records
    POST   /api/attendance/        -> create record
    PUT    /api/attendance/        -> update record
    DELETE /api/attendance/        -> delete record
    """

    # ---------- GET ----------
    if request.method == "GET":
        records = Attendance.objects.select_related('student').all()

        data = [
            {
                "id": r.id,
                "student": {
                    "id": r.student.id,
                    "name": f"{r.student.first_name} {r.student.last_name}",
                    "student_id": r.student.student_id,
                },
                "date": r.date.strftime("%Y-%m-%d"),
                "status": r.status,
            }
            for r in records
        ]

        return JsonResponse({
            "status": "success",
            "count": len(data),
            "data": data
        })

    # Parse JSON body for POST/PUT/DELETE
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # ---------- POST ----------
    if request.method == "POST":
        student_id = body.get("student_id")
        date_str = body.get("date")
        status = body.get("status")

        if not all([student_id, date_str, status]):
            return JsonResponse({"error": "Missing fields"}, status=400)

        student = get_object_or_404(Student, id=student_id)

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        attendance = Attendance.objects.create(
            student=student,
            date=date_obj,
            status=status
        )

        return JsonResponse({
            "message": "Attendance created",
            "id": attendance.id
        }, status=201)

    # ---------- PUT ----------
    if request.method == "PUT":
        attendance_id = body.get("id")
        status = body.get("status")

        if not attendance_id:
            return JsonResponse({"error": "Attendance ID required"}, status=400)

        attendance = get_object_or_404(Attendance, id=attendance_id)

        if status:
            attendance.status = status
            attendance.save()

        return JsonResponse({"message": "Attendance updated"})

    # ---------- DELETE ----------
    if request.method == "DELETE":
        attendance_id = body.get("id")

        if not attendance_id:
            return JsonResponse({"error": "Attendance ID required"}, status=400)

        attendance = get_object_or_404(Attendance, id=attendance_id)
        attendance.delete()

        return JsonResponse({"message": "Attendance deleted"})
