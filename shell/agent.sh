cd /Programs/Python/RL_Curling_Python
now=`date +"%Y%m%d%I%M"`
python3 -m run.agent0 --dir_name $now & python3 -m run.agent1 --dir_name $now