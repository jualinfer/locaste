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

    def majorrest(self, options, seats, census):
        voters = sum(opt['votes'] for opt in options)

        qh = round(voters/seats)
        results_hare = []
        residualvoteslisth = []
        seatslefth = seats

        qd = 1 + round(voters/(seats + 1))
        results_droop = []
        residualvoteslistd = []
        seatsleftd = seats

        qi = round(voters/(seats + 2))
        results_imperiali = []
        residualvoteslisti = []
        seatslefti = seats

        for option in options:
            eh = option['votes'] // qh
            seatslefth = seatslefth - eh
            results_hare.append({
                **option,
                'postproc': eh,
            });
            residualvoteslisth.append({
                **option,
                'residualvotes': option['votes'] - (qh*eh),
            });

            ed = option['votes'] // qd
            seatsleftd = seatsleftd - ed
            results_droop.append({
                **option,
                'postproc': ed,
            });
            residualvoteslistd.append({
                **option,
                'residualvotes': option['votes'] - (qd*ed),
            });

            ei = option['votes'] // qi
            seatslefti = seatslefti - ei
            results_imperiali.append({
                **option,
                'postproc': ei,
            });
            residualvoteslisti.append({
                **option,
                'residualvotes': option['votes'] - (qi*ei),
            });

        resultscopyh = results_hare
        resultscopyd = results_droop
        resultscopyi = results_imperiali

        for seat in range(seatslefth):
            opt = max(residualvoteslisth, key=lambda opt: opt['residualvotes'])
            aux = next((o for o in results_hare if o['option'] == opt['option']), None)
            aux['postproc'] = aux['postproc'] + 1
            residualvoteslisth.remove({**opt});

        for seat in range(seatsleftd):
            opt = max(residualvoteslistd, key=lambda opt: opt['residualvotes'])
            aux = next((o for o in results_droop if o['option'] == opt['option']), None)
            aux['postproc'] = aux['postproc'] + 1
            residualvoteslistd.remove({**opt});

        for seat in range(seatslefti):
            opt = max(residualvoteslisti, key=lambda opt: opt['residualvotes'])
            aux = next((o for o in results_imperiali if o['option'] == opt['option']), None)
            aux['postproc'] = aux['postproc'] + 1
            residualvoteslisti.remove({**opt});


        part = self.participation(census, voters)
        out = {'results_hare': results_hare, 'results_droop': results_droop, 'results_imperiali': results_imperiali, 'participation': part}

        return Response(out)

    def post(self, request):
        t = request.data.get('type', 'IDENTITY')
        seats = request.data.get('seats')
        census = request.data.get('census')
        opts = request.data.get('options', [])

        if t == None:
            return self.identity(opts, census)
        elif t == 'DHONDT':
            return self.dhondt(opts, seats, census)
        elif t == 'SAINTELAGUE':
            return self.saintelague(opts,seats,census,'classic')
        elif t == 'BORDA':
            return self.borda(opts)
        elif t == 'MAJORREST':
            return self.majorrest(opts, seats, census)
        elif t=='SAINTELAGUEMOD':
            return self.saintelague(opts,seats,census,'modified')
        elif t == 'PERCENTAGE':
            return self.percentage(census,opts)

        return Response({})
