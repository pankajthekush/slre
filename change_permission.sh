#!/bin/bash
currentDir=$(
  cd $(dirname "$0")
  pwd
)
driver="/driver/chromedriver"
chmod +x $currentDir$driver
