########################
Installation with Docker
########################

Why Use Docker?
===============

Docker is a platform that allows you to package, distribute, and run applications in containers. By using Docker, you can install Arches on any system that supports Docker. This helps insulate you from worries about how the operating system or other specifics of your host system impact dependencies and configurations. Some of the benefits of using Docker include:

1. Isolation:
    Docker allows developers to isolate applications from the underlying infrastructure,
    reducing the risk of conflicts and making it easier to manage dependencies.
2. Scalability:
    Docker makes it easy to scale applications up or down, as containers can be started
    and stopped quickly and easily.
3. Portability:
    Containers allow a developer to package up an application with all of the parts
    it needs, such as libraries and other dependencies, and ship it all out as one package. By doing so, the developer can be assured that the application will run on any other Linux machine regardless of any customized settings that machine might have that could differ from the machine used for writing and testing the code.

We recommend that you gain some understanding about how Docker works as well as some basic proficiency with using Docker before attempting to deploy Arches using Docker. These tutorials can introduce you to the basics of using Docker: https://docker-curriculum.com/ or https://www.howtogeek.com/733522/docker-for-beginners-everything-you-need-to-know/

This document will guide you through the process of using Docker to install Arches on your system. Even if you do not want to use Docker to deploy Arches, the review of Arches Docker setups can still provide a useful guide to see how various dependencies and configurations fit together.

.. IMPORTANT:: Arches currently lacks an "official" approach to installation using Docker. The examples that we discus here are drawn from various works-in-progress and community-created approaches. They should be helpful to get started with Docker and Arches, but they are not fully tested for production deployments.


Prerequisites
=============

Before you begin, ensure that your system meets the following requirements:

Docker:
    Docker must be installed on your system. You can download Docker from the official website: https://www.docker.com/get-started
Docker Compose:
    Docker Compose is a tool for defining and running multi-container Docker applications. It must also be installed on your system. You can download Docker Compose from the official website: https://docs.docker.com/compose/install/



Example Docker Code Repositories for Testing
============================================

The following lists Docker repositories that set up Docker containers running Arches configured for testing and development, not a production deployment.

1. Arches Dependencies
    This repo (https://github.com/archesproject/arches-dependency-containers) uses Docker to provision the dependency PostgreSQL, ElasticSearch, and RabbitMQ services required by Arches. NOTE: This repo does not install Arches itself, it just provides an alternate means to install dependency services.

2. Arches for Science
    This repo (https://github.com/archesproject/arches-for-science-prj) uses Docker to deploy an instance of Arches running the package and extensions for the *Arches for Science* project. This Docker deployment is designed to run in conjunction with the Docker containers and Docker network started by the *Arches Dependency* repo discussed above. The Arches for Science project aims to support workflows in the scientific conservation of objects (especially in museum collections), see: https://www.archesproject.org/arches-for-science/

3. Arches HER (Historic England)
    This repo (https://github.com/archesproject/arches-her) uses Docker to deploy an instance of Arches running the package and extensions for the Arches implementation developed for Historic England (https://www.archesproject.org/arches-for-hers/). This Docker deployment is designed to run in conjunction with the Docker containers and Docker network started by the *Arches Dependency* repo discussed above.

The *Arches for Science* Docker repository and the *Arches HER* Docker repository both launch instances of Arches that depend upon Docker containers and the Docker network started by the *Arches Dependencies* repository. These Docker repositories can be used to "spin up" different versions of Arches and Arches dependencies. You need to launch the appropriate set of dependencies started with *Arches Dependencies* with the version of Arches you are starting in *Arches for Science* or *Arches HER*. In order to switch between versions of Arches in *Arches for Science* and *Arches HER*, use git to checkout a branch with the desired version of Arches. For example, to run *Arches for Science* using Arches 7.4, use the dev/7.4.x branch in the repo: ``git checkout dev/7.4.x``


Example Docker Code Repositories for Production
===============================================

The following lists Docker repositories that set up Docker containers running Arches configured for production deployment. These repositories are not officially part of the Arches Project, and may not have received the same level of review and vetting as Arches Project repositories. While these are not yet fully vetted, they can be a useful starting point or guide to use Docker for production deployment of Arches:

1. arches-via-docker
    This repo (https://github.com/opencontext/arches-via-docker) uses Docker to provision containers running Arches (the most current stable version) and containers for the dependency PostgreSQL, ElasticSearch, and Redis services. It also starts an Nginx (as a proxy server) container as well as other containers to obtain and update SSL (for secure HTTPS) encryption certificates. You can use this repo directly or use it as a guide to see how to Arches can be configured for "production" deployments.