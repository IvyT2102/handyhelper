from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Job, User, UserManager, Category
import bcrypt

# Create your views here.


def index(request):
    request.session.flush()
    return render(request, 'index.html')


def register(request):  # post redirect
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # hash the password
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # create a user
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST[
                'last_name'], email=request.POST['email'], password=hashed_pw
        )
        # create a session
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')
    return redirect('/')


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/dashboard')
    return redirect('/')
# log out
def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'this_user': User.objects.get(id=request.session['user_id']),
        'jobs': Job.objects.all()
        
    }

    return render(request, 'dashboard.html', context)

def new(request):
    context={
        'all_categories': Category.objects.all()[:3],
    }
    return render(request, 'new.html', context)

def add_a_job(request):
    errors = Job.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')

    # if request.method != 'POST' or 'user_id' not in request.session:
    #     return redirect('/')
    
    this_user = User.objects.get(id= request.session['user_id'])
    # print(request.POST)
    # print(f"categories: {request.POST['categories']}")
    # print(f"getlist: {request.POST.getlist('categories')}")
    # jobs = Job.objects.all()
    new_job=Job.objects.create(
        title = request.POST['title'],   
        description = request.POST['description'],
        location = request.POST['location'],
        created_by = this_user
    )
    # get the list of categories
    for cat_id in request.POST.getlist('categories'):
        # add those categories to the new job
        new_job.categories.add(Category.objects.get(id = cat_id))
    # if there is a new category
    if len(request.POST['new_category'])>0:
        # check if the category already exists
        existing_category = Category.objects.filter(name = request.POST['new_category'])
        if len(existing_category) > 0:
            new_job.categories.add(existing_category[0])
        else:
            # create new category
            other_category= Category.objects.create(name = request.POST['new_category'])
            # add that category to the new job
            new_job.categories.add(other_category)

    return redirect('/dashboard')

def edit(request, job_id):
    one_job = Job.objects.get(id=job_id)
    contex = {
        'job': one_job
    }
    return render(request, 'edit.html', contex)

def update(request, job_id):
    errors = Job.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{job_id}/edit')

    to_update = Job.objects.get(id=job_id)
    to_update.title = request.POST['title']
    to_update.location = request.POST['location']
    to_update.description = request.POST['description']
    to_update.save()
    return redirect('/dashboard')

def job(request, job_id):
    one_job = Job.objects.get(id=job_id)
    context = {
        'this_user': User.objects.get(id=request.session['user_id']),
        'job': one_job
    }
    return render(request, 'job.html', context)

def add_to(request, job_id):
    this_user = User.objects.get(id=request.session["user_id"])
    one_job = Job.objects.get(id=job_id)
    this_user.added_jobs.add(one_job)

    return redirect('/dashboard')

def remove_from(request, job_id):
    this_user = User.objects.get(id=request.session["user_id"])
    one_job = Job.objects.get(id=job_id)
    this_user.added_jobs.remove(one_job)

    return redirect('/dashboard')


def delete(reuqest, job_id):
    to_delete = Job.objects.get(id=job_id)
    to_delete.delete()
    return redirect('/dashboard')