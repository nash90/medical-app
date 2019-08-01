from rest_framework import serializers
from ..models import Drug

class DrugSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drug
        fields = ['drug_id', 'drug_subclass_id', 'drug_name']