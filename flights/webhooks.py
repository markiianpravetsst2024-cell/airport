import logging
import stripe
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Order, Ticket, Payment

logger = logging.getLogger(__name__)

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
            session_id = session.id

            try:
                order = Order.objects.get(id=order_id)
                order.status = Order.Status.PAID
                order.save()
                order.tickets.update(status=Ticket.Status.PAID)
                Payment.objects.filter(stripe_session_id=session_id).update(status=Payment.Status.PAID)
            except Order.DoesNotExist:
                    logger.error(f"CRITICAL: Stripe reported successful payment for missing Order ID {order_id}!")

        elif event['type'] == 'checkout.session.expired':
            session = event['data']['object']
            order_id = session.client_reference_id
            session_id = session.id

            try:
                order = Order.objects.get(id=order_id)
                order.status = Order.Status.EXPIRED
                order.save()

                order.tickets.update(status=Ticket.Status.CANCELLED)

                Payment.objects.filter(stripe_session_id=session_id).update(status=Payment.Status.FAILED)
            except Order.DoesNotExist:
                logger.warning(f"Stripe reported expired session for missing Order ID {order_id}.")

        return HttpResponse(status=200)