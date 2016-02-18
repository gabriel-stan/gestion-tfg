# Makefile - use this file for all project-related actions

SCRIPTS = scripts

# install packages that require sudo privileges
install_system_packages:
	sudo $(SCRIPTS)/install_system_packages.sh
