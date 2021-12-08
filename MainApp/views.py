from django.shortcuts import redirect, render
from .forms import EntryForm, TopicForm
from .models import Topic, Entry
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.

def index (request):
    return render(request, 'MainApp/index.html')

@login_required
#whatever you define in urls file has to be the same - so for here it's "Topics"
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added') # - sign sorts it by descending

# the key is the variable used in the html template file and the value of the dictionary is the
# variable used in the view function
# most of the time the dictionary is named context in Django
    context = {'topics':topics}

    return render(request, 'MainApp/topics.html', context) # pass the dictionary to the html file



@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = entries = topic.entry_set.all()

    context = {'topic':topic, 'entries':entries}

    return render(request, 'MainApp/topic.html', context)
@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid(): #makes sure form complies with the rules of your model
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            #redirect user to main page
            return redirect('MainApp:topics')

    context = {'form':form}
    return render(request, 'MainApp/new_topic.html',context)
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic 
            new_entry.save()
            form.save()
            return redirect('MainApp:topic',topic_id=topic_id)

    context = {'form':form, 'topic':topic}
    return render(request, 'MainApp/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    #Edit an existing entry.
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance = entry)
    else:
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('MainApp:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic':topic, 'form':form}
    return render (request, 'MainApp/edit_entry.html', context)


