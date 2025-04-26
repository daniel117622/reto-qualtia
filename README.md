
Diagrama del sistema.
![image](https://github.com/user-attachments/assets/c32dd332-d3c3-4aba-a773-c4ecd0da141d)
El sistema se levanta con el siguiente comando. El archivo docker-compose necesita de un healthcheck para determinar el momento en que el worker
puede establecer una conexión con selenium.
>docker compose -f docker_compose.yaml up -d --build

Hay un archivo de jupyter notebooks. Este fue usado para documentar el proceso para crear el csv con la data solicitada.
Este proceso lo agregue dentro de la API para que esta ejecute la prueba 1.

La API documenta los endpoints atravez de la función index con los principios HATEOAS.
