# agendaContactos-backed-p2025
Repositorio de una Agenda de contactos personales con Django.

# Ejecutar para Python actualizado
C:\ProgramData\anaconda3\Scripts\activate 

# Para descargar los requirements
pip install -r requirements.txt


# activar el VENV
venv\Scripts\activate

# migraciones


# .env con 

user=postgres.fqkokqbyetrtloykhskw 
password=[YOUR_PASSWORD] 
host=aws-1-us-east-1.pooler.supabase.com
port=6543
dbname=postgres

# Crear super user
python manage.py createsuperuser

# migraciones

python manage.py makemigrations
python manage.py migrate


