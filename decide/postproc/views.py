from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def participation(self, census, voters):
        out = 0

        if census != 0:
            out = (voters/census)*100
            out = round(out,2)

        return out

    def identity(self, options, census):
        results = []
        voters = 0

        for opt in options:
            voters = voters + opt['votes']
            results.append({
                **opt,
                'postproc': opt['votes'],
            });

        results.sort(key=lambda x: -x['postproc'])

        part = self.participation(census, voters)
        out = {'results': results, 'participation': part}

        return Response(out)

    def saintlague(self,options,seats,census):
        results = []
        voters = sum(opt['votes'] for opt in options)

        for seat in range(seats):
            opt = max(options, key=lambda opt: opt['votes'])

            if not any(d.get('option', None) == opt['option'] for d in results):
                results.append({
                    **opt,
                    'postproc' :1,
                });
            else:
                aux = next((o for o in results if o['option'] == opt['option']), None)
                aux['postproc'] = aux['postproc'] + 1

            aux = next((o for o in results if o['option'] == opt['option']), None)
            opt['votes'] = aux['votes']//(2*aux['postproc'] +1)

        part = self.participation(census, voters)
        out = {'results': results, 'participation': part}

        return Response(out)

    def dhondt(self, options, seats, census):
        results = []
        voters = sum(opt['votes'] for opt in options)

        for seat in range(seats):
            opt = max(options, key=lambda opt: opt['votes'])

            if not any(d.get('option', None) == opt['option'] for d in results):
                results.append({
                    **opt,
                    'postproc': 1,
                });
            else:
                aux = next((o for o in results if o['option'] == opt['option']), None)
                aux['postproc'] = aux['postproc'] + 1

            aux = next((o for o in results if o['option'] == opt['option']), None)
            opt['votes'] = aux['votes']//(aux['postproc'] + 1)

        part = self.participation(census, voters)
        out = {'results': results, 'participation': part}

        return Response(out)

    def majorrest(self, options, seats, census):
        results = []
        residualvoteslist = []
        voters = sum(opt['votes'] for opt in options)
        q = round(voters/seats)
        seatsleft = seats

        for option in options:
            e = floor(option['votes'] / q)
            seatsleft = seatsleft - e
            results.append({
                **option,
                'postproc': e,
            });
            residualvoteslist.append({
                **option,
                'residualvotes': option['votes'] - (q*e),
            });

        resultscopy = results
        for seat in range(seatsleft):
            opt = max(residualvoteslist, key=lambda opt: opt['residualvotes'])
            aux = next((o for o in results if o['option'] == opt['option']), None)
            aux['postproc'] = aux['postproc'] + 1
            residualvoteslist.remove({**opt});


        part = self.participation(census, voters)
        out = {'results': results, 'participation': part}

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
        elif t == 'SAINTLAGUE':
            return self.saintlague(opts,seats,census)
        elif t == 'MAJORREST':
            return self.majorrest(opts, seats, census)

        return Response({})
