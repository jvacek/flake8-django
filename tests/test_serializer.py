from .utils import error_code_in_result, run_check


def test_serializer_exclude_fails():
    code = """
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
    """
    result = run_check(code)
    assert error_code_in_result("DJ26", result)


def test_serializer_fields_all_fails():
    code = """
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    """
    result = run_check(code)
    assert error_code_in_result("DJ27", result)


def test_serializer_fields_list_success():
    code = """
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    """
    result = run_check(code)
    assert not error_code_in_result("DJ26", result)
    assert not error_code_in_result("DJ27", result)
