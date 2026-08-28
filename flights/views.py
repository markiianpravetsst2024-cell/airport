import stripe
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins
from .models import Flight, Ticket, Order
from .serializers import FlightSerializer, TicketSerializer, FlightReadSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from airports.permissions import IsAdminOrReadOnly
from .filters import FlightFilter, TicketFilter

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = FlightFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FlightReadSerializer
        return FlightSerializer

class OrderViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'])
    def pay(self, request, pk=None):
        order = self.get_object()
        if order.status == 'paid':
            return Response({'message': 'Order is already paid'}, status=status.HTTP_400_BAD_REQUEST)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        domain_url = settings.DOMAIN_URL
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'Ticket for Order #{order.id}',
                            },
                            'unit_amount': int(order.total_price * 100),
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=domain_url + '/api/orders/success/',
                cancel_url=domain_url + '/api/orders/cancel/',
                client_reference_id=str(order.id)
            )

            order.payment_id = checkout_session.id
            order.save()

            return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)


        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TicketFilter

    def get_queryset(self):
        return Ticket.objects.filter(order__user=self.request.user)