#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy.stats, scipy.linalg, numpy, math

def add_errors(*l): return math.sqrt(sum([x**2 for x in l]))

# theta is the true parameter to be estimated.
# the minimum and maximum values for theta which are physically allowed:
theta_min = 0.0
theta_max = 1.0

# scan range for theta. Set this to a range which you are sure includes the interval(s)
# you want to calculate. The number of scan points for theta controls the accurarcy which is guaranteed
# to be better than delta_theta := (theta_max_scan - theta_min_scan) / theta_scan_n in theta. Runtime and memory consumption is linear
# in theta_scan_n.
theta_min_scan = 0.0
theta_max_scan = 1.0
theta_scan_n = 500

# the resolution of the measurement, which is a Gauss around theta with this standard deviation:
sigma = add_errors(0.08, 0.04)
#sigma = add_errors(3.8/25.8, 1.5/22.2)

# in case "sigma" is relative, the actual Gaussian width is set to   theta * sigma
sigma_is_relative = False
#sigma_is_relative = True

# the confidence level (0.68 = 1sigma, 0.95 = 2sigma, ...)
# alpha = 0.68
# alpha = 0.90
alpha = 0.95

# the values for x for which to evaluate the intervals:
measured_x = [1.08]
#measured_x = [25.8/22.2]

# the value of 0.5 provides a check: this should yield ~ symmetric 2sigma interval;
# x = 1.0 provides some more information how the interval changes in that region

### (end of configuration)


# x_step_min defines the stopping criterion for scans along the x-axis: once the interval in x-direction
# is more accurate that this threshold, the search stops. Here, this is set to 1e-3 times
# the value which corresponds to the same resolution as the limited step size in theta. This
# ensures that the interval accuracy is not limited in the scanning resolution in x (but rather by the scanning resolution in theta).
# Runtime is logarithmic in x_step_min.
# (note: for sigma_is_relative==True, this is the smallest sigma which is > 0, which is also Ok)
x_step_min = 1e-3 * sigma * (theta_max_scan - theta_min_scan) / theta_scan_n


class polygon(object):
    def  __init__(self):
        object.__init__(self)
        self.points = []
        
    def add_point(self, point):
        self.points.append(point)

    def get_intersections(self, s1, s2, extend_to_infinity = False):
        result = []
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            try:
                (t, u) = scipy.linalg.solve([[p2[0] - p1[0], s1[0] - s2[0]], [p2[1] - p1[1], s1[1] - s2[1]]], [s1[0] - p1[0], s1[1] - p1[1]])
                if t > 1 or t < 0: continue
                if not extend_to_infinity and (s > 1 or s < 0): continue
                result.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
            except scipy.linalg.LinAlgError: pass
        return result


def r(x, theta):
    log_p_x_thetabest = 0.0
    if x < theta_min: log_p_x_thetabest = -(x - theta_min)**2 / (2 * sigma**2)
    if x > theta_max: log_p_x_thetabest = -(x - theta_max)**2 / (2 * sigma**2)
    log_p_x_theta = -(x - theta)**2 / (2 * sigma**2)
    return log_p_x_theta - log_p_x_thetabest

# find x_high s.t. integral over Gauss from x_low to x_high is alpha.
# returns +infinity if this is not possible.
def find_x_high(mu, sigma, x_low, alpha):
    s_low = (x_low - mu) / sigma
    c = scipy.stats.norm.cdf(s_low)
    rest = 1 - alpha - c
    if rest < 0: return float("inf")
    s_high = -scipy.stats.norm.ppf(rest)
    return s_high * sigma + mu
    

def grid(n_theta):
    x_intervals = {}
    for theta in numpy.linspace(theta_min_scan, theta_max_scan, n_theta):
        sigma_local = sigma
        if sigma_is_relative:
            sigma_local *= theta
            if sigma_local == 0.0: continue
        x_min = theta - 5*sigma_local
        x_max = theta + 5*sigma_local
        x_low = theta - sigma_local
        x_high = find_x_high(theta, sigma_local, x_low, alpha)
        x_step = sigma_local
        while x_step > x_step_min:
            x_step /= 2
            while x_high == float("inf"):
                x_low -= x_step
                x_high = find_x_high(theta, sigma_local, x_low, alpha)
            while r(x_low, theta) < r(x_high, theta) and x_low < x_max:
                x_low += x_step
                x_high = find_x_high(theta, sigma_local, x_low, alpha)
                if x_high == float("inf"):
                    x_low -= x_step
                    x_high = find_x_high(theta, sigma_local, x_low, alpha)
                    break
            if x_high == float("inf"): continue
            while r(x_low, theta) > r(x_high, theta) and x_low > x_min:
                x_low -= x_step
                x_high = find_x_high(theta, sigma_local, x_low, alpha)
        x_intervals[theta] = (x_low, x_high)
        #print "for theta=%g:  %g--%g" % (theta, x_low, x_high)
    p = polygon()
    for theta in sorted(x_intervals.keys()):
        p.add_point((theta, x_intervals[theta][0]))
    for theta in reversed(sorted(x_intervals.keys())):
        p.add_point((theta, x_intervals[theta][1]))
    return p
        
print "note: scanning resolution in theta is %f; the interval ends are guaranteed to be more accurate than that." % ((theta_max_scan - theta_min_scan) / theta_scan_n)
p = grid(theta_scan_n)
interval = lambda x: sorted([i[0] for i in p.get_intersections((0.0, x), (1.0, x), True)])
print "measured value: interval"
for x in measured_x:
    i = interval(x)
    print "%.2f: %.4f--%.4f" % (x, i[0], i[1])
