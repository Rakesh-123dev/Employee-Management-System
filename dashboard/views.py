from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employee



# Create your views here.
@login_required
def home(request):
    query = request.GET.get('query', '').strip().lower()
    sort_by = request.GET.get('sort', '').strip().lower()
    page = int(request.GET.get('page','1'))
    employees = list(Employee.objects.all())
    
    department = request.GET.get('department', '')

    if department:
        # employees = [emp for emp in employees if emp.department == department]
        employees = Employee.objects.filter(department=department)
    else:
        employees = Employee.objects.all()
    departments = Employee.objects.values_list('department', flat=True).distinct()

    if query:
        filtered = []
        for emp in employees:
            if(
                query in emp.name.lower() or
                query in emp.email.lower() or
                query in str(emp.phone).lower()
            ):
                 filtered.append(emp)
        employees = filtered
    if sort_by == 'name':
        employees.sort(key=lambda emp: emp.name.lower())
    elif sort_by == 'email':
        employees.sort(key=lambda emp: emp.email.lower())
    elif sort_by == 'name_desc':
        employees.sort(key=lambda emp: emp.name.lower(), reverse=True)
        #  print('query', query)
        # print("filtered:", [e.name for e in employees])   
    per_page =2
    total = len(employees)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_employees = employees[start:end]
    total_pages = (total + per_page - 1)//per_page
    context = {
        'employees': paginated_employees,
        'page': page,
        'total_pages': total_pages,
        'query': query,
        'sort': sort_by,
        'department': department,
        'departments': departments,
    }
    return render(request,'dashboard/home.html', context)

def register_employee(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        address = request.POST.get('address')

        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exits")
            return render(request, 'dashboard/register.html')
        user = User.objects.create_user(username=username,password=password)

        Employee.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            department=department,
            address=address,
        )
        return redirect('home')
    return render(request, 'dashboard/register.html')

def edit_employee(request, id):
    try:
        employee = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        return redirect('home')
    
    if request.user != employee.user and not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone')
        employee.department = request.POST.get('department')
        employee.address = request.POST.get('address')
        employee.save()
        return redirect('home')

def delete_view(request, id):
    try:
        employee = Employee.objects.get(id=id)

        if request.user != employee.user and not request.user.is_staff:
            return redirect('home')

        # First delete the linked user account
        user = employee.user
        employee.delete()  # delete employee
        user.delete()      
    except Employee.DoesNotExist:
        return redirect('home')


    return redirect('home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(username=username,password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home')
        else:
            messages.error(request, 'error invalid credentials')
            return redirect('login')
    return render(request,'dashboard/login.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')



def add_employee(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        address = request.POST.get('address')

        new_employee = Employee()
        new_employee.user = request.user
        new_employee.name = name
        new_employee.email = email
        new_employee.phone = phone
        new_employee.department = department
        new_employee.address = address
        new_employee.save()
        return redirect('home')
    return render(request, 'dashboard/add_employee.html')