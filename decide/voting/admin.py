from django.contrib import admin
from django.utils import timezone
import zipfile
from .models import QuestionOption
from .models import Question
from .models import Voting
from django.http import HttpResponse
from .filters import StartedFilter
import os
import requests


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):

    directory = "voting/tallies/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    zipf = zipfile.ZipFile('voting/tallies/tallies.zip', 'w', zipfile.ZIP_DEFLATED)
    token = request.COOKIES.get("decide")
    for v in queryset.filter(end_date__lt=timezone.now()):
        file_name = v.tally_votes(token)
        zipf.write(file_name)
        os.remove(file_name)
    zipf.close()
    with open('voting/tallies/tallies.zip', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=%s' % 'tallies.zip'
        response['X-Sendfile'] = 'tallies.zip'
    fh.close()
    os.remove('voting/tallies/tallies.zip')

    return response


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('pub_key','start_date', 'end_date','tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
