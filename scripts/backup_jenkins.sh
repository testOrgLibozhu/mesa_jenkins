cd /home/majanes/src/mesa_jenkins && rsync -r --exclude *diagnostics* --exclude secret* --exclude plugins --exclude updates --exclude user* --exclude nextBuildNumber --exclude *log*  --exclude builds --exclude workspace* --exclude *.bak --exclude .owner --include *.xml /mnt/space/jenkins/ jenkins/
