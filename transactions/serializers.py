from rest_framework import serializers
from .models import Transaction
from .utils import get_exchange_rate, verify_proof

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('status', 'amount_receiver', 'is_verified', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Calcul montant converti
        rate = get_exchange_rate(validated_data['currency_sender'], validated_data['currency_receiver'])
        if not rate:
            raise serializers.ValidationError("Impossible de récupérer le taux de change.")
        validated_data['amount_receiver'] = validated_data['amount_sender'] * rate

        transaction = Transaction.objects.create(**validated_data)

        # Vérification automatique si preuve uploadée
        if transaction.proof:
            transaction.is_verified = verify_proof(transaction.proof.path, transaction.amount_sender)
            transaction.save()

        # Notification en temps réel
        from .utils import send_transaction_notification
        send_transaction_notification(transaction)

        return transaction
