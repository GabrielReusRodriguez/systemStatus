#!/bin/env python3

import sys, getopt
import datetime
import time
from pathlib import Path
import psutil

#https://psutil.readthedocs.io/en/latest/

PROGRAM_NAME    = "systemStatus.py"
PROGRAM_VERSION = "1.0"
PROGRAM_AUTHOR  = "Gabriel Reus ; https://github.com/GabrielReusRodriguez"

def help():
	print(f'''{PROGRAM_NAME} v{PROGRAM_VERSION} by {PROGRAM_AUTHOR}''')
	print(f''' Use:''')
	print(f'''\t -c | --cpu: \t\tprint cpu section''')
	print(f'''\t -m | --memory: \tprint memory section''')
	print(f'''\t -d | --disk: \t\tprint disk section''')
	print(f'''\t -n | --network: \tprint network section''')
	#print(f'''\t -p | --process: \tprint process section''')
	print(f'''\t -r | --resume: \tprint resume''')
	print(f'''\t -a | --all: \t\tprint all''')
	print(f'''\t -u | --update: \tenable autoupdate''')
	print(f'''\t -t | --time: \t\tspecify time of refresh ( > 0 )''')
	print(f'''\t -s | --sensor: \t\tcheck CPUs Temperatures''')
	print(f'''\t -b | --boot: \t\tget boot time''')
	print(f'''\t -h | --help: \t\tprint this help''')

def format_memory(size: int)->str:

	human_size = size
	aux_size = size
	iteration = 0
	str_size = ""
	while( aux_size >= 1024):
		aux_size = int (aux_size / 1024)
		human_size = aux_size
		iteration = iteration + 1
	str_size = str(human_size)

	if iteration == 0:
		str_size+=" b"
	elif iteration == 1:
		str_size+=" Kb"
	elif iteration == 2:
		str_size+=" Mb"
	elif iteration == 3:
		str_size+=" Gb"
	elif iteration == 4:
		str_size+=" Tb"
	
	return str_size

