from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SnippetModel, TagModel


class RegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error': 'password1 and password2 should be the same'})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already Exists'})
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account


class AddSnippetSerializer(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField()
    tag = serializers.CharField()


class UpdateSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source='tag.tag')
    class Meta:
        model = SnippetModel
        fields = ['title', 'text', 'tag']

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['id','tag']


class TagDetailsSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source='tag.tag')
    user = serializers.CharField(source='created_user.username')
    class Meta:
        model = SnippetModel
        fields = ['title', 'text', 'tag', 'user', 'datetime']


class OverviewSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='snippet_details',
        lookup_field='id'
    )
    class Meta:
        model = SnippetModel
        fields = ['url','title', 'text','datetime']