#!/usr/bin/expect -f

spawn bash
send "cd jetson-inference\r"
expect "$ "
send "./docker/run.sh\r"
expect "$"
send "hvl\r"
expect "$ "
interact