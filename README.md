Docker container that intakes post with the following form data and then "clicks" the link. Intentionally vulnerable. To be used with vulnerable by design web apps to realistically simulate XSS and XSRF (CSRF). Service runs flask to receive the post requests, and runs on the default port of 5000.  
   
      form data:  
      url: required. url encoded value which tells clicker-service which malicious link to "click".  
      cookie_name: optional. If cookie is required, sets the name of the cookie. If set, cookie_value must also be set.  
      cookie_value: optional. If cookie is required, sets the value of the cookie. If set, cookie_name must also be set.  

example request:  
  
      curl -X POST http://clicker:5000/clicker/ -d "url=http%3A%2F%2Fvulnwebapp.com%2Fvulnendpoint%3Fsearch%3Dxsspayload&cookie_name=user&cookie_value=admin"  

This is a stand alone container, though it should generally be deployed with a set of other containers. It is intended to be deployed with a web application and only be reachable on a backend network not exposed to the host networking. This service is intentionally vulnerable. A sample docker-compose.yaml is included to give an idea of intentional use.  
  
Install and run (from the directory with docker-compose.yaml in it):  

      docker-compose build
      docker-compose up
