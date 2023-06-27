# For spt3g01
# DATAPATH=/data/skyviewer

# For coigue-ofc
DATAPATH=${HOME}/skyviewer-dev/skv-home

# One call per band
java -Xmx16g -jar AladinBeta.jar -hipsgen in=$DATAPATH/archive/spt3g/090GHz out=$DATAPATH/hips/SPT_winter2020_090GHz_HiPS id="NCSA/P/SPT/WINTER2020-090GHZ" -creator="Felipe Menanteau (NCSA)" -title="SPT3G-Winter2020-090GHz" -blank=-99 -order=7 -clean
java -Xmx16g -jar AladinBeta.jar -hipsgen in=$DATAPATH/archive/spt3g/150GHz out=$DATAPATH/hips/SPT_winter2020_150GHz_HiPS id="NCSA/P/SPT/WINTER2020-150GHZ" -creator="Felipe Menanteau (NCSA)" -title="SPT3G-Winter2020-150GHz" -blank=-99 -order=7 -clean
java -Xmx16g -jar AladinBeta.jar -hipsgen in=$DATAPATH/archive/spt3g/220GHz out=$DATAPATH/hips/SPT_winter2020_220GHz_HiPS id="NCSA/P/SPT/WINTER2020-220GHZ" -creator="Felipe Menanteau (NCSA)" -title="SPT3G-Winter2020-220GHz" -blank=-99 -order=7 -clean
