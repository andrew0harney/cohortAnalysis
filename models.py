class Cohort(models.Model):
    number = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=datetime.now, null=True)
    def __str__(self):
        return '%d'%(self.number)