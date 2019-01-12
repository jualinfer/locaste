from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def participation(self, census, voters):
        out = 0

        if census != 0:
            out = (voters/census)*100
            out = round(out,2)

        return out

    def percentage(self,census,options):
        results = []
        voters = sum(opt['votes'] for opt in options)

        for opt in options:
            votersOpt = opt['votes']
            out = (votersOpt/census)*100
            out = round(out,2)
            results.append({
                **opt,
                'percentage':out
            });

        results.sort(key=lambda x: -x['percentage'])

        part = self.participation(census,voters)
        out = {'results':results,'participation':part}

        return Response(out)

    def order(self, results):
        results.sort(key=lambda x: -x['postproc'])

    def maximum(self, options):
        return max(options, key=lambda opt: opt['votes'])

    def update_results(self, opt, results, arg):
        if not any(d.get('option', None) == opt['option'] for d in results):
            results.append({
                **opt,
                'postproc': arg,
            })
        else:
            aux = next((o for o in results if o['option'] == opt['option']), None)
            aux['postproc'] = aux['postproc'] + arg

    def borda(self, options):
        results = []
        max_points = len(options)

        for opt in options:
            for i in range(max_points):
                points = opt['votes'][i]*(max_points-i)
                self.update_results(opt, results, points)

        self.order(results)
        out = {'results': results}

        return Response(out)

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

    def saintelague(self,options,seats,census,version):
        results = []
        voters = sum(opt['votes'] for opt in options)

        for seat in range(seats):
            opt = self.maximum(options)
            self.update_results(opt, results, 1)

            if version=='modified':
                aux = next((o for o in results if o['option'] == opt['option']), None)
                if aux['postproc']==1:
                    opt['votes'] =(aux['votes']//(2*aux['postproc'] +1))
                else:
                    opt['votes'] =(aux['votes']//(2*aux['postproc'] +1))*1.4
            elif version=='classic':
                aux = next((o for o in results if o['option'] == opt['option']), None)
                opt['votes'] = aux['votes']//(2*aux['postproc'] +1)

        part = self.participation(census, voters)
        out = {'results': results, 'participation': part}

        return Response(out)


    def dhondt(self, options, seats, census):
        results = []
        voters = sum(opt['votes'] for opt in options)

        for seat in range(seats):
            opt = self.maximum(options)
            self.update_results(opt, results, 1)

            aux = next((o for o in results if o['option'] == opt['option']), None)
            opt['votes'] = aux['votes']//(aux['postproc'] + 1)

        part = self.participation(census, voters)
        out = {'results': results, 'participation': part}

        return Response(out)

    def majorrest(self, options, seats, census, quotient):
        results = []
        residualvoteslist = []
        voters = sum(opt['votes'] for opt in options)
        if quotient == 'hare':
            q = round(voters/seats)
        elif quotient == 'droop':
            q = 1 + round(voters/(seats + 1))
        elif quotient == 'imperiali':
            q = round(voters/(seats + 2))

        seatsleft = seats

        for option in options:
            e = option['votes'] // q
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
        t = request.data.get('type', 'IDENTITY')
        seats = request.data.get('seats')
        census = request.data.get('census')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts, census)
        elif t == 'DHONDT':
            return self.dhondt(opts, seats, census)
        elif t == 'SAINTELAGUE':
            return self.saintelague(opts,seats,census,'classic')
        elif t == 'BORDA':
            return self.borda(opts)
        elif t == 'MAJORRESTHARE':
            return self.majorrest(opts, seats, census, 'hare')
        elif t == 'MAJORRESTDROOP':
            return self.majorrest(opts, seats, census, 'droop')
        elif t == 'MAJORRESTIMPERIALI':
            return self.majorrest(opts, seats, census, 'imperiali')
        elif t=='SAINTELAGUEMOD':
            return self.saintelague(opts,seats,census,'modified')
        elif t == 'PERCENTAGE':
            return self.percentage(census,opts)

        return Response({})
