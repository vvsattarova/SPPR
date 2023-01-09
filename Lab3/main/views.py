from django.shortcuts import render, redirect
from .models import Task
from .models import Prediction
from .animeprediction import predict_anime
from .forms import TaskForm


def index(request):
    tasks = Task.objects.order_by('-id')
    return render(request, 'main/index.html', {'title': 'Главная страница сайта', 'tasks': tasks})


def about(request):
    task = Task.objects.first()
    index_user = int(task.title)
    predicted_list = predict_anime(index_user)
    predicted = Prediction.objects.create(
        pred1=predicted_list[0],
        pred2=predicted_list[1],
        pred3=predicted_list[2],
        pred4=predicted_list[3],
        pred5=predicted_list[4],
        pred6=predicted_list[5]
    )
    return render(request, 'main/about.html', {'predicted': predicted})


def create(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'

    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)


def delete(request):
    tasks = Task.objects.all()
    tasks.delete()
    predicted = Prediction.objects.all()
    predicted.delete()
    return render(request, 'main/delete.html')