def memory()->str:
	mem_virt        = psutil.virtual_memory().used
	mem_avail       = int(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
	mem_perc_used   = int(psutil.virtual_memory().percent)
	swap_total      = psutil.swap_memory().total
	swap_used       = psutil.swap_memory().used
	swap_free       = psutil.swap_memory().free
	swap_perc_used  = int(psutil.swap_memory().percent)
	swap_perc_free  = int(100 - swap_perc_used)
	swap_sin        = psutil.swap_memory().sin
	swap_sout       = psutil.swap_memory().sout


	memory_status = f''' Memoria:\n'''
	memory_status+= f'''\t{format_memory(psutil.virtual_memory().total)} Mb de memoria TOTAL\n'''
	memory_status+= f'''\tUsado un {mem_perc_used}% de memoria ({format_memory(mem_virt)}) y {mem_avail}% de memoria libre \n'''
	memory_status+= f'''\t***Swap***\n'''
	memory_status+= f'''\t{format_memory(swap_total)} de espacio TOTAL \n'''
	memory_status+= f'''\tUsado un {swap_perc_used}% ({format_memory(swap_used)} ) \n'''
	memory_status+= f'''\tDispone de {format_memory(swap_free)} libres, un {swap_perc_free}%\n'''
	if swap_sin > 0:
		memory_status+= f'''\tSe escribieron a disco {format_memory(swap_sin)}\n'''
	if swap_sout > 0:
		memory_status+= f'''\tSe leyeron del disco {format_memory(swap_sout)}\n'''
	
	return memory_status

def cpu(intervalo: int = 1)->str:
	perc_core       = psutil.cpu_percent(interval = intervalo, percpu=True)
	perc_cpu        = psutil.cpu_percent(interval = intervalo)
	cpu_times       = psutil.cpu_times() #percpu =True OPTIONAL PARAM
	cpu_time_user   = cpu_times.user
	cpu_time_system = cpu_times.system
	cpu_time_idle   = cpu_times.idle
	cpu_time_iowait = cpu_times.iowait
	cpu_time_irq    = cpu_times.irq
	cpu_time_total  = cpu_time_user + cpu_time_idle + cpu_time_iowait + cpu_time_irq + cpu_time_system
	core_load       = psutil.getloadavg()

	cpu_freq        = psutil.cpu_freq(percpu = False)
	cpu_freq_curr   = int(cpu_freq.current)
	cpu_freq_max    = int(cpu_freq.max)
	cpu_freq_min    = int(cpu_freq.min)

	cpu_status  = f''' CPU:\n'''
	cpu_status+= f'''\t Frecuencia de la CPU: {cpu_freq_curr}Hz ( min {cpu_freq_min}Hz max {cpu_freq_max}Hz )\n'''
	cpu_status+= f'''\t***Carga de la cpu***\n'''
	cpu_status+= f'''\t La CPU está al {perc_cpu}%.\n'''
	cpu_status+= f'''\t Carga de la cpu: '''
	for x in psutil.getloadavg():
		cpu_status+=f'''{round(x / psutil.cpu_count() * 100,2)}%  '''
	cpu_status+="( hace 1min, 5min y 15min )\n"
	cpu_status+= f'''\t Carga  por hilo {perc_core}%\n'''
	cpu_status+= f'''\t***Tiempos de ejecución***\n'''
	cpu_status+= f'''\t {round(cpu_time_user / cpu_time_total * 100,2)}% ejecutandose en modo usuario\n'''
	cpu_status+= f'''\t {round(cpu_time_system / cpu_time_total * 100,2)}% ejecutandose en modo kernel\n'''
	cpu_status+= f'''\t {round(cpu_time_idle / cpu_time_total * 100,2)}% sin hacer nada\n'''
	cpu_status+= f'''\t {round(cpu_time_iowait / cpu_time_total * 100,2)}% esperando a completar I/O\n''' #solo linux
	cpu_status+= f'''\t {round(cpu_time_irq / cpu_time_total * 100,2)}% ejecutando interrupciones hardware\n''' #irq solo linux
	#cpu_status+= f'''\tLa CPU está al {perc_cpu}%\n'''

	return cpu_status

def disk()->str:

	disk_status = f''' Disco:\n'''

	disk_counters = psutil.disk_io_counters(perdisk=True)

	valid_file_extensions = ("ext2","ext3","ext4","fat32")
	disk_partitions = psutil.disk_partitions( all = False)
	for partition in disk_partitions:
		if partition.fstype in valid_file_extensions:
			#print(partition.device)
			disk_status+= f'''\tDevice: {partition.device} , fileType : {partition.fstype},  mountpoint : {partition.mountpoint}\n'''
			disk_usage = psutil.disk_usage(partition.mountpoint)
			disk_status+= f'''\t\tTotal: {format_memory(disk_usage.total)} , usado: {format_memory(disk_usage.used)} , libre: {format_memory(disk_usage.free)} , porcentaje usado: {disk_usage.percent}%\n'''
			disk_counter = disk_counters[Path(partition.device).name]
			disk_status+= f'''\t\tLeido: {format_memory(disk_counter.read_bytes)} , Escrito: {format_memory(disk_counter.write_bytes)} \n'''
	
	return disk_status

def network()->str:
	
	net_status = f''' Red:\n'''
	net_status+= f'''\t***Interfaces***\n'''
	ips_by_if = psutil.net_if_addrs()
	#print(ips_by_if )
	net_statistics = psutil.net_io_counters(pernic=True)
	for interface in net_statistics.keys():
		net_interface = net_statistics[interface]
		net_status+= f'''\t {interface}\n'''
		ips = ips_by_if[interface]
		net_status+= f'''\t\t'''
		for address in ips:
			if address.family == 2:
				net_status+= f'''Ip v4: {address.address} '''
			if address.family == 10:
				net_status+= f'''Ip v6: {address.address} '''
			if address.family == 17:
				net_status+= f'''MAC: {address.address} '''
		net_status+="\n"
		net_status+= f'''\t\tRecibidos: {format_memory(net_interface.bytes_recv)}, Enviados: {format_memory(net_interface.bytes_sent)}\n'''
		net_status+= f'''\t\tError recepción: {net_interface.errin}, Error envío: {format_memory(net_interface.errout)}\n'''
		net_status+= f'''\t\tDrops recepción: {format_memory(net_interface.dropin)}, Drops envío: {format_memory(net_interface.dropout)}\n'''
	net_status+= f'''\t***Conexiones***\n'''
	conexiones = psutil.net_connections(kind='all')
	for conexion in conexiones:
		#print(conexion)
		if conexion.status == 'NONE':
			continue
		if conexion.family == 2 or conexion.family == 10: #las conexiones AF_INET = 2 AF_INET6 = 10
			net_status+= f'''\t\t origen= {conexion.laddr.ip}:{conexion.laddr.port}'''
			#if not conexion.raddr == False: #Check if it is empty
			if len(conexion.raddr) > 0: #Check if it is empty
			#	net_status+= f''' destino= {conexion.raddr.ip}:{conexion.raddr.port}'''
				net_status+= f''', destino= {conexion.raddr.ip}:{conexion.raddr.port}'''
			net_status+= f''' , status={conexion.status}, pid={conexion.pid}'''				
			net_status+="\n"

	return net_status

#TODO: proces
#def process()->str:
#	proc_status = ""
#	return proc_status

def sensors()->str:
	sensor_status = f''' Sensors:\n'''
	sensors_temperatura = psutil.sensors_temperatures(fahrenheit=False)
	for sensor_temp in sensors_temperatura:
		#print(sensor[1])
		temperatura = sensors_temperatura[sensor_temp]
		for item in temperatura:
			if item.label.startswith("Core"):
				sensor_status+=f'''\t{item.label} current: {item.current}º C , high: {item.high}º C critical: {item.critical}º C\n'''

	#TODO cuando tenga un portatil
	#sensors_bateria = psutil.sensors_battery()
	#if sensors_bateria != None:
	#	print(sensors_bateria.percet)
	return sensor_status

def boot()->str:
	boot_status = ""
	boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
	boot_status = f''' Boot time:\n'''
	boot_status+= f'''\t{boot_time}'''
	return boot_status

def all(intervalo_cpu: int = 1)->str:
	all = ""
	all+=cpu(intervalo = intervalo_cpu)
	all+=memory()
	all+=disk()
	all+=network()
	all+=sensors()
	all+=boot()
	return all

def resume(intervalo_cpu: int = 1):
	resumen = ""
	resumen+=cpu(intervalo = intervalo_cpu)
	resumen+=memory()
	#resumen+=disk()
	#resumen+=network()
	resumen+=sensors()
	resumen+=boot()
	return resumen


def main():
	argv = sys.argv[1:]
	#opts, args = getopt.getopt(argv,"h",["ifile=","ofile="])
	cpu_status = ""
	exec_cpu_status = False
	memory_status = ""
	exec_memory_status = False
	disk_status =""
	exec_disk_status = False
	net_status =""
	exec_net_status = False
	proc_status = ""
	exec_proc_status = False
	all_status = ""
	exec_all_status = False
	exec_auto_update = False
	resume_status =""
	exec_resume = False
	exec_sensor = False
	sensor_status = ""
	exec_boot = False
	boot_status = ""
	global_status  = ""
	refresh_time = -1
	intervalo_cpu = 1

	try:
		#opts, args = getopt.getopt(argv,"hrcmdnpaut:sb",["help","resume","cpu","memory","disk","network","process","all","update","time=","sensor","boot"])
		opts, args = getopt.getopt(argv,"hrcmdnaut:sb",["help","resume","cpu","memory","disk","network","all","update","time=","sensor","boot"])
	except getopt.GetoptError:
		print("Error al parsear los parámetros.")
		sys.exit(1)
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			help()
			sys.exit()
		elif  opt in ("-r","--resume"):
			exec_resume = True
		elif opt in ("-c","--cpu"):
			exec_cpu_status = True
		elif opt in ("-m","--memory"):
			exec_memory_status = True
		elif opt in ("-d","--disk"):
			exec_disk_status = True
		elif opt in ("-n","--network"):
			exec_net_status = True
		#elif opt in ("-p","--process"):
		#	exec_proc_status = True
		elif opt in ("-a","--all"):
			exec_all_status = True
		elif opt in ("-t","--time"):
			if arg.isnumeric() == True:
				refresh_time = float(arg)
		elif opt in ("-u","--update"):
			exec_auto_update = True
		elif opt in ("-s","--sensor"):
			exec_sensor = True
		elif opt in ("-b","--boot"):
			exec_boot = True
		else:
			pass

	while(True):
		if refresh_time > 1:
			time.sleep(refresh_time)
		global_status = ""
		#timestamp = f'''{format(datetime.datetime.now().hour,'02')}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}'''
		timestamp = f'''{datetime.datetime.now().day:02d}/{datetime.datetime.now().month:02d}/{datetime.datetime.now().year:04d} {datetime.datetime.now().hour:02d}:{datetime.datetime.now().minute:02d}:{datetime.datetime.now().second:02d}'''
		if exec_resume == True:
			resume_status = resume()
			global_status+= resume_status
			print(f'''\nEstado actual ({timestamp}) *************************************************''')
			print(global_status)
			if exec_auto_update == False:
				break
			else:
				continue
		if exec_all_status == True:
			all_status = all()
			global_status+= all_status
			print(f'''\nEstado actual ({timestamp}) *************************************************''')
			print(global_status)
			if exec_auto_update == False:
				break
			else:
				continue
		if exec_cpu_status == True:
			cpu_status = cpu(intervalo = intervalo_cpu)
			global_status+= cpu_status
		if exec_memory_status == True:
			memory_status = memory()
			global_status+= memory_status
		if exec_disk_status == True:
			disk_status = disk()
			global_status+= disk_status
		if exec_net_status == True:
			net_status = network()
			global_status+= net_status
		#if exec_proc_status == True:
		#	proc_status = process()
		#	global_status+= proc_status
		if exec_sensor == True:
			sensor_status = sensors()
			global_status+= sensor_status
		if exec_boot == True:
			boot_status = boot()
			global_status+= boot_status

		print(f'''\nEstado actual ({timestamp}) *************************************************''')
		print(global_status)
		

		if exec_auto_update == False:
			break

if __name__ == '__main__' :
	try:
		main()
	except KeyboardInterrupt:
		print("")


		
			

	

