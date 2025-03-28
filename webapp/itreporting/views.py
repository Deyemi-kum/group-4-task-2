from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Module, Student, Registration
from .forms import StudentProfileForm

def home(request):
    username = request.user.username if request.user.is_authenticated else 'Guest'
    return render(request, 'home.html', {'username': username})

def course_page(request):
    modules = Module.objects.all()
    paginator = Paginator(modules, 5)  # Show 5 modules per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'course_page.html', {'modules': page_obj})

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to access this page.')
        return redirect('home')
    student = Student.objects.get(user=request.user)
    return render(request, 'profile.html', {'student': student})

def update_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to access this page.')
        return redirect('home')
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'update_profile.html', {'form': form})

def register_module(request, module_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Unauthorized access'})

    module = Module.objects.get(id=module_id)
    student = Student.objects.get(user=request.user)

    # Check if the student is already registered for the module
    if Registration.objects.filter(student=student, module=module).exists():
        return JsonResponse({'success': False, 'message': 'You are already registered for this module'})

    if module.is_open_for_registration:
        Registration.objects.create(student=student, module=module)
        return JsonResponse({'success': True, 'message': 'Registered successfully'})

    return JsonResponse({'success': False, 'message': 'Module is not open for registration'})

def unregister_module(request, module_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to unregister from a module.')
        return HttpResponseRedirect('/home/')  # Redirect to the welcome page

    try:
        module = Module.objects.get(id=module_id)
        student = Student.objects.get(user=request.user)

        # Delete the registration if it exists
        registration = Registration.objects.filter(student=student, module=module)
        if registration.exists():
            registration.delete()
            return JsonResponse({'success': True, 'message': 'Unregistered successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'You are not registered for this module'})

    except Module.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Module not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})

def my_registrations(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to access this page.')
        return redirect('home')
    student = Student.objects.get(user=request.user)
    registrations = Registration.objects.filter(student=student)
    return render(request, 'my_registrations.html', {'registrations': registrations})

def module_detail(request, module_code):
    module = Module.objects.get(code=module_code)
    registrations = Registration.objects.filter(module=module)
    return render(request, 'module_detail.html', {'module': module, 'registrations': registrations})
