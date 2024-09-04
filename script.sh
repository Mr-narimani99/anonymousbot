exit_status=1;
while [ $exit_status -eq 1 ]; do

    nc -zv mysql 3306 && exit_status=$? || exit_status=$?;
    echo "MySQL is not available yet. Waiting..."
    sleep 5
done

echo "MySQL is available "
python mybot.py

