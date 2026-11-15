from rest_framework import serializers


class SpecializationCountSerializer(serializers.Serializer):
    specialization = serializers.CharField()
    doctor_count = serializers.IntegerField()
