OPTIONS=$1  # "-u username,password ip:port"

remote_dir="data/snap"
local_dir="/home/ftpftp/data/upload/snap"

lftp $OPTIONS -e "mirror -c -R ${local_dir} ${remote_dir} --only-newer --Remove-source-files ; exit"

datestr=`date +%Y%m%d_%H%M%S`
echo $datestr >> /tmp/upload.log
