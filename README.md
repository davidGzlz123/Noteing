# 📋 Noteing

## 📌 Descripción

Proyecto personal realizado para tener una **aplicación de gestión de notas personalizadas**.

Se trata de una página web que perimite el almacenamiento de notas con diversos elementos, desde checkboxes hasta imagenes comprimidas por la propia aplicación web.

## 💾 Tecnologías utilizadas
- Python
- JavaScript
- React
- Django
- SQLite

## ⚙️ Detalles técnicos

Actualmente, el proyecto está configurado para ejecutarse únicamente en una **red local**, utilizando como servidor el equipo que lo corre.
Para su funcionamiento, es necesario inicializar tanto el backend como el frontend. Para facilitar este proceso, se incluye un **script .bash** ubicado en la raíz del proyecto.

El proyecto también cuenta con un archivo **.env** donde se define el puerto de red utilizado. Este puerto depende de la dirección IP del equipo.
Si se desea acceder desde una aplicación móvil, se debe utilizar el puerto **3000**, que corresponde al servidor de desarrollo de React, lo cual permite visualizar correctamente el frontend desde el dispositivo móvil.