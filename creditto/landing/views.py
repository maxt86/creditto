from django.shortcuts import render
from django.shortcuts import redirect

from django.views import View


class IndexView(View):
    
    def get(self, request, *args, **kwargs):
        return (
            render(request, 'landing/index.html'),
            redirect('posts'),
        )[request.user.is_authenticated]
