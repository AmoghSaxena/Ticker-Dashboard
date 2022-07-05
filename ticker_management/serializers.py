from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = '__all__'
		# fields =('tv_condition_before', 'tv_condition_after', 'room_no', 'key','ip', 'ipad_condition_before', 'ipad_condition_after','completed')