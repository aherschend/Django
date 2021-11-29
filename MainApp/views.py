from django.shortcuts import render

from .models import Topic

# Create your views here.

def index (request):
    return render(request, 'MainApp/index.html')

#whatever you define in urls file has to be the same - so for here it's "Topics"
def topics(request):
    topics = Topic.objects.order_by('-date_added') # - sign sorts it by descending

# the key is the variable used in the html template file and the value of the dictionary is the
# variable used in the view function
# most of the time the dictionary is named context in Django
    context = {'topics':topics}

    return render(request, 'MainApp/topics.html', context) # pass the dictionary to the html file

def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)

    entries = entries = topic.entry_set.all()

    context = {'topic':topic, 'entries':entries}

    return render(request, 'MainApp/topic.html', context)

