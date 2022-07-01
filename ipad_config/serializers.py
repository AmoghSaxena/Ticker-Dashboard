from abc import ABC

from rest_framework import serializers

from .models import MainFeatures, JavaConfig


class RecursiveField(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MainFeatureSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = MainFeatures
        fields = ['id', 'room_type', 'name', 'feature', 'parent_id', 'children', 'enabled', 'position']


class MainFeatureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainFeatures
        fields = ['id', 'room_type', 'name', 'feature', 'parent_id', 'enabled', 'position', 'feature_images']


class JavaConfigSerializer(serializers.ModelSerializer):
    config_val = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JavaConfig
        fields = ['module', 'config_key', 'config_val', 'val_type', 'description',
                  'is_deletable', 'hotel_id', 'is_active', 'delete_msg', 'is_deleted',
                  'created_by', 'created_on']

    @staticmethod
    def get_config_val(obj):
        return obj.get_config_val()
