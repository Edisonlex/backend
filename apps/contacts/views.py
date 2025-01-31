# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, Newsletter

class ContactCreateView(APIView):
    def post(self, request, format=None):
        data = self.request.data

        try:
            Contact.objects.create(
                name=data['name'],
                email=data['email'],
                subject=data['subject'],
                phone=data['phone'],
                message=data['message'],
                budget=data['budget'],
            )
            return Response({'success': 'Mensaje guardado exitosamente'})
        except:
            return Response(
                {'error': 'Error al guardar el mensaje'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NewsletterSubscriptionView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            if not email:
                return Response(
                    {'error': 'El email es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            Newsletter.objects.create(email=email)
            return Response({'success': 'Suscripción exitosa'})
        except:
            return Response(
                {'error': 'Error al procesar la suscripción'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
