from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic

from .models import Choice, Poll


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

from .forms import ContactForm, AcceptForm

from django.core.mail import send_mail

def get_contact(request,step=0):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if int(step)==2:
            form = ContactForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
    #            subject = form.cleaned_data['subject']
    #            message = form.cleaned_data['message']
                sender = form.cleaned_data['sender']
#                cc_myself = form.cleaned_data['cc_myself']
                male_num = form.cleaned_data['male_num']
                female_num = form.cleaned_data['female_num']
                
                request.session['sender']=sender
                request.session['male_num']=male_num
                request.session['female_num']=female_num
            
                form = AcceptForm()
                
                m=int(request.session['male_num'])
                f=int(request.session['female_num'])
                prod=m*f
                rs=prod*10
                text=u"Para %s homens e %s mulheres, sugerimos %s \
                    produtos na sua cesta, por %s reais!" %(m,f,prod,rs)
                request.session['step']=3
                return render(request, 'polls/name.html', 
                              {'form': form,'text':text,'step':3,'button_text':'Gostei!'})
        elif int(step)==3:# request.session.get('step',1)==3:
            form = AcceptForm(request.POST)
            if form.is_valid():
                accepted= form.cleaned_data['accepted']
                if accepted: text=u"OK, now just pay us!"
                else: text=u"We dont like you"
                form=''
                return render(request, 'polls/name.html',
                              {'form': form,'text':text,'step':0,'button_text':'Voltar'})
        
        else:
            form = ContactForm()

        return render(request, 'polls/name.html',
                  {'form': form,'text':"",'step':2,'button_text':'Manda'})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

        return render(request, 'polls/name.html',
                  {'form': form,'text':"",'step':2,'button_text':'Manda'})