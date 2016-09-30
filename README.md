### Overview
A sample of Django code to produce an upper triangular heatmap of cohort analysis. Each tab is an analysis for a stage in your funnel.
You will probably need to modify this quite a bit for your use case, but hopefully it will give you some useful pointers.

### Usage
The main class is funnelAnalsysis. You can simply add stages in your funnel by providing stage functions to this class.
Stage functions should return counts of the metric being measured given the paramters cohort/user group and events (see _start_scouting() as an example).

You should provide some representation of the users in each cohort (see models.Cohort)
You should also provide some representation of the analytic you wish to measure for the funnel stage (see models.AnalyticsEvent for example)


### Output

Output is an xlxs heatmap file with tabs according to funnel stage. The output looks as below. Week/period on the x and cohort on the y.


![alt text](https://github.com/andrew0harney/cohortAnalysis/raw/master/images/cohortAnalysis.png "Example Cohort Analysis")

For any EF companies who take a look - Enjoy responsibly :)
