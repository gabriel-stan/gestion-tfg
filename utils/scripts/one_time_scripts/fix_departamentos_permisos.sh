#!/bin/bash

sudo -u postgres psql -U postgres -d gestfg -c "DELETE FROM auth_group_permissions;"
sudo -u postgres psql -U postgres -d gestfg -c "DELETE FROM auth_permission WHERE codename='tfg.create' OR codename='evento.create';"
