web: python boris/manage.py collectstatic --noinput; newrelic-admin run-program python boris/manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3 
