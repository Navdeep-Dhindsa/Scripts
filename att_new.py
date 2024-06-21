import h5py
import os
from collections import defaultdict

def extract_values(file, group, pattern):
    """Extract unique values based on a pattern in the group names."""
    values = set()
    for key in group.keys():
        parts = key.split(pattern)
        if len(parts) > 1:
            try:
                value = parts[1].split('/')[0]
                values.add(value)
            except ValueError:
                pass
    return sorted(values)

def scan_combinations(file):
    """Scan the file to get all combinations of Nc, Nt, Nx, rt, and zeta."""
    combinations = defaultdict(list)
    for Nc in extract_values(file, file, 'Nc'):
        for Nt in extract_values(file, file[f'Nc{Nc}'], 'Nt'):
            for Nx in extract_values(file, file[f'Nc{Nc}/Nt{Nt}'], 'Nx'):
                for rt in extract_values(file, file[f'Nc{Nc}/Nt{Nt}/Nx{Nx}'], 'rt'):
                    for zeta in extract_values(file, file[f'Nc{Nc}/Nt{Nt}/Nx{Nx}/rt{rt}'], 'zeta'):
                        combinations[(Nc, Nt, Nx)].append((rt, zeta))
    return combinations

def extract_group_attributes(file, combinations):
    """Extract and save attributes for all groups to a text file."""
    output_file = "output_attributes/group_attributes.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as txtfile:
        txtfile.write("Nc Nt Nx rt zeta Ntraj Thermalization_cut Block_size Nblocks\n")
        
        for (Nc, Nt, Nx), rt_zeta_list in combinations.items():
            for rt, zeta in rt_zeta_list:
                path = f"Nc{Nc}/Nt{Nt}/Nx{Nx}/rt{rt}/zeta{zeta}"
                
                # Extract attributes for the group
                if path in file:
                    group_attrs = dict(file[path].attrs)
                    txtfile.write(f"{Nc} {Nt} {Nx} {rt} {zeta} {group_attrs.get('Ntraj', '')} "
                                  f"{group_attrs.get('thermalization cut', '')} "
                                  f"{group_attrs.get('block size', '')} "
                                  f"{group_attrs.get('Nblocks', '')}\n")

def extract_dataset_attributes(file, combinations, datasets):
    """Extract and save attributes for all datasets and combinations."""
    output_dir = "output_attributes"
    os.makedirs(output_dir, exist_ok=True)
    
    for dataset in datasets:
        with open(os.path.join(output_dir, f"{dataset}_attributes.txt"), 'w') as output_file:
            for (Nc, Nt, Nx), rt_zeta_list in combinations.items():
                for rt, zeta in rt_zeta_list:
                    path = f"Nc{Nc}/Nt{Nt}/Nx{Nx}/rt{rt}/zeta{zeta}"
                    dataset_path = f"{path}/{dataset}"
                    if dataset_path in file:
                        dataset_attrs = dict(file[dataset_path].attrs)
                        output_file.write(f"Dataset Path: {dataset_path}\n")
                        for attr_name, attr_value in dataset_attrs.items():
                            output_file.write(f"  {attr_name}: {attr_value}\n")
                        output_file.write("\n")
                    else:
                        output_file.write(f"Dataset Path: {dataset_path} does not exist\n\n")

# Main code
file_path = '2dQ4_data.h5'
datasets = [
    "Complexified_Wlines", "Fermion_op_eig", "Maldacena_loop", "Polyakov_loop",
    "SB", "Unitarized_Wlines", "bilin", "energy", "exp_dS", "link_trace",
    "meas", "plaq", "scalar_eig_ave", "scalar_sq"
]

with h5py.File(file_path, 'r') as file:
    combinations = scan_combinations(file)
    extract_group_attributes(file, combinations)
    extract_dataset_attributes(file, combinations, datasets)
