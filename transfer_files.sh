# Define the base directory and remote server path
localBaseDir="D:/1.OriginalProject/1. PhD project/2022 Files/1. ProjectMaterials/EEG/EEG-DATA"
remoteBaseDir="mhejazi@beluga.computecanada.ca:/lustre03/project/6067835/mhejazi/EEG-DATA"

# Define an array of subjects to exclude
excludeSubjects=(6 8 10 13 21 23 25 27)

# Loop through all subjects (1 to 29)
for num in $(seq -w 1 29); do
    if [[ " ${excludeSubjects[@]} " =~ " ${num} " ]]; then
        continue # Skip excluded subjects
    fi
    
    # Construct the source directory and the SCP command
    srcDir="${localBaseDir}/Sub-${num}"
    scp -r "$srcDir" "$remoteBaseDir/"
done

