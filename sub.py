import os
import json
import shutil 
import psutil
import subprocess

class run:
    def __init__(self):
        pass

    def GetFolderName(self):
        """
        Get a project folder for docking
        """
        self.project = input("Enter a project name:")

    def CheckFolderExists(self):
        """
        Check the folder exists or not,
        if exists and want to resume docking process, return '1',
        else if exists and want to change the project name, return '2',
        else return Flase
        """
        if os.path.exists("./projects/" + self.project):
            print(
    """
    It seems that the project folder is exist.
    Which action do want to choose?
    (1) Continue docking process
    (2) Change the project name
    """)
            return input("Option:")
        else:
            return False

    # config
    def set_config(self):
        config = {}

        # project
        config["project"] = self.project

        # PDBFile
        PDBFiles = []
        for i in os.listdir("./Proteins/"):
            if i[-4:] == ".pdb":
                PDBFiles.append(i)
        for i, _ in enumerate(PDBFiles):
            print(f"{[i]}: {_}")
        file = PDBFiles[int(input("Please select a PDBFile:"))]
        os.mkdir(f"./projects/{self.project}/Protein")
        shutil.copy(f"./Proteins/{file}", f"./projects/{self.project}/Protein")
        config["PDBfile"] = self.PDBfile = f"./projects/{self.project}/Protein/{file}"

        # Drug library
        for i, _ in enumerate(os.listdir("./Drugs/")):
            print(f"{[i]}: {_}")
        config["DrugLib"] = self.DrugLib = "./Drugs/" + os.listdir("./Drugs/")[int(input("Please select a folder of drug library:"))] + "/"

        # cores
        print("Your CPU has " + str(psutil.cpu_count(logical = False)) + " cores.")
        config["cores"] = self.cores = int(input("Number of process to use:"))

        # mode
        modes = {"Standard" :[200, 70,  2], 
                 "Stable"   :[300, 80, 10],
                 "Accurate" :[800, 80, 10],
                 "Screening":[200, 70,  3],
                 "Quick"    :[150, 70,  1],
                 "Custom"   :["-","-","-"]}

        for i, _ in enumerate(modes.keys()):
            print(f"[{i}] {_:9} PopSize:{modes[_][0]}, Generations:{modes[_][1]}, Number of solutions:{modes[_][2]}")
        print()
        mode = int(input("Select mode:"))

        if mode == 5:
            config["PopSize"] = self.PopSize = int(input("PopSize:"))
            config["Generations"] = self.Generations = int(input("Generations:"))
            config["Solutions"] = self.Solutions = int(input("Solutions:"))
        else:
            config["PopSize"] = self.PopSize = modes[list(modes.keys())[mode]][0]
            config["Generations"] = self.Generations = modes[list(modes.keys())[mode]][1]
            config["Solutions"] = self.Solutions = modes[list(modes.keys())[mode]][2]
        
        # save config
        with open(f'./projects/{self.project}/config.json', 'w') as f:
            json.dump(config, f)
    
    # Prepare drugs
    def drug_prepare(self):
        self.drug_list = []
        with open("drug_list.txt", 'w') as f:
            for i in os.listdir(self.DrugLib):
                f.writelines(self.DrugLib+i+'\n')
                self.drug_list.append(os.path.splitext(i)[0])
        self.DrugFileType = os.path.splitext(i)[1]
        return self.drug_list

    # Get not dock yet drugs list
    def get_not_dock_drugs(self):
        docked_drug_list = []
        for i in os.listdir(f"./projects/{self.project}/best_Pose/"):
            docked_drug_list.append(i[len(self.PDBfile)-3:-6])
        return list(set(self.drug_list) - set(docked_drug_list))

    # run
    def dock(self, drug):
        # run program  
        proc = subprocess.Popen(["bin\mod_ga", 
                                 "-d", 
                                 f"./projects/{self.project}/", 
                                 f"{self.PopSize}", 
                                 f"{self.PDBfile}", 
                                 f"{drug}"] + f"6 1 1 1 2 0 {self.Generations} {self.Solutions} 1 0 0".split(), stdout=subprocess.PIPE)
        return proc.pid


