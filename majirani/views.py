from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Neighbourhood, Business, Post,Comment
from .forms import SignUpForm, EditProfileForm, NeighbourhoodForm, CreatebizForm, PostForm, CommentForm
# Create your views here.

def welcome(request):
    return render(request,'welcome.html')
def Home(request):
    hoods = Neighbourhood.objects.all()
    return render(request, 'home.html', locals())

@login_required(login_url='/registration/login/')
def profile_edit(request):
    """
    view function to render profile

    """
    form = EditProfileForm()
    current_user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=current_user.profile)
        if form.is_valid():
            form.save()

            return redirect('profile')

    return render(request, 'profile_edit.html', {'form': form})

def updatebiz(request, id):
    """
    create business function
    :param request:
    :return:
    """
    bsns = Business.objects.get(id=id)
    if request.method == 'POST':
        form = CreatebizForm(request.POST, request.FILES, instance=bsns)
        if form.is_valid():
            b = form.save(commit=False)
            b.user = request.user.profile
            b.neighbourhood = request.user.profile.neighbourhood
            b.save()
        return redirect('neighbourhood', request.user.profile.neighbourhood.id)
    else:
        form = CreatebizForm()
    return render(request, 'createbisness.html', locals())


# profile view function
@login_required(login_url='/registration/login/')
def profile(request):
    """
    view function to render profile

    """
    current_user = request.user
    profile = Profile.objects.get(user =current_user)
    bsns = Business.objects.filter(user=current_user)
    post = Post.objects.filter(user= current_user)
    return render(request, 'profile.html', {'profile': profile, "bsns":bsns, "post":post})


# search for business in neighbourhood
def search_biz(request):
    if 'business' in request.GET and request.GET["business"]:
        search_biz =request.GET.get("business")
        searched_biz = Business.find_business(search_biz)
        message = f"{search_biz}"
        return render(request, 'search.html',{"message":message, "businesses":searched_biz})
    else:
        message ="Enter Business to Search For"
        return render(request, "search.html", {"message":message})


@login_required(login_url='/registration/login/')
def create_hood(request):
    """
    view function to create hood
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST, request.FILES)
        if form.is_valid():
            n = form.save(commit=False)
            n.admin = request.user.profile
            request.user.profile.save()
            n.save()
        return redirect('Home')
    else:
        form = NeighbourhoodForm()
    return render(request, 'createmyhood.html', {'form': form})


@login_required(login_url='/registration/login/')
def create_post(request):
    """
    view function to create posts
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            p =form.save(commit=False)
            p.user = request.user.profile
            p.neighbourhood = request.user.profile.neighbourhood
            p.save()
        return redirect('neighbourhood',request.user.profile.neighbourhood.id)
    else:
        form = PostForm
    return render(request, 'addpost.html', locals())


@login_required(login_url='/registration/login/')
def createbiz(request):
    """
    create business function
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CreatebizForm(request.POST, request.FILES)
        if form.is_valid():
            b = form.save(commit=False)
            b.user = request.user.profile
            b.neighbourhood = request.user.profile.neighbourhood
            b.save()
        return redirect('neighbourhood', request.user.profile.neighbourhood.id)
    else:
        form = CreatebizForm()
    return render(request, 'createbisness.html', locals())

@login_required(login_url='/registration/login/')
def neighbourhood(request, neighbourhood_id):
    """
    view function to render neighbourhood

    """
    comments = Comment.objects.all()
    form = CommentForm()
    hood = Neighbourhood.find_neighbourhood(neighbourhood_id)
    bsns = Business.objects.filter(neighbourhood=request.user.profile.neighbourhood)
    post = Post.objects.filter(neighbourhood=request.user.profile.neighbourhood)

    return render(request, 'Theneighbourhood.html',locals())


@login_required(login_url='/accounts/login/')
def enter_hood(request, neighbourhood_id):
    hood = get_object_or_404(Neighbourhood, pk=neighbourhood_id)
    request.user.profile.neighbourhood = hood
    request.user.profile.save()
    return redirect('neighbourhood',neighbourhood_id)
@login_required()
def exit_hood(request, neighbourhood_id):
    hood = get_object_or_404(Neighbourhood, pk=neighbourhood_id)
    if request.user.profile.neighbourhood == hood:
        request.user.profile.neighbourhood = None
        request.user.profile.save()
    return redirect('Home')

def comm(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comms = comment.save(commit=False)
            comms.user = request.user
            comms.post = post
            comms.save()
        return redirect('neighbourhood', request.user.profile.neighbourhood.id)
def about(request):
    return render(request,'aboutus.html')