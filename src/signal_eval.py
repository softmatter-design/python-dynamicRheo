#!/usr/bin/env python
# -*- coding: utf-8 -*-
##### Import #####
from scipy.optimize import curve_fit
import subprocess
import numpy as np
import platform
################################################################################
def main():
	#
	omega = 1.
	gamma0 = 1.
	resolution = 10
	period = 50
	cond = [omega, gamma0, resolution, period]
	input = generate_signal(cond)
	#
	sigma0 = 0.1
	delta = 0.7
	nl = 0.2
	omega_t, gamma, sigma, sigma_wn = calc_sigma(input, sigma0, delta, nl)
	#
	g_sigma0 = 1.
	g_delta = 1.
	guess = [g_sigma0, g_delta]
	popt = fit_rheo(omega_t, sigma_wn, guess)
	#
	save_data(omega_t, gamma, sigma, sigma_wn, popt, "output.dat")
	plotlis("output.dat")

################################################################################

############################################################################
##### Main #####
# 
def generate_signal(cond):
	omega, gamma0, resolution, period = cond

	time = 0
	input = []
	for rep in range(period):
		for t in range(resolution):
			time = t/resolution + rep
			gamma = gamma0*np.sin(omega*time)
			input.append([omega*time, gamma])
	return input

def calc_sigma(input, sigma0, delta, nl):
	omega_t = []
	gamma = []
	sigma = []
	sigma_wn = []
	for dat in input:
		omega_t.append(dat[0])
		gamma.append(dat[1])
		sigma.append(func(dat[0], sigma0, delta))
		sigma_wn.append(np.random.normal(loc= 1., scale=nl)*func(dat[0], sigma0, delta))
	return omega_t, gamma, sigma, sigma_wn

def func(omega_t, sigma0, delta):
	sigma = sigma0*np.sin(omega_t + delta)
	return sigma

def fit_rheo(omega_t, sigma_wn, guess):
	popt, pcov = curve_fit(func, np.array(omega_t), np.array(sigma_wn), p0 = guess)
	print(popt, pcov)
	return popt

############################################################################

def save_data(time, gamma, sigma, sigma_wn, popt, f_data):
	with open(f_data,'w') as f:
		for i, t in enumerate(time):
			f.write(str(t) + '\t' + str(gamma[i]) + '\t' + str(sigma[i]) + '\t' + str(sigma_wn[i]) + '\t' + str(func(t, popt[0], popt[1])) + '\n')
	return

#----- 結果をプロット
def plotlis(f_data):
	plt = make_script(f_data)
	#
	if platform.system() == "Windows":
		subprocess.call([plt], shell=True)
	elif platform.system() == "Linux":
		subprocess.call(['gnuplot ' + plt], shell=True)
	return

# 必要なスクリプトを作成
def make_script(f_data):
	script = make_content(f_data)
	plt = f_data.replace('dat', 'plt')
	with open(plt, 'w') as f:
		f.write(script)
	return plt

# スクリプトの中身
def make_content(f_data):
	out_png = f_data.replace('dat', 'png')
	script = 'set term pngcairo font "Arial,14"\n\n'
	script += 'set colorsequence classic\n\n'
	script += 'data = "' + f_data + '"\n\n'
	script += 'set output "' + out_png + '"\n\n'
	script += 'set key left\nset size square\n'
	script += '#set xrange [1:4]\n#set yrange [0:0.2]\n#set xtics 1\n#set ytics 0.1\n'
	script += 'set xlabel "Strain"\nset ylabel "Stress"\n'	
	script += 'plot	data u 2:3 w l lw 2 lt 1 ti "Original" , \\\n'
	script += 'data u 2:4 w l lw 2 lt 2 ti "Modified", \\\n'
	script += 'data u 2:5 w l lw 2 lt 3 ti "Fitted"'
	script += '\n\nreset'

	return script
################################################################################
#      Main     #
################################################################################
if __name__=='__main__':
	main()