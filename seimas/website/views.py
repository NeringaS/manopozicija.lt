import requests

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.contrib import messages

from seimas.website.helpers import formrenderer
from seimas.website.forms import NewVotingForm
from seimas.website.models import Topic
from seimas.website.models import Position
from seimas.website.models import Voting
from seimas.website.parsers import parse_votes
from seimas.website.services.voting import update_voting
from seimas.website.services.voting import import_votes
from seimas.website.helpers.decorators import superuser_required


def topic_list(request):
    return render(request, 'website/topic_list.html', {
        'topics': Topic.objects.all(),
    })


def topic_details(request, slug):
    topic = get_object_or_404(Topic, slug=slug)

    return render(request, 'website/topic_details.html', {
        'topic': topic,
        'votings': Voting.objects.filter(position__topic=topic).order_by('datetime'),
    })


@superuser_required
def voting_form(request, slug):
    topic = get_object_or_404(Topic, slug=slug)

    if request.method == 'POST':
        form = NewVotingForm(topic, request.POST)
        if form.is_valid():
            voting = form.save(commit=False)
            voting.author = request.user

            resp = requests.get(voting.link)
            data = parse_votes(voting.link, resp.content)
            update_voting(voting, data)

            voting.save()

            Position.objects.create(topic=topic, content_object=voting, weight=form.cleaned_data['weight'])

            import_votes(voting, data['table'])

            messages.success(request, ugettext("Voting „%s“ created." % voting))
            return redirect(topic)
    else:
        form = NewVotingForm(topic)

    return render(request, 'website/voting_form.html', {
        'topic': topic,
        'form': formrenderer.render(request, form, title=ugettext('Naujas balsavimas'), submit=ugettext('Pridėti')),
    })
