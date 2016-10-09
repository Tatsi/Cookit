from django.shortcuts import render

def mainpage(request):
	context = {}
	return render(request, 'mainpage.html', context)


#def login(request):
#    return render(request, "login.html", {})