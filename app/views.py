from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as _login, logout as _logout
import json
from django_htmx.http import HttpResponseClientRedirect, HttpResponseLocation

@login_required(login_url='/login/')
def index(request):
    return render(request, 'app/index.html')

def login(request):
    if(request.method == "POST"):
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if(user is not None):
            _login(request, user)
            return HttpResponseLocation(reverse('index'))
        response = HttpResponse("""
        <div class="absolute top-10 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10" remove-me="2s">
            <div role="alert" class="alert alert-error animate__animated animate__backInDown">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>L'utente non risulta registrato oppure la password è errata</span>
            </div>                        
        </div>
        """)
        response.headers['HX-Retarget'] = 'body'
        response.headers['HX-Reswap'] = 'afterbegin'
        return response
    return render(request, 'app/login.html')

def register(request):
    if(request.method == "POST"):
        try:
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            response = HttpResponse("""
            <div class="absolute top-10 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10" remove-me="2s" hx-preserve="true">
                <div role="alert" class="alert alert-success animate__animated animate__backInDown">
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>Registrazione effettuata con successo!</span>
                </div>                    
            </div>
            <script>
            setTimeout(()=>{
                document.getElementById('redirect-to-login').click();
            }, 2000);
            </script>
            """ + "<a id='redirect-to-login' href='{}' hx-boost='true'></a>".format(reverse('login')))
            response.headers['HX-Retarget'] = 'body'
            response.headers['HX-Reswap'] = 'afterbegin'
        except Exception as e:
            print(e)
            response = HttpResponse("""
            <div class="absolute top-10 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10" remove-me="2s">
                <div role="alert" class="alert alert-error animate__animated animate__backInDown">
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>Sembra che l'utente risulti già registrato</span>
                </div>                        
            </div>
            """)
            response.headers['HX-Retarget'] = 'body'
            response.headers['HX-Reswap'] = 'afterbegin'
        return response
    return render(request, 'app/register.html')

def logout(request):
    _logout(request)
    return HttpResponseLocation(reverse('login'))

def chat(request):
    if(request.method == "POST"):
        response = HttpResponse("""
        <div class="chat chat-end animate__animated animate__backInRight">
            <div class="chat-bubble">{}</div>
        </div>
        """.format(request.POST['message']))
        response.headers['HX-Retarget'] = 'this'
        response.headers['HX-Reswap'] = 'beforebegin'
        return response
    return render(request, 'app/chat.html')