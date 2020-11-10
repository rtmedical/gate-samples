#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib import collections as mc
import scipy.stats as ss
import scipy
import numpy as np
import os
from pathlib import Path
import uproot
import re
import click

def hello():
    print('Hello World')

def get_stat_value(s, v):
    """
    This function retrive a value from a stat file
    """
    g = r''+v+'\w+'
    a = re.search(g, s)
    if a == None:
        return -1
    a = a.group(0)[len(v):]
    return float(a)  
    
def tget(t, array_name):
    """ 
    it is faster to access to root array like this dont know exactly why
    """
    return t.arrays([array_name])[array_name]


def plot_transaxial_position(ax, coinc, slice_time):
    times = tget(coinc, b'time1')
    runID = tget(coinc, b'runID')
    gpx1 = tget(coinc, b'globalPosX1')
    gpx2 = tget(coinc, b'globalPosX2')
    gpy1 = tget(coinc, b'globalPosY1')
    gpy2 = tget(coinc, b'globalPosY2')
    # only consider coincidences  with time lower than time_slice
    # (assuming 2 time slices only)
    mask = (times < slice_time)
    n = 1000 # restrict to the n first values
    r0_gpx1 = gpx1[mask][:n]
    r0_gpx2 = gpx2[mask][:n]
    r0_gpy1 = gpy1[mask][:n]
    r0_gpy2 = gpy2[mask][:n]
    r0x = np.concatenate((r0_gpx1,r0_gpx2, r0_gpx1))
    r0y = np.concatenate((r0_gpy1,r0_gpy2, r0_gpy1))
    ax.scatter(r0x, r0y, s=1)
    mask = (times > slice_time)
    r1_gpx1 = gpx1[mask][:n]
    r1_gpx2 = gpx2[mask][:n]
    r1_gpy1 = gpy1[mask][:n]
    r1_gpy2 = gpy2[mask][:n]
    r1x = np.concatenate((r1_gpx1,r1_gpx2, r1_gpx1))
    r1y = np.concatenate((r1_gpy1,r1_gpy2, r1_gpy1))
    ax.scatter(r1x, r1y, s=1)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('mm')
    ax.set_ylabel('mm')
    ax.set_title('Transaxial detection position ({} first events only)'.format(n))


def plot_axial_detection(ax, coinc):
    # Axial Detection
    ad1 = tget(coinc, b'globalPosZ1')
    ad2 = tget(coinc, b'globalPosZ2')
    ad = np.concatenate((ad1, ad2))
    ax.hist(ad, histtype='step', bins=100)
    ax.set_xlabel('mm')
    ax.set_ylabel('counts')
    ax.set_title('Axial coincidences detection position')


def get_counts(coinc):
    # trues, scatters, randoms, Ctot = p.get_counts(coinc)
    # 
    # Cscat : scatter counts is the number of falsely located coincidence events resulting from gamma rays scattering inside the phantom
    # Ctrue : is the number of true coincidences
    # Crnd  : the number of random (accidental) coincidences
    # Ctot  : Ctot = Cscat + Ctrue + Crnd is the total number of detected coincidences, sometimes called 'prompts'
    # 
    ad1 = tget(coinc, b'globalPosZ1')
    ad2 = tget(coinc, b'globalPosZ2')
    z = (ad1+ad2)/2
    compt1 = tget(coinc, b'comptonPhantom1')
    compt2 = tget(coinc, b'comptonPhantom2')
    rayl1 = tget(coinc, b'RayleighPhantom1')
    rayl2 = tget(coinc, b'RayleighPhantom2')
    mask =  ((compt1==0) & (compt2==0) & (rayl1==0) & (rayl2==0))
    trues = z[mask]
    scatters = z[~mask]
    # Randoms
    eventID1 = tget(coinc, b'eventID1')
    eventID2 = tget(coinc, b'eventID2')
    time = tget(coinc, b'time1')
    randoms = time[eventID1 != eventID2]
    Ctot = len(trues) + len(scatters) + len(randoms)
    return trues, scatters, randoms, Ctot
    
def plot_axial_sensitivity_detection(ax, trues):
    ax.hist(trues, bins=100)
    ax.set_xlabel('mm')
    ax.set_ylabel('counts')
    ax.set_title('Axial Sensitivity Detection')

def plot_axial_scatter_fraction(ax, coinc, scatters): 
    ad1 = tget(coinc, b'globalPosZ1')
    ad2 = tget(coinc, b'globalPosZ2')
    z = (ad1+ad2)/2
    countsa, binsa = np.histogram(scatters, bins=100)
    countsr, binsr = np.histogram(z, bins=100)
    ax.hist(binsa[:-1], bins=100, weights=countsa/countsr)
    ax.set_xlabel('mm')
    ax.set_ylabel('%')
    ax.set_title('Axial Scatter fraction')
    
def get_decays(coinc):
    time = tget(coinc, b'time1')
    sourceID1 = tget(coinc, b'sourceID1')
    sourceID2 = tget(coinc, b'sourceID2')
    mask = (sourceID1==0) & (sourceID2==0)
    decayF18 = time[mask]
    mask = (sourceID1==1) & (sourceID2==1)
    decayO15 = time[mask]
    return decayF18, decayO15

def plot_rad_decay(ax, end_time, decayO15, decayF18):
    # histogram of decayO15
    bin_heights, bin_borders = np.histogram(np.array(decayO15), bins='auto', density=True)
    bin_widths = np.diff(bin_borders)
    bin_centers = bin_borders[:-1] + bin_widths / 2
    # exponential fit
    # (ignore the warning for overflow error)
    np.seterr(all='warn', over='ignore')
    def exponenial_func(x, a, b):
        return a*np.exp(-b*x)
    popt, pcov = scipy.optimize.curve_fit(exponenial_func, bin_centers, bin_heights)
    xx = np.linspace(0, int(end_time), int(end_time))
    yy = exponenial_func(xx, *popt)
    hl = np.log(2)/popt[1]
    # plot
    ax.hist(decayO15, bins=100, label='O15 HL = 122.24 sec', histtype='stepfilled', alpha=0.5, density=True)
    ax.hist(decayF18, bins=100, label='F18 HL = 6586.2 sec', histtype='stepfilled', alpha=0.5, density=True)
    ax.plot(xx, yy, label=f'O15 fit HL = {hl:.2f} sec')
    ax.legend()
    ax.set_xlabel('time (s)')
    ax.set_ylabel('decay')
    ax.set_title('Rad decays')

def plot_randoms_delays(ax, randoms, delays):
    t1 = tget(delays, b'time1')
    ax.hist(randoms, bins=100, histtype='stepfilled', alpha=0.6, label=f'Real randoms = {len(randoms)}')
    ax.hist(t1, bins=100, histtype='step', label=f'Delays (estimated randoms) = {len(delays)}')
    ax.legend()
    ax.set_xlabel('time (s)')
    ax.set_ylabel('events')
    ax.set_title('Randoms')
    
def plot_LOR(ax, coinc, nb):    
    x1 = coinc.arrays()[b'globalPosX1']
    y1 = coinc.arrays()[b'globalPosY1']
    x2 = coinc.arrays()[b'globalPosX2']
    y2 = coinc.arrays()[b'globalPosY2']
    x1 = x1[0:nb]
    y1 = y1[0:nb]
    x2 = x2[0:nb]
    y2 = y2[0:nb]
    ax.plot([x1,x2],[y1,y2])    
    ax.autoscale()
    ax.set_xlabel('Position in mm')
    ax.set_ylabel('Poisition in mm')
    ax.set_title('Lines of response (LOR)')