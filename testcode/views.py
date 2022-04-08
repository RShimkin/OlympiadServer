import os
import subprocess
import datetime as dt
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from testcode.forms import *
from testcode.models import *

def run_cpp(code, lang):
    fname = "main.cpp"
    outname = f"outmain"

    file = open(fname,"w")
    file.write(code)
    file.close()

    command = f"g++ {fname} -o {outname}"
    arr = command.split(' ')
    res = subprocess.run(arr, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # subprocess.run(arr, capture_output=True, text=True)
    compout = res.stdout.decode('utf-8')
    comperr = res.stderr.decode('utf-8')

    success = True

    if comperr != "":

        if "not declared in this scope" in comperr:
            comperr = "Странный идентификатор"
        elif "redefinition" in comperr:
            comperr = "Переопределение!"
        elif "abstract declarator" in comperr:
            comperr = "Абстрактный декларатор"
        elif "conversion from" in comperr:
            comperr = "Ошибка приведения типов"
        elif "could not convert" in comperr:
            comperr = "Ошибка приведения к bool"
        elif "statement cannot resolve address of overloaded function" in comperr:
            comperr = "Не хватает скобок при вызове функции"
        elif "is private within this context" in comperr:
            comperr = "Обращение к приватному свойству"
        elif "is not a type" in comperr:
            comperr = "Странный тип..."

        os.remove(fname)
        success = False
        
    return success, fname, outname, compout, comperr

def test_create(code):
    folder = f"{str(dt.datetime.now()).replace(' ','').replace(':','')}"
    os.mkdir(f'works\{folder}')
    fname = f"works\{folder}\main.cpp"
    outname = f"works\{folder}\outmain"

    file = open(fname,"w")
    file.write(code)
    file.close()

    command = f"g++ {fname} -o {outname}"
    arr = command.split(' ')
    res = subprocess.run(arr, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

def test_cpp(code):
    fname = "main.cpp"
    outname = f"outmain"

    file = open(fname,"w")
    file.write(code)
    file.close()

    command = f"g++ {fname} -o {outname}"
    arr = command.split(' ')
    res = subprocess.run(arr, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # subprocess.run(arr, capture_output=True, text=True)
    compout = res.stdout.decode('utf-8')
    comperr = res.stderr.decode('utf-8')

    success = True

    if comperr != "":

        if "not declared in this scope" in comperr:
            comperr = "Странный идентификатор"
        elif "redefinition" in comperr:
            comperr = "Переопределение!"
        elif "abstract declarator" in comperr:
            comperr = "Абстрактный декларатор"
        elif "conversion from" in comperr:
            comperr = "Ошибка приведения типов"
        elif "could not convert" in comperr:
            comperr = "Ошибка приведения к bool"
        elif "statement cannot resolve address of overloaded function" in comperr:
            comperr = "Не хватает скобок при вызове функции"
        elif "is private within this context" in comperr:
            comperr = "Обращение к приватному свойству"
        elif "is not a type" in comperr:
            comperr = "Странный тип..."

        os.remove(fname)
        success = False
        
    return success, fname, outname, compout, comperr

def run_cs(code, lang):
    fname = "main.cs"
    outname = "main.exe"

    file = open(fname,"w")
    file.write(code)
    file.close()

    command = f"..\CompileCS.cmd {fname}"
    arr = command.split(' ')
    res = subprocess.run(arr, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # subprocess.run(arr, capture_output=True, text=True)
    compout = res.stdout.decode('CP866')
    comperr = res.stderr.decode('utf-8')

    success = True

    if comperr != "":
        os.remove(fname)
        success = False
        
    return success, fname, outname, compout, comperr

def run_tests(fname, curtask):
    points = 0
    tests = curtask.tests
    input_fname = "args.txt"
    for test in tests:
        inp = test['testinput']
        outp = test['testoutput']

        file = open(input_fname, "w")
        file.write(inp)
        file.close()

        arr = [fname, input_fname]
        res = subprocess.run(arr, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        out = res.stdout.decode('utf-8')
        err = res.stderr.decode('utf-8')

        if err != "":
            return (False, err, 0)
        
        if out != outp:
            print('outp', outp)
            print('out', out)
        else:
            points += 1
    
    score = (points * curtask.points) // len(tests)

    if os.path.isfile(fname):
        os.remove(fname)
    if os.path.isfile('args.txt'): 
        os.remove('args.txt')

    return (True, "", score)

def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'testcode/tasks.html', {'title': 'Задачи','tasks': tasks})

# @login_required(login_url='signup')
@csrf_exempt
def task(request, task_name):

    #print(request.POST)

    curtask = Task.objects.get(name=task_name)
    err = out = comperr = compout = score = ""

    if request.method == 'POST':
        form = CodeForm(request.POST)

        if form.is_valid():
            formcontent = form.cleaned_data
            lang =  formcontent['plang']
            code = formcontent['content']

            if lang == "C++":
                res, cppname, fname, compout, comperr = run_cpp(code, lang)
                fname = f"{fname}.exe"
            elif lang == "C#":
                res, cppname, fname, compout, comperr = run_cs(code, lang)
            
            if res:
                res, err, score = run_tests(fname, curtask)
                if res:
                    un = 'stranger'
                    if request.user.is_authenticated:
                        un = request.user.username
                    result = Result(
                        uname = un,
                        taskname = curtask.name,
                        points = score,
                    )
                    result.save()
                    curtask.results.add(result)
                    curtask.save()
                
            if os.path.isfile(cppname):
                os.remove(cppname)

            context = {
                'cerror': comperr, 'cout': compout, 'out': out, 'err': err, 'score': score 
            }

            return JsonResponse(context, status=200)
        else:
            print('invalid form')
            return JsonResponse({ 'text': 'invalid form' }, status=400)

    else:
        form = CodeForm()

    rating = list(curtask.results.all())

    return render(request, 'testcode/task.html', {
        'task': curtask, 'title': 'Отправка кода', 'form': form, 
        'cerror': comperr, 'cout': compout, 'out': out, 'err': err, 'score': score, 'rating': rating })

def code(request):
    #print(request.POST)
    #print(request.headers)
    err = out = comperr = compout = ""
    if request.method == 'POST':
        form = MyCodeForm(request.POST)
        if form.is_valid():
            formcontent = form.cleaned_data
            code = formcontent['content']
            test_create(code)
        else:
            print('invalid form')
    else:
        form = MyCodeForm()

    return render(request, 'testcode/code.html', 
           {'title': 'Отправка кода', 'form': form, 'cerror': comperr, 'cout': compout, 'out': out, 'err': err})

def ajax(request):
    print (request.POST)
    return JsonResponse("OK")
