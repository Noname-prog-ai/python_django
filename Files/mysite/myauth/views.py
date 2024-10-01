from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from django.contrib.auth.models import User
from .models import Profile

class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        login(self.request, self.object)
        return response

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")

@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")

@login_required

def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})

@login_required
def about_me(request):
    profile = request.user.profile
    return render(request, 'myauth/about_me.html', {'profile': profile})

@login_required
def edit_avatar(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('myauth:about-me')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'myauth/edit_avatar.html', {'form': form})

def user_list(request):
    users = User.objects.all()
    return render(request, 'myauth/user_list.html', {'users': users})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    return render(request, 'myauth/user_detail.html', {'user': user, 'profile': profile})
