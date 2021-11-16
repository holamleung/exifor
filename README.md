# Exifor

Exifor is a web application that helps users extract and understand the Exif data stored in their image files.

## Purpose

Exif (Exchangeable Image File Format) is a standard that specifies the formats for storing data in images. It records information such as the model of the camera, capture setting, location, timestamp, and copyright information. These metadata are designed for technical use by default, which is quite challenging to understand. Thus, a proper interpretation is needed to make them more digestible for most users. That is what Exifor is for.

## Getting Start

At the homepage, simply upload your image and then click the "Examine" button. Voilà! The site will return a list of metadata to you.

![Screenshot (10)](https://user-images.githubusercontent.com/75563658/139430533-4314ee39-4afa-4f19-bba9-56ac9a30f865.png)



![Screenshot (12)](https://user-images.githubusercontent.com/75563658/139430621-710711ee-6ef6-4850-9168-9d6c19661809.png)

## Description

The application is built using the Flask framework. Here is the project layout:
```
/exifor
|-app.py
|-extract.py
|-README.md
|-templates
| |-result.html
| |-layout.html
| |-index.html
| |-error.html
|-config.cfg
|-static
| |-style.css
| |-clients_upload
| |-background-1920x1275.jpg
|-requirements.txt
```

<code>app.py</code> and <code>extract.py</code> are the two main Python codes that drive the program. <code>app.py</code> is mainly for the configuration of the flask and routing. <code>extract.py</code> focuses on processing the image files and the Exif data. Exif data are extracted using the Pillow library.

<code>config.cfg</code> has the configuration for the <code>secret_key</code> and maximum file size for the application. <b>Make sure to define a unique <code>secret_key</code> before running the program.</b> <code>requirements.txt</code> listed all the Python modules are used in the program.

<code>README.md</code> is a text file describing the project. 

Inside the <code>templates</code> folder, there are four HTML files. <code>index.html</code> is the homepage. <code>result.html</code> displays the Exif data after users submit their files. <code>error.html</code> is a custom error page to handle exceptions in the application. <code>layout.html</code> is a layout template.

The <code>static</code> folder contains the <code>style.css</code> for styling the webpage and the background image file. <code>clients_upload</code> temporarily stores the image files uploaded by users.

