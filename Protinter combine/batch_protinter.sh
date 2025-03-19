#!/bin/bash

# Loop over all .pdb files in the directory
for pdb in *.pdb; do
    echo "Processing $pdb..."
    
    # 1. Run protinter on the pdb file
    protinter --hydrophobic --hb2 --arosul --hb3 --disulphide --ionic --hb1 --catpi --aroaro -csv "$pdb"
    
    # 2. Run the Python script to calculate the parameters
    # Make sure process_csv.py is in the same directory or provide its full path.
    python combine_nba.py
    
    # 3. Rename the output combined_results.csv to match the pdb file name (with .csv extension)
    base=$(basename "$pdb" .pdb)
    mv combined_results.csv "${base}.csv"
    
    # 4. Delete the protinter-generated CSV files
    rm -f result_hydrophobic.csv result_hbond_main_side.csv result_arosul.csv result_hbond_side_side.csv result_disulphide.csv result_ionic.csv result_hbond_main_main.csv result_cationpi.csv result_aroaro.csv

    echo "Finished processing $pdb. Output saved as ${base}.csv"
done

echo "All files processed."
