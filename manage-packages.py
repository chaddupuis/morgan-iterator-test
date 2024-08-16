import shutil
import subprocess
import os
import sys
import shutil



"""
Starts with python3 manage-packages.py new|all
new will diff what packages are there and only do new ones for each env
all will go through all existing packages and update
"""

if not sys.argv[1:]:
    print("you must enter an action to take 'all' or 'new'... exiting...")
    sys.exit()

if sys.argv[1] not in ('new', 'all'):
    print("Your action must be 'all' or 'new'... exiting...")
    sys.exit()
else:
    what_action = sys.argv[1]

print(f'going to do ::: {what_action}')

"""
Iterate packages list with versions and put into a list to pull individually - this allows multiple versions of the same package with morgan does not otherwsise all
"""


"""
RIGHT NOW JUST DOING ALL EVERYTIME - TODO ADD DIFFS AND HOLDER TO ITERATE JUST NEW
"""

main_packages_path = '/usr/app/'
main_packages_file = ''
if what_action == "new":
    ## handle only new packages
    if os.environ["AMIPROD"] == "dev":
        main_packages_file = 'dev-packages.ini'
    else:
        main_packages_file = 'prod-packages.ini'

elif what_action == "all":
    ## update all current packages
    if os.environ["AMIPROD"] == "dev":
        main_packages_file = 'dev-packages.ini'
    else:
        main_packages_file = 'prod-packages.ini'

else:
    print("you have to have a packages file... exiting...")
    sys.exit()

main_packages = main_packages_path+main_packages_file

def read_and_split(filename):
    result_list = []  # Initialize an empty list to store the data

    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)  # Split by the first '='
            result_list.append([key.strip(), value.strip()])  # Add to the list

    return result_list

'''
Create a list of lists of package / version written into morgan.ini 
one at a time below to allow for multiple versions of the same package
'''
packages_list = read_and_split(main_packages)

# Dict of env builders:
environments = []
env_groupings = ()
'''
env names just have to be unique 
but are currently "w" [win] or "l" [linux] "p" [python] 
full version like 3.8.17 3817 
--- so "lp3817"
'''

''' 
following function is a matching iterator to lump the environments together
that should work - ie all 3.10 and 3.11 for example, but not 3.8 and 3.11
this speeds it up a bit vs. iterating every package for every environment
'''
def return_matching_envs(environments, env_groupings, env_group_to_match):
    envs_to_return = []

    if len(env_group_to_match) == 2:   # it is a "global" 
        for env in environments:  
#            if ((env['envname'][4:-2] not in env_groupings) and (env['envname'][4:-1] not in env_groupings)) and (env['envname'][4:-4] == env_group_to_match):
            if ((env['envname'][4:-2] not in env_groupings) and (env['envname'][4:-1] not in env_groupings)) and (env['envname'][4:6] == env_group_to_match):
                envs_to_return.append(env)

    else:
        for env in environments:
            if env['envname'][4:-2] == env_group_to_match or env['envname'][4:-1] == env_group_to_match:
                envs_to_return.append(env)

    return envs_to_return

if os.environ["AMIPROD"] == "dev":
    environments = [
        {'envname': 'env.lp3817', 'os_name': 'posix', 'sys_platform': 'linux', 'platform_machine': 'x86_64', 'platform_python_implementation': 'cpython', 'platform_system': 'Linux', 'python_version': '3.8', 'python_full_version': '3.8.17', 'implementation_name': 'cpython'},
        {'envname': 'env.lp3919', 'os_name': 'posix', 'sys_platform': 'linux', 'platform_machine': 'x86_64', 'platform_python_implementation': 'cpython', 'platform_system': 'Linux', 'python_version': '3.9', 'python_full_version': '3.9.19', 'implementation_name': 'cpython'},
        {'envname': 'env.lp31014', 'os_name': 'posix', 'sys_platform': 'linux', 'platform_machine': 'x86_64', 'platform_python_implementation': 'cpython', 'platform_system': 'Linux', 'python_version': '3.10', 'python_full_version': '3.10.14', 'implementation_name': 'cpython'}
    ]
    env_groupings = ( 'lp38', 'lp' )
    # lp is everything not in the array - to lp38, lp will to 38 alone and then all else at once
else:
    environments = [
        {'envname': 'env.lp3817', 'os_name': 'posix', 'sys_platform': 'linux', 'platform_machine': 'x86_64', 'platform_python_implementation': 'cpython', 'platform_system': 'Linux', 'python_version': '3.8', 'python_full_version': '3.8.17', 'implementation_name': 'cpython'},
        {'envname': 'env.lp3919', 'os_name': 'posix', 'sys_platform': 'linux', 'platform_machine': 'x86_64', 'platform_python_implementation': 'cpython', 'platform_system': 'Linux', 'python_version': '3.9', 'python_full_version': '3.9.19', 'implementation_name': 'cpython'},
        {'envname': 'env.lp3109', 'os_name': 'posix', 'sys_platform': 'linux', 'platform_machine': 'x86_64', 'platform_python_implementation': 'cpython', 'platform_system': 'Linux', 'python_version': '3.10', 'python_full_version': '3.10.9', 'implementation_name': 'cpython'},
        {'envname': 'env.lp3109', 'os_name': 'posix', 'sys_platform': 'linux', 'platform_machine': 'x86_64', 'platform_python_implementation': 'cpython', 'platform_system': 'Linux', 'python_version': '3.10', 'python_full_version': '3.10.12', 'implementation_name': 'cpython'},
        {'envname': 'env.lp3111', 'os_name': 'posix', 'sys_platform': 'linux', 'platform_machine': 'x86_64', 'platform_python_implementation': 'cpython', 'platform_system': 'Linux', 'python_version': '3.11', 'python_full_version': '3.11.1', 'implementation_name': 'cpython'},
        {'envname': 'env.wp3105', 'os_name': 'nt', 'sys_platform': 'win32', 'platform_machine': 'AMD64', 'platform_python_implementation': 'CPython', 'platform_system': 'Windows', 'python_version': '3.10', 'python_full_version': '3.10.5', 'implementation_name': 'cpython'}
    ]
    env_groupings = ( 'lp38', 'lp', 'wp' )

