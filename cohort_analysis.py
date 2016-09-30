import logging
from django.db.models import Q
import collections
import datetime as dt
import numpy as np
import time
from django.utils import timezone
import pytz
import pandas as pd
from collections import Counter

class FunnelAnalysis:

    def __init__(self):
        self._stages = []
        self.columns = None

    def add_stage(self, stageFunction, name):
        self._stages.append((stageFunction, name))

    def get_labels(self):
        return [stage[1] for stage in self._stages]

    def get_analysis(self, cohorts):
        from analytics.models import AnalyticsEvent

        result = np.zeros([len(cohorts), len(self._stages)])
        for i, cohort in enumerate(cohorts):
            for j, func in enumerate(self._stages):
                events = AnalyticsEvent.objects.filter(user__userprofile__cohort=cohort)
                result[i, j] = func[0](cohort, events)

        return result

    def get_cohort_analysis(self, cohorts, interval_days=14):
        from analytics.models import AnalyticsEvent

        start_date = cohorts.order_by('number').first().start_date
        now = pytz.timezone("UTC").localize(timezone.datetime.now())
        index = pd.date_range(start=start_date, end=now, freq='2W')
        result = np.zeros([len(self._stages), len(cohorts), len(index)+1])

        for j, cohort in enumerate(cohorts):
            events = AnalyticsEvent.objects.filter(user__userprofile__cohort=cohort)
            n_cohort_users = cohort.userprofile_set.count()
            start_date = cohort.start_date
            for i, stage_func in enumerate(self._stages):
                end_date = start_date
                k = 0
                while end_date <= now:
                    print('Cohort %d, Stage %s, Week %d'%(cohort.number, stage_func[1], k+1))
                    end_date = end_date+timezone.timedelta(days=interval_days)
                    result[i, j, k ] = stage_func[0](cohort, events, start_date, end_date)*100/n_cohort_users
                    k += 1

        return result

def _register(cohort, events):
    return cohort.userprofile_set.all().count()

def _start_tutorial(cohort, events):
    return events.filter(type='tutorial', value='start').distinct('user').count()

def _extension_auth(cohort, events):
    return events.filter(type='extension_authorisation_granted').distinct('user').count()

def _complete_tutorial(cohort,events):
    return events.filter(type='tutorial', value='finish').distinct('user').count()


def _construct_filter(conditions):
    queries = [Q(**terms) for terms in conditions]
    query = queries.pop()
    for q in queries:
        query &= q
    f = query

    return f

def _start_scouting(cohort, events, min_date=None, max_date=None):

    conditions = [{'category' : 'cs_interaction_active'}]
    if min_date is not None:
        conditions.append({'datetime__gte': min_date})
    if max_date is not None:
        conditions.append({'datetime__lte': max_date})

    query_filter = _construct_filter(conditions)
    return events.filter(query_filter).distinct('user').count()

def add_headmap(workbook, name, data, headings, row_names):
        import xlsxwriter
        worksheet = workbook.add_worksheet(name)
        bold = workbook.add_format({'bold': 1})

        n_cohorts, n_weeks = data.shape

        worksheet.write_row('B1', headings, bold)
        worksheet.write_column('A2', row_names, bold)

        for ix in range(2, n_cohorts+2):
            worksheet.write_row('B%d'%(ix), data[ix-2,:].tolist())

        for w in range(n_weeks):
            col = xlsxwriter.utility.xl_col_to_name(w+1)
            worksheet.conditional_format('%s2:%s%d'%(col, col, n_cohorts+1), {'type': '3_color_scale'})


def cohort_analysis(cohorts=None, output=None):

    fa = FunnelAnalysis()
    fa.add_stage(_start, 'Start Start')


    from analytics.models import Cohort

    if cohorts is None:
        cohorts = Cohort.objects.filter(number__in=['%s'%(str(n.number)) for n in Cohort.objects.all()]).all().order_by('number')
    if output is None:
        output = 'cohortAnalysis.xlsx'

    result = fa.get_cohort_analysis(cohorts)

    workbook = xlsxwriter.Workbook(output)
    n_stages, n_cohorts, n_weeks = result.shape

    for s in range(n_stages):
        add_headmap(workbook, fa.get_labels()[s], result[s,:,:], range(n_weeks), ['Cohort %s'%(cohort.number) for cohort in cohorts])
    workbook.close()

if __name__ == '__main__':
    cohort_analysis()