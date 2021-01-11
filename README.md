<h1 align="center">
  <br>
  <a href="https://github.com/IcelyFramework/icely-annotator"><img src="document/icicle.png" alt="Icely Annotator" width="200"></a>
  <br>
  Icely Annotator
  <br>
</h1>

<h4 align="center">An Annotation Tool for annotating software requirements and generate static ontology.</h4>

<p align="center">
  <img alt="Docker Image Version (latest semver)" src="https://img.shields.io/docker/v/icely/icely-annotator">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/IcelyFramework/icely-annotator">
  <img alt="GitHub" src="https://img.shields.io/github/license/IcelyFramework/icely-annotator">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/IcelyFramework/icely-annotator?style=social">
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

![screenshot](document/demo.gif)

## About
Icely Annotator is a tool for annotating software requirements, and generate static ontology of Icely Framework.

This tool is largely based on the [brat annotation tool](http://brat.nlplab.org/) and [S-Case Requirements Annotation tool](https://github.com/s-case/requirements-annotation-tool)

## ✨ Key Features
* Annotate Textual Requirement
* Export Annotation to Static Ontoloty (.owl)
* Virtualize Textual Requirement
* Auto-Annotate (In Progress)

## 🚀 How To Use

### Using Docker (Recommended)
If you’d rather run the Icely Annotator from a Docker image, it is available on Docker Hub at [icely/icely-annotator](https://hub.docker.com/r/icely/icely-annotator).

### Building from source
To clone and run this application, you'll need [Git](https://git-scm.com) and [Python 3](https://www.python.org/downloads/) (which comes with [pip](http://npmjs.com)) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone git@github.com:IcelyFramework/icely-annotator.git

# Go into the repository
$ cd icely-annotator

# Install dependencies
$ pip install -r requirements.txt

# Create Directory and Copy Static Ontoloty
$ mkdir -p /app/icely-annotator/original_ontology/ && cp original_ontology/requirements.owl /app/icely-annotator/original_ontology/requirements.owl
# Run the app
$ python standalone.py
```

Note: for run server via apache see [brat documentation](https://brat.nlplab.org/installation.html)

## ☑ Roadmap
If you want to see a new feature feel free to create a new Issue. Here are some features which are either under way or planned:

- [ ] [Auto-Annotation](https://github.com/IcelyFramework/icely-annotator/issues/1)

If you'd like to give any of these a shot feel free to contribute.

## Support

<a href="https://www.buymeacoffee.com/amirdeljouyi" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## License

Copyright © 2019 [Amir Deljouyi](https://github.com/amirdeljouyi).  
Icely Annotator is made available under the [MIT](https://github.com/IcelyFramework/icely-annotator/blob/main/LICENSE) licensed.

## 🤝 Contributing
Contributions, issues and feature requests are welcome.  
Feel free to check [issues page](https://github.com/IcelyFramework/icely-annotator/issues) if you want to contribute.

---

> [amirdeljouyi](http://ce.sharif.edu/~deljouyi) &nbsp;&middot;&nbsp;
> GitHub [@amirdeljouyi](https://github.com/amirdeljouyi) &nbsp;&middot;&nbsp;
> Twitter [@amirdeljouyi](https://twitter.com/amirdeljouyi)
