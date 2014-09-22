Readme
======================

Run
---------

sudo -s
supervisorctl stop haproxy
ctrl-C

haproxy -f /home/andrey/Documents/Projects/science-social/scienc/configs/haproxy.conf

su postgres -c '/opt/local/lib/postgresql93/bin/postgres -D /opt/db/postgresql93/defaultdb'

Stop
----------

postgres:
ctrl-C
killall postgres
kill | pgrep -f postgres

haproxy:
ctrl-C

supervisorctl start haproxy