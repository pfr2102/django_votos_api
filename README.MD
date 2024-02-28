# API-REST votos comite de etica

## Clonar el Repositorio

Para comenzar a trabajar en este proyecto en tu máquina local, sigue estos pasos:

1. Abre tu terminal.

2. Crea un entorno virtual dentro de la misma carpeta donde clones este proyecto.

    ```bash
   python -m venv envs/Nombre_del_entorno
   .\envs\Nombre_del_entorno\Scripts\Activate
   pip install django

2. Utiliza el siguiente comando para clonar el repositorio en tu máquina:

   ```bash
   git clone https://github.com/pfr2102/django_votos_api.git

## Instala dependencias del proyecto dentro del entorno virtual

    pip install -r requirements.txt


## Push y Pull desde tu repositorio local

    --git push <-- con esto mandas al repo remoto todas las modificaciones de tu repo local, asi que cada vez que lo uses tienes que estar seguro de que tu proyecto este en una version estable y sin fallas o en  todo caso hacer una rama para hacer calis y hacer todos los push que quieras sin afectar la rama main que tiene la version estable.

    --git pull <-- con esto actualizas los cambios que haya recibido el repo remoto en git-hub (solo de la rama main)