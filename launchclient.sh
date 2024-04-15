#!/usr/bin/expect -f

spawn bash
send "cd jetson-inference/\r"
expect "$ "
send "$ "
expect "Password:"
send "hvl\r"
expect "$ "
interact