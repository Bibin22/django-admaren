from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework_simplejwt.tokens import AccessToken




class RegistrationView(APIView):
    def post(self, request):
        permission_class = [IsAuthenticated]
        if request.method == 'POST':
            serializer = RegistrationSerializers(data=request.data)
            data = {}
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = "Registrations Sucessfull"
                data['username'] = account.username
                data['email'] = account.email
                refresh = RefreshToken.for_user(account)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

            else:
                data = serializer.errors

            return Response(data, status=status.HTTP_201_CREATED)


class OverViewAPI(APIView):
    def get(self, request):
        snippet = SnippetModel.objects.all()
        serializers = OverviewSerializer(snippet, many=True, context={'request':request})
        return Response(serializers.data)


class CreateAPI(APIView):
    def post(self, request, id):
        permission_class = [IsAuthenticated]
        serializer = AddSnippetSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get("title")
            text = serializer.validated_data.get("text")
            tag = serializer.validated_data.get("tag")
            access_token_str = id
            access_token_obj = AccessToken(access_token_str)
            user_id = access_token_obj['user_id']
            print(user_id)
            user = User.objects.get(id=user_id)
            print(user.username)
            tag_exists = TagModel.objects.filter(tag=tag).exists()
            if not tag_exists:
                tag = TagModel.objects.create(tag=tag)
            else:
                tag = TagModel.objects.get(tag=tag)
            snippet = SnippetModel.objects.create(title=title, text=text, tag=tag, created_user=user)

            data = [
                {
                    'title': snippet.title,
                    'text': snippet.text,
                    'tag': snippet.tag.tag,
                    'response': "Snippet Created Successfully"
                }
            ]
            return Response(data)


class DetailsAPI(APIView):
    def get(self, request, id):
        try:
            snippet = SnippetModel.objects.get(id=id)

            result = {
                "title": snippet.title,
                "text": snippet.text,
                "tag": snippet.tag.tag,
                "created_user": snippet.created_user.username,
                "created_at": snippet.datetime.strftime('%d-%m-%Y, %H:%M:%S'),

            }
            return Response(result)


        except:
            result = {
                "msg": "No Snippets"
            }
            return Response(result, status=status.HTTP_204_NO_CONTENT)


class UpdateAPI(APIView):
    serializer_class = UpdateSerializer

    def get(self, request, id):
        try:
            snipet = SnippetModel.objects.get(id=id)
            serializer = UpdateSerializer(snipet)
            return Response(serializer.data)
        except:
            result = {
                "msg": "No Snippets on this id"
            }
            return Response(result, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        try:
            snipet = SnippetModel.objects.get(id=id)
            data = request.data
            serializer = UpdateSerializer(snipet, data=request.data)
            if serializer.is_valid():
                tag = data['tag']
                tag_exists = TagModel.objects.filter(tag=tag).exists()
                if not tag_exists:
                    tag = TagModel.objects.create(tag=tag)
                else:
                    tag = TagModel.objects.get(tag=tag)
                snipet.title = data['title']
                snipet.text = data['text']
                snipet.tag = tag
                snipet.save()
                res = {
                    'title': snipet.title,
                    'text': snipet.text,
                    'tag': snipet.tag.tag,
                    'response': "Snippet Updated Successfully"
                }

                return Response(res)
        except:
            result = {
                "msg": "No Snippets on this id"
            }
            return Response(result, status=status.HTTP_204_NO_CONTENT)


class DeleteAPI(APIView):
    def delete(self, request, id):
        try:
            SnippetModel.objects.get(id=id).delete()
            snipet = SnippetModel.objects.all()
            serializers = AddSnippetSerializer(snipet, many=True)

            return Response(serializers.data)
        except:
            return Response("matching query does not exist.")


class TagListAPI(APIView):
    def get(self, request):
        tags = TagModel.objects.all()
        serializers = TagListSerializer(tags, many=True)
        return Response(serializers.data)


class TagDetailsAPI(APIView):
    def get(self, request, id):
        try:
            snippet = SnippetModel.objects.filter(tag_id=id)
            serializers = TagDetailsSerializer(snippet, many=True)
            return Response(serializers.data)
        except:
            result = {
                "msg": "No Snippets on this id"
            }
            return Response(result, status=status.HTTP_204_NO_CONTENT)

