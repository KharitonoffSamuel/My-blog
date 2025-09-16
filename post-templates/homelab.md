---
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
date: {{ .Date }}
draft: true
topics: ["Homelab"]
tags: ["talos.linux", "K8S", "K9S", "K3S", "talosctl", "proxmox", "hardware", "homelab", "network"]
projects: ["HomeLab gitDevSecOps"]
categories: ["IT", "Homelab"]
weight: 0 # Lower number = toper in the list
cover:
  image: "homelab-cover.svg"
  alt: '{{ replace .Name "-" " " | title }}'
  caption: ""
  relative: true  
  hidden: true             # si true → pas de cover sur la page du post
  hiddenInList: true       # si true → pas de cover dans la liste des posts
  hiddenInSingle: false    # si true → pas de cover sur la page individuelle
---