op=$1

options="-u ftpftp,ftp111 192.168.11.1:2121"

remote_dir="/discsda/tt/data"
local_dir="/home/pi/src"

if [ $op = "1" ]
then
    echo "download newer files..."
    lftp $options -e "mirror -c ${remote_dir} ${local_dir}/data --only-newer; exit"
elif [ $op = "2" ]
then
    dirname=`date +%Y%m%d_%H%M%S`
    echo "save and delete older files to $dirname ..."
    lftp $options -e "mirror -c  ${remote_dir} ${local_dir}/data_old/${dirname} --older-than=now-1hour --Remove-source-files; exit"
fi
