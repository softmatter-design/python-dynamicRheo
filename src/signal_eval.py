#!/usr/bin/env python
# -*- coding: utf-8 -*-
##### Import #####
from UDFManager import *
import sys
import os
import subprocess
import numpy as np
import platform
################################################################################
def main():
	#
	omega = 1.
	gamma0 = 1.
	resolution = 10
	period = 10
	cond = [omega, gamma0, resolution, period]
	input = generate_signal(cond)
	#
	sigma0 = 0.5
	delta = 0.2
	output = calc_sigma(input, omega, sigma0, delta)
	save_data(output, "output.dat")
	plotlis("output.dat")
	#
	nl = 0.03
	output2 = calc_sigma_wn(input, omega, sigma0, delta, nl)
	save_data(output2, "output2.dat")
	plotlis("output2.dat")

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
			input.append([time, gamma])
	return input

def calc_sigma(input, omega, sigma0, delta):
	sigma = []
	for dat in input:
		sigma.append([dat[0], dat[1], sigma0*np.sin(omega*dat[0] + delta)])
	return sigma

def calc_sigma_wn(input, omega, sigma0, delta, nl):
	sigma = []
	for dat in input:
		sigma.append([dat[0], dat[1], np.random.normal(loc= 1., scale=nl)*sigma0*np.sin(omega*dat[0] + delta)])
	return sigma

############################################################################
def save_data(target, f_data):
	with open(f_data,'w') as f:
		for line in target:
			for data in line:
				f.write(str(data) + '\t')
			f.write('\n')
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
	script += 'plot	data u 2:3 w l lw 2 lt 1 ti "Stress"'
	script += '\n\nreset'

	return script
################################################################################
#      Main     #
################################################################################
if __name__=='__main__':
	main()