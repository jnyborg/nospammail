from dashboard.models import GeneratedEmail
from django.contrib.auth.models import User
from rest_framework import serializers


class GeneratedEmailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article class. 
    """
    # The following fields will not be required.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = GeneratedEmail
        fields = ('description', 'email', 'forward', 'visibility', 'owner')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    emails = serializers.HyperlinkedRelatedField(
        many=True, view_name='generatedemail-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'emails')
