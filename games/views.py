from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
def home(request):
    context = {"message": "This came from the view."}
    return render(request, "games/home.html", context)