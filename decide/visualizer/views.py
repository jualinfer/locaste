from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        custom_url = ''
        if 'custom_url' in kwargs:
            custom_url = kwargs.get('custom_url', 1)

        try:
            r = mods.get('voting', params={'id': vid})
            if r[0]['custom_url'] != '' and custom_url != '':
                r = mods.get('voting', params={'id': vid, 'custom_url': custom_url})
                if r[0]['custom_url'] != custom_url:
                    raise Http404
            elif (r[0]['custom_url'] == '' and custom_url != '') or (r[0]['custom_url'] != '' and custom_url == ''):
                raise Http404
            context['voting'] = r[0]
        except:
            raise Http404

        return context
