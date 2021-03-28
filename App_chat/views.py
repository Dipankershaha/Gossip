from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
# from chat.models import Thread, Message
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from django.shortcuts import redirect
from .models import Thread, Message
from django.contrib.auth.models import User



class ThreadView(View):
    template_name = 'App_Chat/chat.html'

    def get_queryset(self):
        print("query")
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        print("get object")
        other_username  = self.kwargs.get("username")
        self.other_user = get_user_model().objects.get(username=other_username)
        obj = Thread.objects.get_or_create_personal_thread(self.request.user, self.other_user)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        print("Get Conext")
        context = {}
        context['me'] = self.request.user
        print(context['me'])
        context['thread'] = self.get_object()
        context['user'] = self.other_user
        context['messages'] = reversed(self.get_object().message_set.all())
        
        return context

    def get(self, request, **kwargs):
        print("get")

        self.user = None 
        if request.user.is_authenticated:
            self.user = request.user
        else:
            try:
                token = parse_qs(request.scope["query_string"].decode("utf*"))["token"][0]
                token = Token.objects.get(key=token)
                self.user = token.user
            except KeyError:
                pass
        if self.user:
            context = self.get_context_data(**kwargs)
            print("hello")
            print(self.template_name)
            if request.GET.get('search',''):
                search = request.GET.get('search','')
                print("nothing")
                result = User.objects.filter(username__icontains=search)
                return render(request, 'App_Posts/home.html',context={'title':'Home','search':search,'result':result,})
            return render(request, self.template_name, context=context)

        else:
            return redirect('/admin/login/?next=' + request.path)

    def post(self, request, **kwargs):
        print("Post")
        
        self.object = self.get_object()
        thread = self.get_object()
        data = request.POST
        user = request.user
        text = data.get("message")
        Message.objects.create(sender=user, thread=thread, text=text)
        context = self.get_context_data(**kwargs)
        
        return render(request, self.template_name, context=context)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error':'Invalid Credentials'},
        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    print(token.key)
    return Response({'token':token.key},
    status=status.HTTP_200_OK)