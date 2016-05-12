from django.http import HttpResponse

def under_construction(request):
    html = "<html><body>Under construction. Please come back later. (Saludos a JJ)</body></html>"
    return HttpResponse(html)