# %%
import sub
import os
import json
import time
import signal
import platform
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool

# %%
if __name__ == '__main__':
    a = sub.run()
    while True:
        Resume = False
        a.GetFolderName()
        print("Creating project...")
        Exists = a.CheckFolderExists()
        if Exists == '1':
            Resume = True
            break
        elif not Exists:
            os.mkdir(f"./projects/{a.project}")
            os.mkdir(f"./projects/{a.project}/drug_list")
            os.mkdir(f"./projects/{a.project}/best_Pose")
            os.mkdir(f"./projects/{a.project}/docked_Pose")
            os.mkdir(f"./projects/{a.project}/gemdock_out")
            break

    if Resume:
        print('Resume...')
        #load config
        with open(f'./projects/{a.project}/config.json', 'r') as f:
            config = json.load(f)
        a.project = config['project']
        a.PDBfile = config['PDBfile']
        a.DrugLib = config['DrugLib']
        a.cores = config['cores']
        a.PopSize = config['PopSize']
        a.Generations = config['Generations']
        a.Solutions = config['Solutions']
    else:
        print('Set configuration:')
        a.set_config()
    
    # Prepare drugs
    print('Prepare drugs...')
    drug_list = a.drug_prepare()
    if Resume:
        drug_list = a.get_not_dock_drugs()

    drug_path_list = []
    for i in drug_list:
        drug_path_list.append(a.DrugLib + i + a.DrugFileType + '\n')
    drug_path_list = np.array(drug_path_list)
    
    # Split drugs list by number of cores usage
    path = []
    for _, i in enumerate(np.array_split(drug_path_list, a.cores)):
        with open(f"./projects/{a.project}/drug_list/drug_list_{_}.txt", 'w') as f:
            path.append(f"./projects/{a.project}/drug_list/drug_list_{_}.txt")
            for j in i:
                f.writelines(j)

    # Docking
    print('Docking...')
    pids = []
    with Pool(processes=a.cores) as pool:
        for i in pool.imap_unordered(a.dock, path):
            pids.append(i)


    # Timer
    time.sleep(5)

    number_of_drugs = len(drug_list)
    t0 = time.time()
    done = len(os.listdir(f"./projects/{a.project}/best_Pose/"))
    print("Press 'n' to stop docking")
    import msvcrt
    with tqdm(total=number_of_drugs-done) as pbar:
            
        while True:
            new_done = len(os.listdir(f"./projects/{a.project}/best_Pose/")) - done
            done = len(os.listdir(f"./projects/{a.project}/best_Pose/"))
            pbar.update(new_done)

            stop = False
            if msvcrt.kbhit():
                if msvcrt.getch() == b'n':
                    stop = True
            if stop:
                for i in pids:
                    os.kill(i, signal.SIGTERM)
                break

            time.sleep(1)



