#!/bin/sh

currentDir=$(
  cd $(dirname "$0")
  pwd
)
resource="/resources"
profilepath=$currentDir$resource
google-chrome --remote-debugging-port=9223 --user-data-dir=$profilepath &>/dev/null &
