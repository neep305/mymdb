from django.contrib.auth.mixins import (
    LoginRequiredMixin)
from django.core.exceptions import (
    PermissionDenied)
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, UpdateView,
    CreateView
)

from core.forms import VoteForm
from core.models import Movie, Person, Vote


# Create your views here.
class MovieDetail(DetailView):
    # model = Movie
    queryset = (
        Movie.objects.all_with_related_persons()
    )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user
            )

            if vote.id:
                vote_form_url = reverse(
                    'core:UpdateVote',
                    kwargs={
                        'movie_id': vote.movie.id,
                        'pk': vote.id
                    }
                )
            else:
                vote_form_url = (
                    reverse(
                        'core:CreateVote',
                        kwargs={
                            'movie_id': self.object.id
                        }
                    )
                )
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        return ctx


class MovieList(ListView):
    model = Movie


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movie()
