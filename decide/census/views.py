from django.views.generic import TemplateView
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist, PermissionDenied
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CensusSerializer
from rest_framework.status import (
    HTTP_201_CREATED as ST_201,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_401_UNAUTHORIZED as ST_401,
    HTTP_403_FORBIDDEN as ST_403,
    HTTP_409_CONFLICT as ST_409
)

from .models import Census
from django.http import Http404

from base import mods

from rest_framework.permissions import IsAuthenticated


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Census.objects.all()
    serializer_class = CensusSerializer

    def create(self, request, *args, **kwargs):

        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters') or []
        voter_id = request.data.get('voter_id')
        if voter_id:
            voters.append(voter_id)

        try:
            voters = Census.public_or_private(voting_id, voters, request.user)
            if not voters:
                return Response('No voter ids where provided', status=ST_400)
            Census.check_restrictions_multiple_voters(voting_id, voters)

            for voter in voters:
                census = Census.create(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error trying to create census', status=ST_409)
        except ValidationError as e:
            return Response(str(e), status=ST_400)
        except PermissionDenied as p:
            return Response(str(p), status=ST_403)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        if voting_id is None:
            voter_id = request.GET.get('voter_id')
            if voter_id is None:
                return Response('', status=ST_400)
            else:
                voting = Census.objects.filter(voter_id=voter_id).values_list('voting_id', flat=True)
                return Response({'voting': voting})
        else:
            voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
            return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters') or []
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')


class CensusView(TemplateView):
    template_name = 'census/census.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = r[0]
        except:
            raise Http404

        return context
