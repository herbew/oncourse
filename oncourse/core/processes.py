from __future__ import unicode_literals, absolute_import

import psutil
def get_process_id_by_name(name):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string name
    '''
    list_process = []
    
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if name.lower() in pinfo['name'].lower():
               list_process.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
            pass
        
    return [proc['pid'] for proc in list_process]