## Leftover things and pages from tutorial
from django.shortcuts import render
test_posts = [
    {
        'author':'bwarex',
        'title':'Blog Post 1',
        'content':'First post content',
        'data_posted':'October 7, 2020',
    },
    {
        'author':'Author 2',
        'title':'Blog Post 2',
        'content':'Second post content',
        'data_posted':'October 8, 2020',
    },
    ]

def test_home(request):
    # return HttpResponse('<h1>Hydroxychloroquine Home</h1>')
    context = {
        'title':'test_home',
        'test_posts':test_posts,
    }
    return render(request, 'Hydroxychloroquine/test_home.html', context)

def test_about(request):
    context = {
        'title':'test_about',
    }
    # return HttpResponse('<h1>Hydroxychloroquine About</h1>')
    return render(request, 'Hydroxychloroquine/test_about.html', context)

def test_base(request):
    context = {
        'title':'test_base',
    }
    return render(request, 'Hydroxychloroquine/test_base.html'), context
