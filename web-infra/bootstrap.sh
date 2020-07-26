#!/usr/bin/env bash

# Setup User and group
/usr/sbin/groupadd deployers
echo "%deployers ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
chmod 440 /etc/sudoers

/usr/sbin/useradd -s /bin/bash -m -g deployers imon
/usr/sbin/usermod -a -G deployers imon
mkdir -vp /home/imon/.ssh
cp /root/.ssh/authorized_keys /home/imon/.ssh/authorized_keys
chown -R imon /home/imon/.ssh
chgrp -R deployers /home/imon/.ssh