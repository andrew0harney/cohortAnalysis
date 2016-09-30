class Cohort(models.Model):
    number = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=datetime.now, null=True)
    def __str__(self):
        return '%d'%(self.number)


class AnalyticsEvent(models.Model):

    user = models.ForeignKey(User, db_index=True, null=True)
    type = models.CharField(max_length=100, db_index=True)
    value = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=200, null=True)
    related_event = models.ForeignKey('self', null=True, blank=True)
    datetime = models.DateTimeField(default=tz_datetime.now, db_index=True)
