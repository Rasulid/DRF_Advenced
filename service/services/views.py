from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from .serializer import SupscriptionSerializer
from clients.models import Client


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        'service',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email'))
    ).annotate(price=F('service__price') -
                     F('service__price') *
                     F('plan__discount_percent') / 100.00)

    serializer_class = SupscriptionSerializer

    # aggregation function
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = super().list(request, *args, **kwargs)

        response_data = {
            'result': response.data,
            'total_amount': queryset.aggregate(total=Sum('price')).get('total')
        }
        response.data = response_data

        return response
