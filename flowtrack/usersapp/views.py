from django.shortcuts import render, redirect
from .forms import UserInfoForm, UserPreferencesForm, UserPaginationForm, UserSortPreferences
from .models import UserSettings

def settings(request):
    settings = UserSettings.objects.get_or_create(user=request.user)[0]
    edit = request.GET.get('edit', '')
    infoform = UserInfoForm(instance=settings)
    preferencesform = UserPreferencesForm(instance=settings)
    userpaginationform = UserPaginationForm(instance=settings)
    usersortpreferences = UserSortPreferences(instance=settings)

    if request.method == "POST":
        edit = request.POST.get('edit')
        if edit == "infoform":
            infoform = UserInfoForm(request.POST, instance=settings)
            if infoform.is_valid():
                infoform.save()
            return redirect('settings')
        if edit == "preferencesform":
            preferencesform = UserPreferencesForm(request.POST, instance=settings)
            if preferencesform.is_valid():
                preferencesform.save()
            return redirect('settings')
        if edit == "userpaginationform":
            userpaginationform = UserPaginationForm(request.POST, instance=settings)
            if userpaginationform.is_valid():
                userpaginationform.save()
            return redirect('settings')
        if edit == "usersortpreferences":
            usersortpreferences = UserSortPreferences(request.POST, instance=settings)
            if usersortpreferences.is_valid():
                usersortpreferences.save()
            return redirect('settings')
        
    context = {
        "edit": edit,
        "infoform": infoform,
        "preferencesform": preferencesform,
        "userpaginationform": userpaginationform,
        "usersortpreferences": usersortpreferences,
        "settings": settings,
    }
    return render(request, "usersapp/settings.html", context)

def index(request):
    return render(request, "index.html")