from django.http import JsonResponse
from django.views.decorators.http import require_GET
from academeet.supabase_client import get_holidays as get_supabase_holidays
from datetime import datetime
from .models import Holiday


# --- DRF Imports ---
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # <-- Allows access for testing
# -----------------------------

from .models import Schedule # Crucial: Import your Schedule model

# ----------------- STANDARD DJANGO VIEW (Enhanced Holiday Endpoint) -----------------


@require_GET
def get_holidays_api(request, year=None, month=None):
    """API endpoint to fetch recurring holidays constructed for the given year/month"""
    try:
        if year and month:
            y = int(year)
            m = int(month)
            
            # Query all holidays and construct dates for this year/month
            holidays = Holiday.objects.filter(month=m).order_by('day')
            
            # Convert to full dates for the requested year
            holiday_data = []
            for h in holidays:
                full_date = h.get_date_for_year(y)
                if full_date:
                    holiday_data.append({
                        'date': full_date.isoformat(),
                        'name': h.name,
                        'holiday_name': h.name,
                        'description': h.description or '',
                        'school_specific': getattr(h, 'school_specific', False)
                    })
            
            # If no local holidays for this month, try Supabase fallback
            if not holiday_data:
                supabase_holidays = get_supabase_holidays(y, m)
                holiday_data = supabase_holidays if supabase_holidays else []
        else:
            # Get all holidays from local database (recurring definition)
            holidays = Holiday.objects.all().order_by('month', 'day')
            # For all-holidays endpoint, construct dates for current year
            from datetime import date as date_class
            current_year = date_class.today().year
            holiday_data = []
            for h in holidays:
                full_date = h.get_date_for_year(current_year)
                if full_date:
                    holiday_data.append({
                        'date': full_date.isoformat(),
                        'name': h.name,
                        'holiday_name': h.name,
                        'description': h.description or '',
                        'school_specific': getattr(h, 'school_specific', False)
                    })
        
        return JsonResponse(holiday_data, safe=False)
    except Exception as e:
        print(f"Error in get_holidays_api: {e}")
        # Fallback to empty list if error
        return JsonResponse([], safe=False)



# ---------------------------- DRF SERIALIZER -----------------------------------

class ScheduleSerializer(serializers.ModelSerializer):
    professor_username = serializers.CharField(source='professor.username', read_only=True)
    department_display = serializers.CharField(source='get_department_display', read_only=True)
    start_time_formatted = serializers.CharField(source='formatted_start_time', read_only=True)
    end_time_formatted = serializers.CharField(source='formatted_end_time', read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'department', 'department_display', 'professor_username', 
            'day', 'start_time', 'end_time', 'start_time_formatted', 'end_time_formatted',
            'subject_code', 'subject_name', 'section', 'room', 
            'year_level', 'status'
        ]

# ---------------------------- DRF FILTER VIEWS ----------------------------------

VALID_DEPARTMENTS = [
    'CCS', 'CMBA', 'CCJ', 'CNAHS', 'CEA', 'CASE'
]

# --- 1. ENDPOINT: Filter by Department (URL Path) ---
class ScheduleDepartmentFilterView(ListAPIView):
    """ GET /api/schedules/department/CCS/ """
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny] # TEMPORARY: Allows testing without login
    
    def get_queryset(self):
        dept_code = self.kwargs.get('dept_code', '').upper()
        if dept_code not in VALID_DEPARTMENTS:
            return Schedule.objects.none()
        return Schedule.objects.filter(department=dept_code)

    def list(self, request, *args, **kwargs):
        dept_code = self.kwargs.get('dept_code', '').upper()
        if dept_code not in VALID_DEPARTMENTS:
            return Response(
                {"detail": f"Department code '{dept_code}' is invalid."},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().list(request, *args, **kwargs)


# --- 2. ENDPOINT: Filter by Timeslot/Day (Query Params) ---
class ScheduleDayTimeFilterView(ListAPIView):
    """ GET /api/schedules/?day=Monday&timeslot=08:00:00 """
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny] # TEMPORARY: Allows testing without login
    
    def get_queryset(self):
        queryset = Schedule.objects.all()
        
        day = self.request.query_params.get('day', None)
        timeslot = self.request.query_params.get('timeslot', None)
        department = self.request.query_params.get('department', None)
        
        if day:
            queryset = queryset.filter(day__iexact=day)

        if timeslot:
            queryset = queryset.filter(start_time=timeslot)
            
        if department:
            queryset = queryset.filter(department=department)

        return queryset