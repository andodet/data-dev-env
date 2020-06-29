while ping -c1 mysql_seeding &>/dev/null 
do 
    sleep 1 
done;
echo "Finished seeding" && pytest ./tests.py