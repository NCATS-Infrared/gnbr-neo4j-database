# Set GNBR download url and folder
base_url="https://zenodo.org/record/1243969/files"
target_dir="$HOME/gnbr"
mkdir -p $target_dir
cd $target_dir

############ PART 1 DATA
curl ${base_url}/part-i-chemical-disease-path-theme-distributions.txt.gz -O 
curl ${base_url}/part-i-chemical-gene-path-theme-distributions.txt.gz -O
curl ${base_url}/part-i-gene-disease-path-theme-distributions.txt.gz -O
curl ${base_url}/part-i-gene-gene-path-theme-distributions.txt.gz -O

############# PART 2 DATA
curl ${base_url}/part-ii-dependency-paths-chemical-disease-sorted-with-themes.txt.gz -O
curl ${base_url}/part-ii-dependency-paths-chemical-gene-sorted-with-themes.txt.gz -O
curl ${base_url}/part-ii-dependency-paths-gene-disease-sorted-with-themes.txt.gz -O
curl ${base_url}/part-ii-dependency-paths-gene-gene-sorted-with-themes.txt.gz  -O