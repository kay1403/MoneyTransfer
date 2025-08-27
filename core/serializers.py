from rest_framework import serializers
from .models import User, Transaction, Notification
from django.contrib.auth.password_validation import validate_password
from .utils import get_exchange_rate

# Serializer utilisateur
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'country', 'role', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            country=validated_data['country'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Serializer transaction
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at', 'amount_receiver')

    def create(self, validated_data):
        rate = get_exchange_rate(validated_data['currency_sender'], validated_data['currency_receiver'])
        if rate is None:
            raise serializers.ValidationError("Impossible de récupérer le taux de change.")
        
        # Conversion
        validated_data['amount_receiver'] = validated_data['amount_sender'] * rate
        
        transaction = Transaction.objects.create(**validated_data)
        return transaction


# Serializer notification
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
