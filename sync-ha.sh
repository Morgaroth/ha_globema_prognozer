

rsync -avz -e "ssh -p2222  -i $HOME/.ssh/id_rsa_prv" --exclude venv --exclude .idea --exclude .github --exclude images --exclude sync-ha.sh --exclude .git $HOME/projects/ha_globema_prognozer/custom_components/pv_forecast_globema root@192.168.0.20:/root/config/custom_components