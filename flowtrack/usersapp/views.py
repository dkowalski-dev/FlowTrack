from django.shortcuts import render, redirect
from .forms import UserInfoForm, UserPreferencesForm
from .models import UserSettings

def settings(request):
    settings = UserSettings.objects.get_or_create(user=request.user)[0]
    infoform = UserInfoForm(instance=settings)
    preferencesform = UserPreferencesForm(instance=settings)

    if request.method == "POST":
        infoform = UserInfoForm(request.POST, instance=settings)
        preferencesform = UserPreferencesForm(request.POST, instance=settings)
        if infoform.is_valid() and preferencesform.is_valid():
            infoform.save()
            preferencesform.save()
            return redirect('offers')
    context = {
        "infoform": infoform,
        "preferencesform": preferencesform
    }
    return render(request, "usersapp/settings.html", context)