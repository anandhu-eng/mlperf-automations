#!/bin/bash

if [[ ${MLC_SUDO_USER} == "yes" ]]; then
  echo "${MLC_SUDO} dmidecode -t memory > ${MLC_MEMINFO_FILE}"
  ${MLC_SUDO} dmidecode -t memory > ${MLC_MEMINFO_FILE}
  echo "dmidecode over"
fi
# test $? -eq 0 || return $?
# commented as it is not working properly inside docker
