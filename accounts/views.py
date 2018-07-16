from django.shortcuts import render,redirect
from accounts.forms import LoginForm


def main(request):
    if request.user.is_authenticated:
        return redirect('sales:mainpage')
    login_form = LoginForm(request.POST or None)
    context = { 'login_form': login_form }
    return render(request, 'registration/login.html',context)
