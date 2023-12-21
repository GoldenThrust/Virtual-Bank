from django.shortcuts import render, redirect
from .models import Notification
from django.http import JsonResponse, Http404

def read_notification(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        notification = Notification.objects.filter(user=request.user, pk=id).first()
        if notification:
            notification.status = 'READ'
            notification.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed'})
    raise Http404()