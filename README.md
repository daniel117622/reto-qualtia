
Diagrama general del sistema. Este describe los contenedores asi como una breve descripción de lo que consume o recibe
cada uno de los contenedores.

![image](https://github.com/user-attachments/assets/c32dd332-d3c3-4aba-a773-c4ecd0da141d)

El archivo docker-compose necesita de un healthcheck para determinar el momento en que el worker puede establecer una conexión con selenium. Las depedencias se manejan de manera individual por contenedor, las cuales vienen indicadas en su respectivo Dockerfile.

El sistema se levanta con el siguiente comando. 
>docker compose -f docker_compose.yaml up -d --build

Hay un archivo de jupyter notebooks. Este fue usado para documentar el desarrollo de la lógica para extraer los datos solicitados del archivo JSON. Se hacen algunas observaciones sobre como localizar los datos eficientemente.

La API documenta los endpoints a travez de la función index con los principios HATEOAS. Con ayuda de IA, implemente un sistema de reflexión y decoradores personalizados para lograr esta funcionalidad. 

Uno de los retos para esta asignación fue que era muy complicado extraer los productos por API porque parte de las peticiones que hacia el e-commerce se encontraban ofuscadas. Por esto se decidio utilizar selenium para renderizar la pagina , hacer un scroll, y finalmente solicitar un snapshot del DOM el cual se parsea con BeautifulSoup y los datos se envian a REDIS junto a su timestamp. Se utilizo IA para partes puntuales del código por cuestión de tiempo, pero los servicios utilizados y comunicación entre ellos fueron diseñados por mi.

En el correo se envio la IP de la API que esta hosteada en GCP.
