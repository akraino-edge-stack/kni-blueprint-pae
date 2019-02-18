﻿## KNI Provider Access Edge (PA) Blueprint
This blueprint is part of the KNI-Edge Family. Please look [here](https://wiki.akraino.org/display/AK/Kubernetes-Native+Infrastructure+for+Edge+%28KNI-Edge%29+Family) for details

**Blueprint architecture**
![enter image description here](https://wiki.akraino.org/download/attachments/6128842/PAE_Blueprint.png?version=1&modificationDate=1544049994000&api=v2)

**About this repository**
This repository will contain basic templates for deploying an OpenShift cluster specially focused on Provider Access Edge. All settings for deployment and update will be handled on code repositories, following GitOps strategy, that is, using git as a single source of truth for declarative infrastructure and applications.
Initially templates for libvirt and AWS will be offered, being on its own folder, that will contain all the configuration files and instructions needed for deployment.
