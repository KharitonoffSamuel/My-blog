+++
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
topics: ["Homelab"]
tags: ["network", "kubernetes"]
categories = ["IT", "Home lab"]
cover:
  image: "cover.png"
  alt: "{{ replace .Name "-" " " | title }}"
  caption: ""
  relative: true  
+++