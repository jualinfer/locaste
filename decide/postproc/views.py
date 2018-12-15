from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def participation(self, census, voters):
        out = (voters/census)*100
        out = round(out,2)

        return out

    def identity(self, options, census):
        out = []
        voters = 0

        for opt in options:
            voters = voters + opt['votes']
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        out.append({
            'participation': self.participation(census, voters)
        })

        return Response(out)

    def dhondt(self, options, seats, census):
        out = []
        voters = sum(opt['votes'] for opt in options)

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

        out.append({
            'participation': self.participation(census, voters)
        })

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
        census = request.data.get('census')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts, census)
        elif t == 'DHONDT':
            return self.dhondt(opts, seats, census)

        return Response({})
