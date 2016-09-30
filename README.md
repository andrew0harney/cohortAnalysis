### Overview
A sample of django code to product an upper triangular heatmap of cohort analysis. Each tab is an analysis for a stage in your funnel.
You will probabably need to modify this quite a bit for you use case, but hopefully it will give you some useful pointers.

### Usage
The main class is funnelAnalsysis. You can simply add stages in your funnel by providing stage functions to this class.
Stage functions should give counts of the metric being measured (see _start_scouting() as an example)

You should provide some representation of the users in each cohort (see models.Cohort)
You should also provide some representation of the analytic you wish to measure for the funnel stage (see models.AnalyticsEvent for example)


### Output

Output is an xlxs heatmap file with tabs according to funnel stage. It looks something like cohortAnalysis.xlsx


![alt text](https://github.com/andrew0harney/cohortAnalysis/master/images/cohortAnalysis.png "Example Cohort Analysis")
