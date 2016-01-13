''' Tony Rice
    created as an exercise for the WRAL.com article on the science of "The Martian"
    http://www.wral.com/-the-martian-gets-the-science-right/15228560/

    relies heavily on the excellent astronomical calculation package PyEphem by Craig Rhodes
    http://rhodesmill.org/pyephem/
'''

import holidays
import ephem
from datetime import timedelta

sol_in_days = 1.027491251
c = 299792458  # speed of light in meters per sec
au_in_meters = 149597870700
transit_in_days = 124
thanksgiving_sol = 15  # Weir calls arrival sol 1


class TheMartian(object):

    def __init__(self, year):
        self.year = year
        self.thanksgiving = self.thanksgiving_date(year)
        self.arrival = self.thanksgiving - timedelta(days=thanksgiving_sol * sol_in_days)
        self.launch = self.arrival - timedelta(days=transit_in_days)

    def thanksgiving_date(self, year):
        d = holidays.US(years=year)
        return d.keys()[d.values().index('Thanksgiving')]

    def mars_earth_dist(self, sol=0):
        earth_date = self.sol_to_earth_date(sol)
        au = ephem.Mars(earth_date).earth_distance
        return au*(au_in_meters/c)/60

    def sol_to_earth_date(self, sol):
        return self.arrival + timedelta(days=(sol*sol_in_days))


if __name__ == "__main__":
    stringfmt = "%4s %8s %8s %8s %8s"
    print stringfmt % ('year', 'launch', 'sol1', 'tgiving', 'sol96')
    for year in range(2014, 2050):
        launch_opportunity = TheMartian(year)
        comms_delay_minutes = launch_opportunity.mars_earth_dist(sol=96)
        if comms_delay_minutes >= 11 and comms_delay_minutes < 12:
            print stringfmt % (year, launch_opportunity.launch.strftime('%b-%d'),
                               launch_opportunity.arrival.strftime('%b-%d'),
                               launch_opportunity.thanksgiving.strftime('%b-%d'),
                               launch_opportunity.sol_to_earth_date(96).strftime('%b-%d'))
