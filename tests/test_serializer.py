from .utils import error_code_in_result, run_check
from .utils import run_check, load_fixture_file, error_code_in_result


def test_serializer_exclude_fails():
    code = load_fixture_file('serializer_exclude.py')
    result = run_check(code)
    assert error_code_in_result("DJ26", result)


def test_serializer_fields_all_fails():
    code = load_fixture_file('serializer_fields_all.py')
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