# file we are creating and location of it (where morgan mirror is running)
env_file = 'morgan-env-holder.ini'
env_path = '/usr/app/'
morgan_env=env_path+env_file

# above is the env iterator and this becomes the package iterator per env
final_file = 'morgan.ini'
final_path = '/usr/app/'
morgan_final=final_path+final_file

#env_path = '/usr/app/'

for envgroup in env_groupings:
    print(f'working on {envgroup}')
    print(f'=====================')
    envs_to_process = return_matching_envs(environments, env_groupings, envgroup)
    print(f'cleaning env holders before starting iterations')
    print(f'========================================')
    print(f'========================================')
    print(f'========================================')
    print(f'========================================')
    print(f'========================================')
    print(f'========================================')
    print(envs_to_process)
    print(f'========================================')
    print(f'========================================')
    print(f'========================================')
    print(f'========================================')
    print(f'========================================')
    print(f'========================================')
    if os.path.isfile(morgan_env):
        os.remove(morgan_env)
    if os.path.isfile(morgan_final):
        os.remove(morgan_final)

    for environment in range(len(envs_to_process)):
        with open(morgan_env, "a") as f:
            f.write(f'[{envs_to_process[environment]["envname"]}]\n')
            f.write(f'os_name = {envs_to_process[environment]["os_name"]}\n')
            f.write(f'sys_platform = {envs_to_process[environment]["sys_platform"]}\n')
            f.write(f'platform_machine = {envs_to_process[environment]["platform_machine"]}\n')
            f.write(f'platform_python_implementation = {envs_to_process[environment]["platform_python_implementation"]}\n')
            f.write(f'platform_system = {envs_to_process[environment]["platform_system"]}\n')
            f.write(f'python_version = {envs_to_process[environment]["python_version"]}\n')
            f.write(f'python_full_version = {envs_to_process[environment]["python_version"]}\n')
            f.write(f'implementation_name = {envs_to_process[environment]["implementation_name"]}\n')
        f.close()
    # add the final requirements line to start iterate packages through
    with open(morgan_env, "a") as f:
        f.write(f'\n[requirements]\n')
    f.close()
        
    for pkg in packages_list:
        # iterate packages list of lists packagename[0] = version[1]
        print(f'{pkg[0]} = {pkg[1]}')
        shutil.copyfile(morgan_env, morgan_final) 
        with open(morgan_final, "a") as pf:
            pf.write(f'{pkg[0]} = {pkg[1]}')
        pf.close()

        print(f'Running mirror on {envgroup} group now for {pkg[0]} - {pkg[1]}')
        # now run the mirror with this env and this package
        try:
            morgan_load = subprocess.run(["/root/.local/bin/morgan", "mirror"],timeout=1800)
        except:
            print(f'Passed on {envgroup} group skipping ::: {pkg[0]} - {pkg[1]}')
            pass

print("should have all packages now")
print("cleaning up")
# remove our empty env file
os.remove(morgan_env)
# ensure morgan.ini is an empty file 
shutil.copyfile("/usr/app/empty-env.ini",morgan_final)

# # iterate through env dict and to do mirroring for each env
# for env in range(len(environments)):

#     '''
#     each morgan.ini looks like:
#     [env.RHp39]
#     os_name = posix
#     sys_platform = linux
#     platform_machine = x86_64
#     platform_python_implementation = CPython
#     platform_system = Linux
#     python_version = 3.9
#     python_full_version = 3.9.13
#     implementation_name = cpython

#     [requirements]
#     packagename = >= version
#     '''
#     with open(morgan_env, "w") as f:
#         f.write(f'[{environments[env]["envname"]}]\n')
#         f.write(f'os_name = {environments[env]["os_name"]}\n')
#         f.write(f'sys_platform = {environments[env]["sys_platform"]}\n')
#         f.write(f'platform_machine = {environments[env]["platform_machine"]}\n')
#         f.write(f'platform_python_implementation = {environments[env]["platform_python_implementation"]}\n')
#         f.write(f'platform_system = {environments[env]["platform_system"]}\n')
#         f.write(f'python_version = {environments[env]["python_version"]}\n')
#         f.write(f'python_full_version = {environments[env]["python_version"]}\n')
#         f.write(f'implementation_name = {environments[env]["implementation_name"]}\n')
#         f.write(f'\n[requirements]\n')
#     f.close()

#     for pkg in packages_list:
#         # iterate packages list of lists packagename[0] = version[1]
#         print(f'{pkg[0]} = {pkg[1]}')
#         shutil.copyfile(morgan_env, morgan_final) 
#         with open(morgan_final, "a") as pf:
#             pf.write(f'{pkg[0]} = {pkg[1]}')
#         pf.close()

#         print(f'Running mirror on {environments[env]["envname"]} now for {pkg[0]} - {pkg[1]}')
#         # now run the mirror with this env and this package
#         try:
#             morgan_load = subprocess.run(["/root/.local/bin/morgan", "mirror"],timeout=1800)
#         except:
#             print(f'Passed on {environments[env]["envname"]} skipping ::: {pkg[0]} - {pkg[1]}')
#             pass

# print("should have all packages now")
# print("cleaning up")
# # remove our empty env file
# os.remove(morgan_env)
# # ensure morgan.ini is an empty file 
# shutil.copyfile("/usr/app/empty-env.ini",morgan_final)


