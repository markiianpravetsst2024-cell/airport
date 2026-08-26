import stripe
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Order, Ticket


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order_id = session.client_reference_id

            try:
                order = Order.objects.get(id=order_id)
                order.status = Order.Status.PAID
                order.save()
                order.tickets.update(status=Ticket.Status.PAID)
            except Order.DoesNotExist:
                pass

        return HttpResponse(status=200)