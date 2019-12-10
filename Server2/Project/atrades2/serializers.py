from .models import User, Transaction, BankAccount, Company, Stocks, RecurringBuy

from rest_framework import routers, serializers, viewsets



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_fname', 'user_lname', 'user_ssn', 'user_address', 'user_email', 'user_phone']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'transaction_user', 'transaction_account', 'transaction_timestamp', 'transaction_type', 'transaction_symbol', 'transaction_price']

        

class StocksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stocks
        fields = ['stock_id', 'stock_user', 'stock_symbol', 'stock_buy_price', 'stock_buy_timestamp', 'stock_count']


class RecurringBuySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecurringBuy
        fields = ['rec_id', 'rec_user_id', 'rec_count', 'rec_symbol', 'rec_interval', 'rec_start_timestamp', 'rec_schedule']


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['company_id', 'company_symbol', 'company_name', 'company_description', 'company_employees', 'company_address', 'company_zip', 'company_country']


class BankAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['acc_id', 'acc_owner', 'acc_type', 'acc_number', 'acc_routing_number', 'acc_balance']