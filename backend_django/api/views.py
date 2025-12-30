from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from rafeeq.models import Subscription, Habit
from .serializers import OptInSerializer, UserSerializer

class RafeeqViewSet(viewsets.ViewSet):
    """
    API endpoints for Rafeeq functionality.
    """
    
    @action(detail=False, methods=['post'], url_path='opt-in')
    def opt_in(self, request):
        serializer = OptInSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            phone = data['phone_number']
            
            # Upsert User
            user, created = User.objects.update_or_create(
                phone_number=phone,
                defaults={
                    'username': phone, # Use phone as username for simplicity
                    'first_name': data.get('name', ''),
                    'timezone': data.get('timezone', 'UTC'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                }
            )
            
            # Upsert Subscription (Salah)
            habit, _ = Habit.objects.get_or_create(slug="salah", defaults={"name": "Salah"})
            
            Subscription.objects.update_or_create(
                user=user,
                habit=habit,
                defaults={
                    'is_active': True,
                    'preferences': data.get('preferences', {})
                }
            )
            
            return Response({
                "status": "success",
                "user_id": user.id,
                "message": "Welcome to Rafeeq (Django). Accountability active."
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='status')
    def status(self, request):
        phone = request.query_params.get('phone_number')
        if not phone:
            return Response({"detail": "Phone number required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(phone_number=phone)
            # Get preferences for Salah
            try:
                sub = Subscription.objects.get(user=user, habit__slug="salah", is_active=True)
                prefs = sub.preferences
                user_status = "active"
            except Subscription.DoesNotExist:
                prefs = {}
                user_status = "inactive"
                
            return Response({
                "status": user_status,
                "name": user.first_name,
                "preferences": prefs
            })
        except User.DoesNotExist:
            return Response({"status": "new_user", "preferences": None})
