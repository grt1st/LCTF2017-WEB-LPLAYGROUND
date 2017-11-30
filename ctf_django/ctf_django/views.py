from django.shortcuts import HttpResponse, render, redirect

from ctf_django.html_parse import get_html_content
from ctf_django.safe import safe_request_url
from ctf_django.forms import UrlForm
from ctf_django.sess import randomword
from ctf_django.flag import FLAG


def index(request):
    if not request.session.get('name', False):
        request.session['name'] = randomword()

    try:
        user = request.session.get('name', 'None')
    except Exception as e:
        user = 'None'

    if user == 'administrator':
        return HttpResponse("here is your flag: %s" % FLAG)

    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['target']

            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://%s' % url

            try:
                r = safe_request_url(url, timeout=3)
            except Exception as e:
                return render(request, 'result.html', {'title': 'L Playground: Error happens', 'form': UrlForm(),
                        'user': user, 'url': url, 'status_code': e, 'web_title': "None", 'content': "None"})

            try:
                title, content = get_html_content(r.content)
            except Exception as e:
                return render(request, 'result.html', {'title': 'L Playground: Error happens', 'form': UrlForm(),
                        'user': user, 'url': url, 'status_code': e, 'web_title': "None", 'content': "None"})

            return render(request, 'result.html', {'title': 'L Playground', 'form': UrlForm(),
                        'user': user, 'url': url, 'status_code': r.status_code, 'web_title': title, 'content': content})
            #return redirect('/')
        else:
            return render(request, 'result.html', {'title': 'L Playground: Error happens', 'form': UrlForm(),
                        'user': user, 'url': "None", 'status_code': form.errors, 'web_title': "None", 'content': "None"})

    else:
        form = UrlForm()
        try:
            return render(request, 'base.html', {'title': 'L Playground', 'user': user, 'form': form})
        except Exception as e:
            return HttpResponse(e)
