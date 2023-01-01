<h1 align="center">AMP: is a fast admin dashboard template based on FastAPI</h1>
<h3 align="center"><img src='./src/static/img/logo.png'></h3>


<h1>Introduction</h1>
    AMP: is a fast admin dashboard template based on FastAPI. The project uses its own database sqlite, which allows you to start using immediately after installation. Peewee is used as an ORM. The templates use bootstrap and C3(D3-based reusable chart library). 

<h1>Screenshots</h1>
<h3 align="center">Desktop view</h3>
<img src='./src/static/img/desktop_view.jpg' width='100%'>
<h3 align="center">Mobile view</h3>
<h3 align="center"><img src='./src/static/img/mobile_view.jpg' width='25%'></h3>

<h1>Demo</h1>
<img src='./static/img/demo.gif' width='100%'>


<h1>Installation</h1>
<ol>
<li> Clone repo. </li>
<li> In workdir: <code> pip install -r requirements.txt </code></li>
<li> in console make folder 'src' current </li>
<li> in console run: <code>uvicorn main:app --reload</code> </li>
</ol>


&nbsp;&nbsp;The project also contains Docker files so you can build your image in container.

<h1>License</h1>
This project is licensed under the GPL-3.0 License.
