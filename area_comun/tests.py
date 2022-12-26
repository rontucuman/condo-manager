from django.db.utils import IntegrityError
from django.test import Client, TestCase
from accounts.models import User
from .models import AreaComun, ReservaAreaComun
from datetime import datetime
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
    
class ReservaAreaComunTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='testing', email='testing@gmail.com', password='Control123!')
        login = self.client.login(username='testing', password='Control123!')
        self.piscina_gratis = AreaComun.objects.create(nombre='Piscina', descripcion='Piscina de 2 metros de altura y 25 metros de largo', mobiliario='10 mesas con sus sillas', costo=0)
        self.salon_eventos_pago= AreaComun.objects.create(nombre='Salon de eventos', descripcion='Salon de eventos principal ubicado en el centro del condominio', mobiliario='10 mesas, refrigerador, frigorifico, aire acondicionado, television por cable, parlante con microfono', costo=300)

    def test_crear_reserva_gratis(self):
        nueva_reserva = ReservaAreaComun.objects.create(area_comun=self.piscina_gratis, propietario=self.usuario, fecha=datetime.now().date())
        reserva_creada = ReservaAreaComun.objects.get(id=nueva_reserva.id)
        self.assertEquals(reserva_creada.area_comun, self.piscina_gratis)
        self.assertEquals(reserva_creada.propietario, self.usuario)
        self.assertEquals(reserva_creada.fecha, datetime.now().date())
        self.assertEquals(reserva_creada.confirmada, False)

    def test_lista_area_comun_registrar_respuesta(self):
        response = self.client.get("/area_comun/lista/")
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_mis_reservas_registrar_respuesta(self):
        response = self.client.get("/area_comun/misReservas/")
        print(response)
        self.assertEqual(response.status_code, 200)