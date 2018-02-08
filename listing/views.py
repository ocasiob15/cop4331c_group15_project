from django.shortcuts import render

# Create your views here.
def index (request):
  return render(request, "index.html", {})
def new (request):
  return render(request, "view.html", {})
def view (request):
  return render(request, "view.html", {})
def edit (request):
  return render(request, "edit.html", {})
def delete (request):
  return render(request, "delete.html", {})
