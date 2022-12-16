from django.db.utils import IntegrityError
from django.test import Client, TestCase
from accounts.models import User
from .models import AreaComun
# Create your tests here.

class AreaComunTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='testing', email='testing@gmail.com', password='Control123!')
        login = self.client.login(username='testing', password='Control123!')

    def test_crear_area_comun(self):
        nombre='Salon de Eventos - Gardenias'
        descripcion='Ubicado en el patio trasero'
        mobiliario='Sillas, mesas, manteles'
        costo=1200
        nueva_area_comun = AreaComun.objects.create(nombre=nombre, descripcion=descripcion, mobiliario=mobiliario, costo=costo)
        area_comun_creada = AreaComun.objects.get(id=nueva_area_comun.id)
        self.assertEquals(area_comun_creada.nombre, nombre)
        self.assertEquals(area_comun_creada.descripcion, descripcion)
        self.assertEquals(area_comun_creada.mobiliario, mobiliario)
        self.assertEquals(area_comun_creada.costo, costo)

    def test_crear_area_comun_sin_costo(self):
        nombre='Parque Infantil'
        descripcion='Ubicado en el patio trasero'
        mobiliario='Sifon de agua, colchonetas'
        nueva_area_comun = AreaComun.objects.create(nombre=nombre, descripcion=descripcion, mobiliario=mobiliario)
        area_comun_creada = AreaComun.objects.get(id=nueva_area_comun.id)
        self.assertTrue(area_comun_creada.costo == 0)

    def test_crear_area_comun_sin_mobiliario(self):
        nombre='Parque Infantil'
        descripcion='Ubicado en el patio trasero'
        nueva_area_comun = AreaComun.objects.create(nombre=nombre, descripcion=descripcion)
        area_comun_creada = AreaComun.objects.get(id=nueva_area_comun.id)
        self.assertTrue(area_comun_creada.mobiliario == 'Ninguno')

    #Test de manejo de errores

    def test_crear_area_comun_costo_negativo(self):
        nombre='Parque Infantil'
        descripcion='Ubicado en el patio trasero'
        mobiliario='Sifon de agua, colchonetas'
        costo=-1
        with self.assertRaises(IntegrityError):
            AreaComun.objects.create(nombre=nombre, descripcion=descripcion, mobiliario=mobiliario, costo=costo)

    def test_crear_area_comun_costo_negativo(self):
        nombre='Parque Infantil'
        descripcion='Ubicado en el patio trasero'
        mobiliario='Sifon de agua, colchonetas'
        costo=-1
        with self.assertRaises(IntegrityError):
            AreaComun.objects.create(nombre=nombre, descripcion=descripcion, mobiliario=mobiliario, costo=costo)
    

    def test_area_comun_registrar_respuesta(self):
        response = self.client.get("/area_comun/registrar/")
        print(response)
        self.assertEqual(response.status_code, 200)
    