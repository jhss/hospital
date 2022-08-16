sudo /etc/init.d/ssh start
source ~/.profile &&
start-dfs.sh
start-yarn.sh
airflow scheduler
