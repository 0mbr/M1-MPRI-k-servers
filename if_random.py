# If you opt for a randomized algorithm, you need to compute its performance on average:
# the mean results and its confidence interval.
# below, you will find all the elements required for this purpose.

import numpy
import scipy.stats

# To have a sample (gather the results of your random algorithm in sample)
# In this example, the sample is filled with values from the normal distribution N(0,1) 
sample = numpy.random.normal(size=100)
average_solution = numpy.mean(sample)

# A typical confidence level is 95%
confidence = 0.95

# Computation of the confidence interval: bounds returned in a tuple.
(lower_bound, upper_bound) = scipy.stats.norm.interval(confidence, loc=average_solution, scale=scipy.stats.sem(sample))

# Finally, the outcome:
print("Mean "+str(average_solution)+" inside of "+str((lower_bound, upper_bound)))

 