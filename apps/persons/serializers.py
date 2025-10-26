from rest_framework import serializers
from .models import Person, PersonGroup, ChangeSet
from datetime import datetime


class PersonSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с Person через API"""
    
    class Meta:
        model = Person
        fields = [
            'id', 'group_id', 'last_name', 'first_name', 'middle_name',
            'birth_date', 'gender', 'address', 'phone', 'email',
            'created_at', 'is_current'
        ]
        read_only_fields = ['id', 'group_id', 'created_at', 'is_current']

    def validate_last_name(self, value):
        """Валидация фамилии"""
        person = Person(last_name=value)
        if not person._validate_name(value):
            raise serializers.ValidationError(
                'Фамилия должна начинаться с большой буквы, содержать минимум 2 символа кириллицы и дефис'
            )
        return value

    def validate_first_name(self, value):
        """Валидация имени"""
        person = Person(first_name=value)
        if not person._validate_name(value):
            raise serializers.ValidationError(
                'Имя должно начинаться с большой буквы, содержать минимум 2 символа кириллицы и дефис'
            )
        return value

    def validate_middle_name(self, value):
        """Валидация отчества"""
        if value:
            person = Person(middle_name=value)
            if not person._validate_name(value):
                raise serializers.ValidationError(
                    'Отчество должно начинаться с большой буквы, содержать минимум 2 символа кириллицы и дефис'
                )
        return value

    def validate_phone(self, value):
        """Валидация телефона"""
        if value:
            person = Person(phone=value)
            if not person._validate_phone(value):
                raise serializers.ValidationError(
                    'Телефон должен быть в формате +7(XXX)XXX-XX-XX'
                )
        return value

    def validate_email(self, value):
        """Валидация email"""
        if value:
            person = Person(email=value)
            if not person._validate_email(value):
                raise serializers.ValidationError(
                    'Email должен быть в формате login@domain, где login и domain минимум 3 символа'
                )
        return value

    def validate_address(self, value):
        """Валидация адреса"""
        if not value or not value.strip():
            raise serializers.ValidationError('Адрес не может быть пустым')
        return value

    def validate_birth_date(self, value):
        """Валидация даты рождения"""
        if value > datetime.now().date():
            raise serializers.ValidationError('Дата рождения не может быть в будущем')
        return value


class PersonSearchSerializer(serializers.Serializer):
    """Сериализатор для поиска людей"""
    last_name = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    middle_name = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    limit = serializers.IntegerField(default=100, min_value=1, max_value=1000)
    offset = serializers.IntegerField(default=0, min_value=0)


class PersonVitrineSerializer(serializers.Serializer):
    """Сериализатор для витрины (результатов поиска)"""
    group_id = serializers.IntegerField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(allow_null=True)
    birth_date = serializers.DateField()
    gender = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField(allow_null=True)
    email = serializers.CharField(allow_null=True)
