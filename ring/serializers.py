from rest_framework import serializers
from .models import Company, Assistant
from twilio.rest import Client
from django.contrib.auth.models import User


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['founder', 'phoneNumber', 'companyName']


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'company']

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        company_serializer = CompanySerializer(data=company_data, context={'request': self.context['request']})
        if company_serializer.is_valid(raise_exception=True):
            company_serializer.save(user=user)

        return user

    def update(self, instance, validated_data):
        company_data = validated_data.pop('company', None)
        company_instance = instance.company

        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        if company_data:
            company_serializer = CompanySerializer(company_instance, data=company_data, partial=True,
                                                   context={'request': self.context['request']})
            if company_serializer.is_valid(raise_exception=True):
                company_serializer.save()

        return instance


class AssitantSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source='company' 
    )

    class Meta:
        model = Assistant
        fields = ("pk", "company_id", "content", "name")
