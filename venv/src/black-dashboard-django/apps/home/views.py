# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from .models import join_eval
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
import json
import re

@csrf_protect
def index(request):

    #final = join_final.objects.all()
    #context = {"hospital": final}
    if 'sido' in request.POST.keys():
        sido = request.POST['sido']
        gugun = request.POST['gugun']
        disease = [int(request.POST['disease'])]
        tmp = join_eval.objects.filter(addr__contains=sido) & join_eval.objects.filter(addr__contains=gugun) &\
                join_eval.objects.filter(srch_list__contains = disease)
        context = {"hos": tmp[0]}
        print("[DEBUG] context: ", tmp[0].addr)
        return render(request, 'home/index.html', context)
    else:
        html_template = loader.get_template('home/index.html')
        print("[DEBUG] index is being called")
        return HttpResponse(html_template.render({}, request))


@csrf_protect
def receive(request):
    if request.method == 'POST':
        print("[DEBUG] receive POST is being called")
        sido    = request.POST['sido']
        gugun   = request.POST['gugun']
        disease = [int(request.POST['disease'] )]
        tmps = join_eval.objects.filter(addr__contains=sido) & join_eval.objects.filter(addr__contains=gugun) &\
                join_eval.objects.filter(srch_list__contains = disease)
        
        addr_list = []
        name_list = []
        asmgrd_list = []
        #top5_list = []
        for tmp in tmps:
            addr = tmp.addr.split(' ')
            addr[3] = re.sub("[^\d\.]", "", addr[3])
            addr_list.append("{} {} {} {}".format(addr[0], addr[1], addr[2], addr[3]))
            name_list.append(tmp.name)
            asmgrd_list.append(tmp.asmGrdList)
            #top5_list.append(tmp.top5)
        print(addr_list)
        #print(top5_list)
        request.session['addr'] = ','.join([str(i) for i in addr_list])
        request.session['name'] = json.dumps(name_list)
        request.session['asmgrdlist'] = json.dumps(asmgrd_list)
        #request.session['top5'] = json.dumps(top5_list)
        print(name_list)
        print(request.session['asmgrdlist'])


        #request.session['addr'] = json.dumps(addr_list)
        #return HttpResponseRedirect(reverse('receive'))
        return redirect('/receive')
    else:
        print("[DEBUG] request GET is called")
        return render(request, 'home/receive.html', context = {})
    

@csrf_protect
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        print("pages function is called")
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def post_detail(request, pk):
    ret = Post.__class__.objects.all()
    print(ret)
    return render(request, "post_detail.html", context)

