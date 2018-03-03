# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Quotes
from django.contrib import messages
from django.db.models import Count

def index(request):
    return render(request, 'quotes/index.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def submit_register(request):
    goto = "/quotes"
    response = User.objects.createUser(request.POST)
    #if response was successful put user info in session
    if response['status']:
        request.session['alias'] = response['user'].alias
        request.session['user_id'] = response['user'].id
        return redirect('/quotes')
    #else show error messages
    else:
        for error in response['errors']:
            messages.error(request, error)
            goto = "/"
    return redirect(goto)

def submit_signin(request):
    goto = "/"
    response = User.objects.login_validation(request.POST)
    if response['status']:
        request.session['alias'] = response['user'].alias
        request.session['user_id'] = response['user'].id
        return redirect('/quotes')
    else:
        for error in response['errors']:
            messages.error(request, error)
            return redirect(goto)
    return redirect(goto)


def logon(request):
    me = User.objects.get(id=request.session['user_id'])
    my_quotes = me.favorited_by.all()
    t = Quotes.objects.exclude(favorites = me)
    context = { 
        'user' : me, 'q': t, 'myfav': my_quotes
    }
    return render(request, 'quotes/allquotes.html', context)

def submit_quote(request):
    author = User.objects.get(id=request.POST['author_id'])
    if len(request.POST['text']) < 10:
        messages.error(request, 'Quote message needs to be at least 10 characters.')
        if len(request.POST['quote_by']) < 3:
            messages.error(request, 'Quoted by needs at least 3 characters.')
        return redirect('/quotes')
    else:
        Quotes.objects.create(text=request.POST['text'], quote_by=request.POST['quote_by'], author=author)
    return redirect('/quotes')

def uprof(request, id):
    t =  Quotes.objects.values('quote_by').annotate(Count('id'))
    context = {
        'user': User.objects.get(id=id), 
        'quote': t,
        'q': Quotes.objects.all()
    }
    return render(request, 'quotes/userquotes.html', context)

def add_quote(request, id):
    me = User.objects.get(id=request.session['user_id'])
    myquote = Quotes.objects.get(id=id)
    me.favorited_by.add(myquote)
    return redirect('/quotes')

def remove_quote(request, id):
    me = User.objects.get(id=request.session['user_id'])
    myquote = Quotes.objects.get(id=id)
    me.favorited_by.remove(myquote)
    return redirect('/quotes')
