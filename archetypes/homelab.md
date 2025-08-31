---
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
date: {{ .Date }}
draft: true
topics: ["Homelab"]
tags: ["talos.linux", "K8S", "K9S", "K3S", "talosctl", "proxmox", "hardware", "homelab", "network"]
categories: ["IT", "Home lab"]
weight: 0 # Lower number = toper in the list
cover:
  image: "cover.png"
  alt: '{{ replace .Name "-" " " | title }}'
  caption: ""
  relative: true  
---