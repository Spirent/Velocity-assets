#!/bin/sh


echo "[INFO] Script with infinite loop"

while :
do
	# echo "[INFO] Sleep 1 second"
	sleep 1
done

echo "[ERROR] This message should never be seen."
