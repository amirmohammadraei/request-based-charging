from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.db.models import Count
from datetime import datetime


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        Token.objects.filter(user=user).delete()

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class UserTokenCreateView(CreateAPIView):
    serializer_class = UserAuthenticationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class RequestCreateView(CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        username = request.data.get('user')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            Request.objects.create(user=user)
            return Response({'message': 'New request created for the user.'}, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


class RequestListView(ListAPIView):
    serializer_class = UserRequestCountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Request.objects.values('user__id', 'user__username').annotate(request_count=Count('user'))
        return queryset


class TotalPriceView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TotalPriceSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)

        if username:
            return self.calculate_total_price_for_user(username)
        else:
            return self.calculate_total_price_for_all_users()

    def calculate_total_price_for_user(self, username):
        try:
            user = User.objects.get(username=username)
            request_count = Request.objects.filter(user=user).count()
            cost_per_request = 0.001
            total_price = request_count * cost_per_request
            return [{'user': user.username, 'total_price': total_price}]
        except User.DoesNotExist:
            return [{'user': 'User does not exist.', 'total_price': 0}]

    def calculate_total_price_for_all_users(self):
        users = User.objects.all()
        total_prices = []

        for user in users:
            request_count = Request.objects.filter(user=user).count()
            cost_per_request = 0.001
            total_price = request_count * cost_per_request
            total_prices.append({'user': user.username, 'total_price': total_price})

        return total_prices

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentMonthCostView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentMonthCostSerializer

    def get_object(self):
        user = self.request.user
        current_month = datetime.now().month
        requests_in_current_month = Request.objects.filter(
            user=user,
            timestamp__month=current_month
        )

        total_cost = len(requests_in_current_month) * 0.001

        return {'user': user.username, 'total_cost': total_cost}
