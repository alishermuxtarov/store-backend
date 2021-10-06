
from rest_framework import serializers


class ValidatorSerializer(serializers.Serializer, object):
    @classmethod
    def check(cls, data, many=False, context=None):
        serializer = cls(data=data, many=many, context=context or {})
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
