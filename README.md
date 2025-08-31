# My temporary blog use Hugo and GitHub
I have multiples projects build in my own, but I never expose to other. So, I allway want to 
have my own server with my own domaine name, but for personal resons I can't have persistant server.
I found a solution to host blog in minutes with hugo and GitHub, so was I.

## Blog access
[My blog](https://kharitonoffsamuel.github.io/My-blog)

## Topics
I am a tech guy, work in **developpement** first, with **management**, **process optimisation** and **project management**.

## Create new post
With the default archetypes file :
```bash
hugo new posts/<NAME_OF_YOUR_POST>/index.md
```
With specifique template file :
```bash
hugo --kind <NAME_OF_YOUR_TEMPLATE> posts/<NAME_OF_YOUR_POST>/index.md
```

## Generate localy
If you want to test, or writ and see the result in live, you can use this command :
```bash
hugo server -D
```
The server is set at the port `1313`.