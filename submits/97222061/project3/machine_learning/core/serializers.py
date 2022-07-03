from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError


def interpolation_method_validator(method):
    if method not in [
        'linear',
        'time',
        'index',
        'pad',
        'from_derivatives',
        'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'spline', 'barycentric', 'polynomial',
        'krogh', 'piecewise_polynomial', 'spline', 'pchip', 'akima', 'cubicspline',
    ]:
        raise ValidationError(detail='invalid interpolation method', code=status.HTTP_400_BAD_REQUEST)


def calendar_type_validator(calendar_type):
    if calendar_type not in ['shamsi', 'miladi']:
        raise ValidationError(
            detail='invalid calendar type. (must be one of shmsi/miladi)',
            code=status.HTTP_400_BAD_REQUEST
        )


def time_interval_validator(interval):
    if interval not in ['1h', '1d', '1w', '1M']:
        raise ValidationError(
            detail='unsupported time interval. (must be one of 1h/1d/1w/1M)',
            code=status.HTTP_400_BAD_REQUEST
        )


def managing_method_serializer(method):
    if method not in ['undersampling', 'oversampling', 'smothe']:
        raise ValidationError(
            detail='unsupported method. (must be one of undersampling, oversampling, smothe)'
        )


class InterpolationSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10, validators=[calendar_type_validator], required=False, default='shamsi')
    time = serializers.CharField(max_length=5, validators=[time_interval_validator])
    interpolation = serializers.CharField(max_length=20, validators=[interpolation_method_validator])
    data = serializers.JSONField()
    skip_holiday = serializers.BooleanField(required=False, default=False)

    @classmethod
    def validate_interpolation(cls, method: str):
        return method.lower()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class OutlierDetectionSerializer(serializers.Serializer):
    time_series = serializers.BooleanField(default=False)
    data = serializers.JSONField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UnbalancedManagingSerializer(serializers.Serializer):
    major_class_tag = serializers.CharField(max_length=64)
    minor_class_tag = serializers.CharField(max_length=64)
    method = serializers.CharField(max_length=24, validators=[managing_method_serializer])
    data = serializers.JSONField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
