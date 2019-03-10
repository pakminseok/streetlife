# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .forms import UserLoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
# Create your views here.

from .models import SpotPost, StreetPost
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def Home(request):
	query = request.GET.get("query")
	if query:
		street_list =  StreetPost.objects.all().filter(
			Q(title__contains=query) |
			Q(content__contains=query) |
			Q(city__contains=query)  |
			Q(category__contains=query) 
			).distinct()
		return render(request, 'street_list.html', {
			'street_list': street_list,
			})
	return render(request, 'home.html', {})

def Overview(request):
	name = 'hello streetlife'

	args = {'myName' : name}
	return render(request, 'overview.html', args)

def Spot(request):
	spot_list = SpotPost.objects.all()
	return render(request, 'spot_list.html', {
			'spot_list': spot_list,
		})

def Spot_detail(request, pk):
	spot = get_object_or_404(SpotPost, pk=pk)
	return render(request, 'spot_detail.html', {
			'spot': spot
		})

def Popup_spot(request, pk):
	spot = get_object_or_404(SpotPost, pk=pk)
	return render(request, 'popup_spot.html', {
			'spot': spot
		})

@login_required(redirect_field_name='/login/')
def Create(request):
	return render(request, 'create.html')

@login_required(redirect_field_name='/login/')
def Create_Spot(request):
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get("content")
		photo = request.FILES.get("photo")
		latitude = request.POST.get("lat")
		longitude = request.POST.get("lng")

		obj = SpotPost.objects.create(
			title = title,
			content = content,
			photo = photo,
			latitude = latitude,
			longitude = longitude,
			spot_user = request.user,
			)
		return HttpResponseRedirect("/spot/")
	context={}
	return render(request, 'create_spot.html', context)

@login_required(redirect_field_name='/login/')
def Create_Street(request):
	spot_list = SpotPost.objects.all()
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get("content")
		category = request.POST.get("category")
		city = request.POST.get("city")
		
		spots = request.POST.getlist("spots")

		obj = StreetPost.objects.create(
			title = title,
			content = content,
			category = category,
			city = city,
			user = request.user,
			)
		for spot_id in spots:
			obj.spots.add(SpotPost.objects.get(id=spot_id))
		return HttpResponseRedirect("/street/")
	context={'spot_list': spot_list}
	return render(request, 'create_street.html', context)

def Street(request):
	street_list = StreetPost.objects.all()

	query = request.GET.get("query")
	if query:
		street_list = street_list.filter(
			Q(title__contains=query) |
			Q(content__contains=query) |
			Q(city__contains=query)  |
			Q(category__contains=query) 
			).distinct()

	return render(request, 'street_list.html', {
			'street_list': street_list,
		})
def Street_detail(request, pk):
	street = get_object_or_404(StreetPost, pk=pk)
	spots = street.spots.all()
	is_recommended= False
	if street.recommends.filter(id=request.user.id).exists():
		is_recommended = True
	return render(request, 'street_detail.html', {
			'street': street,
			'spots' : spots,
			'total_recommend' : street.total_recommend(),
			'is_recommended' : is_recommended
		})
@login_required(redirect_field_name='/login/')
def Delete_Spot(request, pk):
	spot = get_object_or_404(SpotPost, pk=pk)
	if request.user != spot.spot_user:
		raise Http404()
	if request.method == "POST":
		spot.delete()
		return HttpResponseRedirect("/spot/")
	context={'spot': spot}
	return render(request, 'delete_spot.html', context)

@login_required(redirect_field_name='/login/')
def Delete_Street(request, pk):
	street = get_object_or_404(StreetPost, pk=pk)
	if request.user != street.user:
		raise Http404()
	if request.method == "POST":
		street.delete()
		return HttpResponseRedirect("/street/")
	context={'street': street}
	return render(request, 'delete_street.html', context)
@login_required(redirect_field_name='/login/')
def Edit_Spot(request, pk):
	spot = get_object_or_404(SpotPost, pk=pk)
	if request.user != spot.spot_user:
		raise Http404()
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get("content")
		latitude = request.POST.get("lat")
		longitude = request.POST.get("lng")

		obj = SpotPost.objects.filter(pk=pk)
		obj.update(
			title = title,
			content = content,
			latitude = latitude,
			longitude = longitude
			)
		update_img = SpotPost.objects.get(pk=pk)
		update_img.photo = request.FILES.get("photo")
		update_img.save()
		return HttpResponseRedirect("/spot/")
	
	context={'spot': spot}
	return render(request, 'edit_spot.html', context)	

@login_required(redirect_field_name='/login/')
def Edit_Street(request, pk):
	spot_list = SpotPost.objects.all()
	street = get_object_or_404(StreetPost, pk=pk)
	if request.user != street.user:
		raise Http404()
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get("content")
		category = request.POST.get("category")
		city = request.POST.get("city")
		
		spots = request.POST.getlist("spots")
		
		StreetPost.objects.filter(pk=pk).update(
			title = title,
			content = content,
			category = category,
			city = city,
		)
		obj = StreetPost.objects.get(pk=pk)
		obj.spots.clear()
		for spot_id in spots:
			obj.spots.add(SpotPost.objects.get(id=spot_id))
		return HttpResponseRedirect("/street/")
	context={
		'spot_list': spot_list,
		'street' : street
	}
	return render(request, 'edit_street.html', context)	

def register(request):
	if request.method =='POST':
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			return HttpResponseRedirect('/')
	else:
		form = RegistrationForm()
	context = {
		'form' : form,
	}
	return render(request, 'reg_form.html', context)

def User_Login(request):
	if request.method =='POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = request.POST.get("username")
			password = request.POST.get("password")
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/')
				else:
					return HttpResponse('User is not active')
			else:
				return HttpResponse('User is not exist. Check your ID or PassWord.')
	else:
		form = UserLoginForm()

	context = {
		'form' : form,
	}
	return render(request, 'login.html', context)

def User_Logout(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(redirect_field_name='/login/')
def Recommend(request, pk):
	street = get_object_or_404(StreetPost, pk=pk)
	is_recommended = False
	if street.recommends.filter(id=request.user.id).exists():
		street.recommends.remove(request.user)
		is_recommended = False
	else:
		street.recommends.add(request.user)
		is_recommended = True
	return HttpResponseRedirect(street.get_absolute_url())