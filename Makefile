# Change the configuration here.
# Include your useid/name as part of IMAGENAME to avoid conflicts
IMAGENAME = docker-test
COMMAND   = bash
DISKS     = -v /data/deep/data:/data:ro -v $(PWD):/project
USERID      = --user $(shell id -u):$(shell id -g)
USERNAME  = $(shell whoami)
# No need to change anything below this line

# Allows you to use sshfs to mount disks
SSHFSOPTIONS = --cap-add SYS_ADMIN --device /dev/fuse

.docker: Dockerfile requirements.txt
	docker build -t $(USERNAME)-$(IMAGENAME) .
	touch .docker

# Using -it for interactive use
RUNCMD=docker run --rm $(USERID) $(SSHFSOPTIONS) $(DISKS) -it $(USERNAME)-$(IMAGENAME)

# Replace 'bash' with the command you want to do
default: .docker
	$(RUNCMD) $(COMMAND)


