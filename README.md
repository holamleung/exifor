# IMFO
#### Video Demo:  <URL HERE>
#### Description:

## IMFO is a web application that helps users extract Exif data stored in their image files.

The application is built using the Flask framework. Here is the project layout:
```
/imfo
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

<code>app.py</code> and <code>extract.py</code> are the two main Python codes that drive the program. <code>app.py</code> contains the configuration of the flask and routing. <code>extract.py</code> contains the functions to process the image files and extract the Exif data.

<code>config.cfg</code> has the configuration for the <code>secret_key</code> and maximum file size for the application. Before running the program, make sure to define a unique <code>secret_key</code> first. <code>requirements.txt</code> listed all the Python modules are used in the program.

<code>README.md</code> is a text file describing the project. 

Inside the <code>templates</code> folder, there are four HTML files. <code>index.html</code> is the homepage. <code>result.html</code> displays the Exif data after users submit their files. <code>error.html</code> is a custom error page to handle exceptions in the application. <code>layout.html</code> is a layout template.

The <code>static</code> folder contains the <code>style.css</code> for styling the webpage and the background image file. <code>clients_upload</code> temporarily stores the image files uploaded by users.

