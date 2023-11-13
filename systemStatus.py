#!/bin/env python3

import sys, getopt
import datetime
import time
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
    print(f'''\t -p | --process: \tprinc process section''')
    print(f'''\t -r | --resume: \tprint resume''')
    print(f'''\t -a | --all: \t\tprint all''')
    print(f'''\t -u | --update: \tenable autoupdate''')
    print(f'''\t -t | --time: \t\tspecify time of refresh ( > 0 )''')
    print(f'''\t -h | --help: \t\tprint this help''')

def resume():
    perc_cpu    = psutil.cpu_percent(interval = 1, percpu=True)
    mem_virt    = int(psutil.virtual_memory().used / (1024 ** 2))
    avail_mem   = int(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
    print(f'''Estado actual del PC:
          La CPU está al {perc_cpu}%
          Usando {mem_virt} Mb de la memoria
          Quedando {avail_mem}% memoria libre''')

def memory()->str:
    mem_virt        = int(psutil.virtual_memory().used / (1024 ** 2))
    mem_avail       = int(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
    mem_perc_used   = int(psutil.virtual_memory().percent)
    swap_total      = int(psutil.swap_memory().total / (1024 ** 2))
    swap_used       = int(psutil.swap_memory().used / (1024 ** 2))
    swap_free       = int(psutil.swap_memory().free / (1024 ** 2))
    swap_perc_used  = int(psutil.swap_memory().percent)
    swap_perc_free  = int(100 - swap_perc_used)
    swap_sin        = int(psutil.swap_memory().sin / (1024 ** 2))
    swap_sout       = int(psutil.swap_memory().sout / (1024 ** 2))


    memory_status = f''' Memoria:\n'''
    memory_status+= f'''\tUsando {mem_virt} Mb de la memoria, el {mem_perc_used}% del total\n'''
    memory_status+= f'''\tQuedando {mem_avail}% memoria libre\n'''
    memory_status+= f'''\t***Swap***\n'''
    memory_status+= f'''\tDispone de {swap_total} Mb \n'''
    memory_status+= f'''\tSe usan {swap_used} Mb, un {swap_perc_used}%\n'''
    memory_status+= f'''\tDispone de {swap_free} Mb libres, un {swap_perc_free}%\n'''
    if swap_sin > 0:
        memory_status+= f'''\tSe escribieron a disco {swap_sin} Mb\n'''
    if swap_sout > 0:
        memory_status+= f'''\tSe leyeron del disco {swap_sout} Mb\n'''
    
    return memory_status

def cpu()->str:
    perc_core       = psutil.cpu_percent(interval = 1, percpu=True)
    perc_cpu        = psutil.cpu_percent(interval = 1)
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
    cpu_status+= f'''\tFrecuencia de la CPU: {cpu_freq_curr}Hz ( min {cpu_freq_min}Hz max {cpu_freq_max}Hz )\n'''
    cpu_status+= f'''\t***Carga de la cpu***\n'''
    cpu_status+= f'''\tLa CPU está al {perc_cpu}%.\n'''
    cpu_status+= f'''\tCarga de la cpu: '''
    for x in psutil.getloadavg():
        cpu_status+=f'''{round(x / psutil.cpu_count() * 100,2)}%  '''
    cpu_status+="( hace 1min, 5min y 15min )\n"
    cpu_status+= f'''\tCarga  por hilo {perc_core}%\n'''
    cpu_status+= f'''\t***Tiempos de ejecución***\n'''
    cpu_status+= f'''\t{round(cpu_time_user / cpu_time_total * 100,2)}% ejecutandose en modo usuario\n'''
    cpu_status+= f'''\t{round(cpu_time_system / cpu_time_total * 100,2)}% ejecutandose en modo kernel\n'''
    cpu_status+= f'''\t{round(cpu_time_idle / cpu_time_total * 100,2)}% sin hacer nada\n'''
    cpu_status+= f'''\t{round(cpu_time_iowait / cpu_time_total * 100,2)}% esperando a completar I/O\n''' #solo linux
    cpu_status+= f'''\t{round(cpu_time_irq / cpu_time_total * 100,2)}% ejecutando interrupciones hardware\n''' #irq solo linux
    #cpu_status+= f'''\tLa CPU está al {perc_cpu}%\n'''

    return cpu_status

def disk()->str:
    disk_status = ""
    return disk_status

def network()->str:
    net_status = ""
    return net_status

def process()->str:
    proc_status = ""
    return proc_status

def all()->str:
    all = ""
    return all

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
    global_status  = ""
    refresh_time = -1

    opts, args = getopt.getopt(argv,"hrcmdnpaut:",["help","resume","cpu","memory","disk","network","process","all","update","time="])
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
        elif opt in ("-p","--process"):
            exec_proc_status = True
        elif opt in ("-a","--all"):
            exec_all_status = True
        elif opt in ("-t","--time"):
            if arg.isnumeric() == True:
                refresh_time = float(arg)
        elif opt in ("-u","--update"):
            exec_auto_update = True

    while(True):
        if refresh_time > 1:
            time.sleep(refresh_time)
        global_status = ""
        #timestamp = f'''{format(datetime.datetime.now().hour,'02')}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}'''
        timestamp = f'''{datetime.datetime.now().day:02d}/{datetime.datetime.now().month:02d}/{datetime.datetime.now().year:04d} {datetime.datetime.now().hour:02d}:{datetime.datetime.now().minute:02d}:{datetime.datetime.now().second:02d}'''
        if exec_resume == True:
            resume_status = resume()
            print(resume_status)
            continue
        if exec_all_status == True:
            all_status = all()
            print(all_status)
            continue
        if exec_cpu_status == True:
            cpu_status = cpu()
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
        if exec_proc_status == True:
            proc_status = process()
            global_status+= proc_status

        print(f'''\nEstado actual ({timestamp}) del PC *************************************************''')
        print(global_status)


        if exec_auto_update == False:
            break

if __name__ == '__main__' :
    try:
        main()
    except KeyboardInterrupt:
        print("")


        
            

    

