from rest_framework import serializers

class ModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['company'] = self.context['user'].employee.company
        return super().create(validated_data)