# Importamos los modelos a utilizar (al crear un objeto de la clase User se creará el mismo objeto en la clase Profile)
from django.contrib.auth.models import User
from red_social.models import Profile
# Importamos el metodo post_save desde signals que se encuentra dentro de models, db, django
from django.db.models.signals import post_save
# Importamos el metodo receiver desde dispatch que se encuentra en dispatch
from django.dispatch import receiver

#Definimos la funcion create_profile y la decoramos con la funcion receiver con los parametros post_save y la clase desde donde se creará
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Si el objeto está creado entonces crearemos el mismo objeto en la clase Profile utilizando la instancia user
    if created:
        Profile.objects.create(user=instance)

# Primer metodo de crear perfil automaticamente al crear usuario.
#post_save.connect(create_profile, sender=User)
