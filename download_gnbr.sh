# Set input folder
mkdir ../data

base_data="../data"

mkdir -p ${base_data}"/GNBR"
GNBR_dir=${base_data}"/GNBR"
# mkdir -p ${base_data}"/CTD"
# CTD_dir=${base_data}"/CTD"
# mkdir -p ${base_data}"/pubtator"
# pub_dir=${base_data}"/pubtator"

# Download GNBR theme data and entity mappings

############ PART 1 DATA
wget https://zenodo.org/record/1134693/files/part-i-chemical-disease-path-theme-distributions.txt -O ${GNBR_dir}/part-i-chemical-disease-path-theme-distributions.txt
# rm ${GNBR_dir}/part-i-chemical-disease-path-theme-distributions.txt


wget https://zenodo.org/record/1134693/files/part-i-chemical-gene-path-theme-distributions.txt -O ${GNBR_dir}/part-i-chemical-gene-path-theme-distributions.txt
# rm ${GNBR_dir}/part-i-chemical-gene-path-theme-distributions.txt


wget https://zenodo.org/record/1134693/files/part-i-gene-disease-path-theme-distributions.txt -O ${GNBR_dir}/part-i-gene-disease-path-theme-distributions.txt
# rm ${GNBR_dir}/part-i-gene-disease-path-theme-distributions.txt


wget https://zenodo.org/record/1134693/files/part-i-gene-gene-path-theme-distributions.txt -O ${GNBR_dir}/part-i-gene-gene-path-theme-distributions.txt
# rm ${GNBR_dir}/part-i-gene-gene-path-theme-distributions.txt

############# PART 2 DATA
wget https://zenodo.org/record/1134693/files/part-ii-dependency-paths-chemical-disease-sorted-with-themes.txt -O ${GNBR_dir}/part-ii-dependency-paths-chemical-disease-sorted-with-themes.txt
# rm ${GNBR_dir}/part-ii-dependency-paths-chemical-disease-sorted-with-themes.txt


wget https://zenodo.org/record/1134693/files/part-ii-dependency-paths-chemical-gene-sorted-with-themes.txt -O ${GNBR_dir}/part-ii-dependency-paths-chemical-gene-sorted-with-themes.txt
# rm ${GNBR_dir}/part-ii-dependency-paths-chemical-gene-sorted-with-themes.txt


wget https://zenodo.org/record/1134693/files/part-ii-dependency-paths-gene-disease-sorted-with-themes.txt -O ${GNBR_dir}/part-ii-dependency-paths-gene-disease-sorted-with-themes.txt
# rm ${GNBR_dir}/part-ii-dependency-paths-gene-disease-sorted-with-themes.txt


wget https://zenodo.org/record/1134693/files/part-ii-dependency-paths-gene-gene-sorted-with-themes.txt  -O ${GNBR_dir}/part-ii-dependency-paths-gene-gene-sorted-with-themes.txt
# rm ${GNBR_dir}/part-ii-dependency-paths-gene-gene-sorted-with-themes.txt


# # Download CTD data

# wget "https://catalystresearch.io/product_downloads?token=&productCode=ctd&fileURL=%2Freports%2FCTD_chemicals.csv.gz&referrer=&sourceURL=http%3A%2F%2Fctd.mdibl.org%2Fdownloads%2F&redirect=http%3A%2F%2Fctd.mdibl.org%2Freports%2FCTD_chemicals.csv.gz" -O ${CTD_dir}/CTD_chemicals.csv.gz

# wget "https://catalystresearch.io/product_downloads?token=&productCode=ctd&fileURL=%2Freports%2FCTD_diseases.csv.gz&referrer=&sourceURL=http%3A%2F%2Fctd.mdibl.org%2Fdownloads%2F&redirect=http%3A%2F%2Fctd.mdibl.org%2Freports%2FCTD_diseases.csv.gz" -O ${CTD_dir}/CTD_diseases.csv.gz

# # Download pubtator data for mapping raw strings back to their IDs
# wget "ftp://ftp.ncbi.nlm.nih.gov/pub/lu/PubTator/chemical2pubtator.gz" -O ${pub_dir}/chemical2pubtator.gz

# wget "ftp://ftp.ncbi.nlm.nih.gov/pub/lu/PubTator/disease2pubtator.gz" -O ${pub_dir}/disease2pubtator.gz

# wget "ftp://ftp.ncbi.nlm.nih.gov/pub/lu/PubTator/gene2pubtator.gz" -O ${pub_dir}/gene2pubtator.gz

