# Status API endpoints for professors
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .models import TeacherProfile
import json


@login_required(login_url='teacher_login')
@require_GET
def api_get_professor_status(request):
    """Get the current professor's status"""
    try:
        teacher_profile = TeacherProfile.objects.get(user=request.user)
        return JsonResponse({
            "success": True,
            "status": teacher_profile.status
        })
    except TeacherProfile.DoesNotExist:
        # If no profile exists, return default status
        return JsonResponse({
            "success": True,
            "status": "available"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)


@login_required(login_url='teacher_login')
def api_set_professor_status(request):
    """Set the current professor's status"""
    if request.method != 'POST':
        return JsonResponse({
            "success": False,
            "error": "Method not allowed"
        }, status=405)
    
    try:
        data = json.loads(request.body)
        status = data.get('status')
        
        # Validate status
        valid_statuses = ['available', 'busy', 'absent']
        if status not in valid_statuses:
            return JsonResponse({
                "success": False,
                "error": "Invalid status"
            }, status=400)
        
        # Get or create TeacherProfile
        teacher_profile, created = TeacherProfile.objects.get_or_create(user=request.user)
        teacher_profile.status = status
        teacher_profile.save()
        
        return JsonResponse({
            "success": True,
            "status": teacher_profile.status,
            "message": "Status updated successfully"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)
