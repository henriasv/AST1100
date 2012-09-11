# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from scitools.easyviz.matplotlib_ import plot, figure, hold, closefigs, title, legend, xlabel, ylabel, hardcopy
from Scientific.Functions.LeastSquares import leastSquaresFit

class Star:
    """
    Holds information about star observations:
        time
        frequency
        intensity
    """
    def __init__(self, filename, path):

        self.path = os.path.expanduser(path+filename);
        self.filename = filename;
        self.mass = 0;
        self.file = open(self.path);
        self.t = [];
        self.frequencies = [];
        self.intensities = [];
        self.velocities = [];
        self.v_r = 0;
        self.v_mean = 0;
        self.P = 0;
        self.t_0 = 0;
        self.model = ModelFitStar();
        self.guessedParameters  = []; # When initialized: [v_mean, v_r, P, t_0]
        
        for line in self.file:
            data = line.split();
            self.t.append(float(data[0]));
            self.frequencies.append(float(data[1]));
            self.intensities.append(float(data[2]));
        self.t = np.asarray(self.t);
        self.frequencies = np.asarray(self.frequencies);
        self.intensities = np.asarray(self.intensities);
            
    def calculate_velocities(self, lambda_0=656.3, c = 299792458.0):
        """
        Using the doppler effect to calculate the radial velocity of the star
        requires that some 
        """

        self.velocities = np.asarray((self.frequencies-lambda_0)/(lambda_0)*c);
            
    def set_mass(self, mass):
        self.mass = mass;
        
    def plot_intensities(self):
        figure();
        plot(self.t, self.intensities);
        xlabel('t[s]');
        ylabel('Relative intensity')
        title(self.filename + ' intensity');
        
    def plot_frequencies(self):
        figure();
        plot(self.t, self.frequencies);
        xlabel('t[s]');
        ylabel('Wavelength [nm]');
        title(self.filename + ' Wavelength');
        
    def plot_velocities(self):
        figure();
        if not self.velocities:
            self.calculate_velocities();
        plot(self.t, self.velocities);
        title(self.filename + ' Velocities');
        xlabel('t[s]');
        ylabel('radial velocity [m/s]');
        
    def fit_velocities(self):
        """
        Calculates the best parameter values to fit the imported data.
        Saves them as object attributes.
        """
        if len(self.velocities) == 0:
            self.calculate_velocities();
        
        if not self.guessedParameters:
            param, fit_value = self.model(self.t, self.velocities);
        else:
            param, fit_value = self.model(self.t, self.velocities, param = self.guessedParameters);
        self.v_mean = param[0];
        self.v_r = param[1];
        self.P = param[2];
        self.t_0 = param[3];
        print param;
        
    def plot_fitted_velocities(self, destination = False):
        if self.P == 0:
            self.fit_velocities();
        data = self.model.modelFunction([self.v_mean, self.v_r, self.P, self.t_0], self.t);
        figure();
        plot(self.t, self.velocities, '--r');
        hold('on');
        plot(self.t, data, '-b')
        title("Least square modeled velocities");
        xlabel('t [s]');
        ylabel('v [m/s]');
        legend('v_mean=%g \n v_r=%g \n P=%g \n t_0=%g' % (self.v_mean, self.v_r, self.P, self.t_0));
        if destination:
            hardcopy(destination);
            
    def output_data(self, destination):
        outfile = open(destination, 'w');
        outfile.write(self.filename + '\n');
        outfile.write('Guessed parameters: \n');
        if not self.guessedParameters:
            outfile.write('Parameters were not guessed');
        else:
            outfile.write('v_mean: %g \n' % self.guessedParameters[0]);
            outfile.write('v_r: %g \n' % self.guessedParameters[1]);
            outfile.write('P: %g \n' % self.guessedParameters[2]);
            outfile.write('t_0: %g \n' % self.guessedParameters[3]);
            
        outfile.write('Fitted parameters: \n')
        outfile.write('v_mean: %g \n' % self.v_mean);
        outfile.write('v_r: %g \n' % self.v_r);
        outfile.write('P: %g \n' % self.P);
        outfile.write('t_0: %g \n' % self.t_0);
        
        
        
class ModelFitStar:
    
    def __call__(self, t, data, param = [10000, 200, 300000, 2000]):
        """
        Sets the Star object parameters to the best fit. param can be changed
        for better performance. Be aware that there might be more than one fix
        point for each data-set, so inspect the result to see wheter it is a 
        realistic fit. Usually this is no problem if the initializing parameters 
        are sensible.
        """
        # create list of tuples
        values = [];
        print len(data);
        print len(t);
        for i in range(len(t)):
            values.append([t[i], data[i]]);
        values = np.asarray(values);
        return leastSquaresFit(self.modelFunction, param, values)
    
    def modelFunction(self, param, t):
        """
        Arguments:
            param - parameters to be fitted:
                param[0] = v_mean
                param[1] = v_r
                param[2] = P (period of star orbit)
                param[3] = t_0
        """
        return param[0]+param[1]*np.cos(2*np.pi/param[2]*(t-param[3]));
    
class StarAnalysis:
    def __init__(self, path):
        star_list = os.listdir(path);
        star_list.sort();
        self.chosen_stars = [];
        self.stars = [];
        for name in star_list:
            self.stars.append(Star(name, path));
        
    def choose_stars(self):
        for star in self.stars:
            star.plot_velocities();
            star.plot_intensities();
            isContinue = raw_input('Choose this star? (y/n/b/q)');
            if isContinue == 'q':
                closefigs();
                sys.exit(0);
            elif isContinue == 'b':
                break;
            elif isContinue == "y":
                isTryInputParameters = True;
                while (isTryInputParameters):
                    param = raw_input("input your best guess for \
                        velocity model parameters as a list \
                        \"v_mean v_r P t_0\" s");
                    if param == "q":
                        sys.exit(1);
                    param = param.split();
                    for i in range(len(param)):
                        param[i] = float(param[i]);
                    print "Your input:";
                    print param;
                    if isinstance(param, (list, tuple)) and len(param) == 4:
                        star.guessedParameters = list(param);
                        isTryInputParameters = False;
                    else:
                        print "Invalid parameters, try again"     
                self.chosen_stars.append(star);
            elif isContinue == "n":
                print "Ok. Presenting next star";
            closefigs();
        print "No more stars";
        
    def analyze_stars(self, destination):
        for star in self.chosen_stars:
            star.plot_fitted_velocities(destination+star.filename+".png");
            star.output_data(destination+star.filename+".txt");
            closefigs();
        
        
        
star_path = '/home/henrik/Dropbox/Henrik/Emner/AST1100/Obliger/oblig2/star_data/';
destination_path = '/home/henrik/Dropbox/Henrik/Emner/AST1100/Obliger/oblig2/output/';
sa = StarAnalysis(star_path);
sa.choose_stars();
sa.analyze_stars(destination_path);
raw_input('press enter');
"""
star_path = '/home/henrik/Dropbox/Henrik/Emner/AST1100/Obliger/oblig2/star_data/';
star1 = Star('star0.txt', star_path);
#star1.plot_intensities();
star1.plot_frequencies();
star1.plot_fitted_velocities();

raw_input('press enter');
closefigs();
"""
        
        