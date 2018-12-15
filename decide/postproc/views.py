from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def dhondt(self, options, seats):
        out = []

        for seat in range(seats):
            opt = max(options, key=lambda opt: opt['votes'])

            if not any(d.get('option', None) == opt['option'] for d in out):
                out.append({
                    **opt,
                    'postproc': 1,
                });
            else:
                aux = next((o for o in out if o['option'] == opt['option']), None)
                aux['postproc'] = aux['postproc'] + 1

            aux = next((o for o in out if o['option'] == opt['option']), None)
            opt['votes'] = aux['votes']//(aux['postproc'] + 1)

        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        seats = request.data.get('seats')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'DHONDT':
            return self.dhondt(opts, seats)

        return Response({})
