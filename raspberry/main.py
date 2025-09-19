import RPi.GPIO as GPIO
import time
from PIL import Image
import paho.mqtt.client as mqtt
import customtkinter as ctk
from threading import Thread
from dotenv import load_dotenv
from pathlib import Path
import json, os

# Configuración de espacios
espacios = {'casillero_1': {'number': 1, 'sensor': 4, 'lock': 17},
            'casillero_2': {'number': 2, 'sensor': 5, 'lock': 27}}

# Configuración GPIO
SENSOR_PIN = [4, 5]  # Pin GPIO del sensor (BCM numbering)
LED_PINS = [17, 27]  # Pines GPIO para las cerraduras
TIEMPO_MUESTREO = 0.5  # Intervalo de lectura en segundos

# Carga las variables del archivo .env
dotenv_path = Path('config/.env')
load_dotenv(dotenv_path=dotenv_path)

# Información del Locker
SLOCKER=[os.getenv("NOMBRE"), os.getenv("ZONA"), os.getenv("CIUDAD"), os.getenv("ESTADO")]

# Configuración MQTT
BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USUARIO")
PASSWORD = os.getenv("PASSWORD")

TOPIC_SENSOR = "casillero/respuestas"
TOPIC_PANTALLA = "casillero/pantalla"
TOPIC_COMANDOS = "casillero/comando"
TOPIC_CHEQUEO = "casillero/check"

# Configuración inicial GPIO
GPIO.setmode(GPIO.BCM)

for pin in SENSOR_PIN:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configura como entrada con resistencia pull-up

for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Clase para el monitoreo del sensor
class SensorMonitor:

    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect_sensor
        self.client.tls_set()
        self.client.username_pw_set(USER, PASSWORD)
        self.running = True
        self.estado_anterior = {}  # Diccionario por pin

        # Inicializar estados
        for pin in SENSOR_PIN:
            self.estado_anterior[pin] = GPIO.input(pin)

    def on_connect_sensor(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("\033[30;47mLOCK\033[0m:    Sensores conectados al servidor MQTT.")
        else:
            print(f"\033[37;41mERROR\033[0m:   Error al conectar los sensores MQTT: {rc}")

    def start(self):
        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()

            while self.running:
                for pin in SENSOR_PIN:
                    estado_actual = GPIO.input(pin)
                    if estado_actual != self.estado_anterior[pin]:
                        if estado_actual == GPIO.HIGH:
                            mensajeEstado = 'ABIERTO'
                        else:
                            mensajeEstado = 'CERRADO'
                        for casillero, datos in espacios.items():
                            if datos['sensor'] == pin:
                                mensaje = {"casillero": datos['number'], "estado": mensajeEstado, "locker": SLOCKER}
                                self.client.publish(TOPIC_SENSOR, json.dumps(mensaje), qos=1)
                        self.estado_anterior[pin] = estado_actual
                time.sleep(TIEMPO_MUESTREO)

        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"\033[37;41mERROR\033[0m:   Error en el monitoreo de los sensores: {e}")
            self.stop()

    def stop(self):
        self.running = False
        self.client.loop_stop()

# Clase para la aplicación de la interfaz
class CalculatorApp:

    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Interfaz RPi")
        # self.app.attributes("-fullscreen", True)
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        self.app.geometry(f"{screen_width}x{screen_height}+0+0")
        self.app.resizable(True, True)

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect_ui
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.tls_set()
        self.client.username_pw_set(USER, PASSWORD)

        # Variables de la interfaz
        self.current_input = ""
        self.max_digits = 10
        self.exit_code = "123456789"

        # Configuración de la interfaz
        self.setup_ui()
    
    def setup_frames(self):
        self.frames["bienvenida"] = self.create_welcome_frame()
        self.frames["qr"] = self.create_qr_frame()
        self.frames["teclado"] = self.create_keyboard_frame()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(expand=True, fill="both")

    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        self.frames = {}
        self.setup_frames()
        self.show_frame("bienvenida")

    def create_welcome_frame(self):
            frame = ctk.CTkFrame(self.app)
            label = ctk.CTkLabel(frame, text="Bienvenidos a Smartlock", font=("Arial", 42))
            label.pack(pady=(200, 20))

            btn1 = ctk.CTkButton(frame, 
                                text="Solicitar Casillero", 
                                command=lambda: self.show_frame("qr"),
                                height=80,
                                width=200,
                                font=("Arial",24),
                                fg_color="#3aa9f6",
                                corner_radius=20)
            btn1.pack(pady=10)
            
            btn2 = ctk.CTkButton(frame, 
                                text="Abrir Casillero", 
                                command=lambda: self.show_frame("teclado"),
                                height=80,
                                width=210,
                                font=("Arial",24),
                                fg_color="#983af6",
                                corner_radius=20)
            btn2.pack(pady=10)
            return frame

    def create_qr_frame(self):
        frame = ctk.CTkFrame(self.app)
        label = ctk.CTkLabel(frame, text="Escanea el cÃ³digo QR", font=("Arial", 42))
        label.pack(pady=(150, 20))

        # Ruta de imagen QR
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        qr_path = os.path.join(BASE_DIR, "qr.jpg")
        if os.path.exists(qr_path):
            image = Image.open(qr_path)
            qr_ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(350, 350))
            qr_label = ctk.CTkLabel(frame, image=qr_ctk_image, text="")  # text="" para no mostrar texto por defecto
            qr_label.pack(pady=10)
        else:
            qr_label = ctk.CTkLabel(frame, text="Imagen QR no encontrada", font=("Arial", 18))
            qr_label.pack(pady=10)

        back_btn = ctk.CTkButton(frame, 
                                 text="Volver", 
                                 command=lambda: self.show_frame("bienvenida"),
                                 height=80,
                                 width=210,
                                 font=("Arial",24),
                                 fg_color="#f76666",
                                 corner_radius=20)
        back_btn.pack(pady=20)
        return frame

    def create_keyboard_frame(self):
        frame = ctk.CTkFrame(self.app)
        layout = ctk.CTkFrame(frame)
        layout.pack(expand=True, fill="both", padx=20, pady=20)

        # IZQUIERDA: Teclado
        left = ctk.CTkFrame(layout)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.display = ctk.CTkLabel(left, text="0", font=("Arial", 48))
        self.display.pack(pady=80)

        self.button_frame = ctk.CTkFrame(left)
        self.button_frame.pack()

        self.create_number_buttons()
        self.create_special_buttons()

        # DERECHA: Instrucciones o imágenes
        right = ctk.CTkFrame(layout)
        right.pack(side="right", fill="both", expand=True)

        self.notificacion_label = ctk.CTkLabel(right, text="", font=("Arial", 40), text_color="green")
        self.notificacion_label.pack(pady=(70, 0))

        instruccion = ctk.CTkLabel(right, text="INSTRUCCIONES", font=("Arial", 20))
        instruccion.pack(pady=(80, 20))

        instruccion = ctk.CTkLabel(right, text="- El cÃ³digo para abrir el casillero estÃ¡ en la", font=("Arial", 20))
        instruccion.pack()
        instruccion = ctk.CTkLabel(right, text="pantalla principal del sitio web.", font=("Arial", 20))
        instruccion.pack()

        instruccion = ctk.CTkLabel(right, text="- Si no tienes acceso a internet:", font=("Arial", 20))
        instruccion.pack(pady=(20, 0))
        instruccion = ctk.CTkLabel(right, text="Revisa tu correo electrÃ³nico.", font=("Arial", 20))
        instruccion.pack()
        instruccion = ctk.CTkLabel(right, text="Ã“", font=("Arial", 20))
        instruccion.pack(pady=20)
        instruccion = ctk.CTkLabel(right, text="Si agregaste tu nÃºmero de telÃ©fono,", font=("Arial", 20))
        instruccion.pack()
        instruccion = ctk.CTkLabel(right, text="tambiÃ©n se enviÃ³ por WhatsApp.", font=("Arial", 20))
        instruccion.pack()

        back_btn = ctk.CTkButton(right, 
                                 text="Volver", 
                                 command=lambda: self.show_frame("bienvenida"),
                                 height=80,
                                 width=200,
                                 font=("Arial",24),
                                 fg_color="#3aa9f6",
                                 corner_radius=20)
        back_btn.pack(pady=20)
        return frame

    def create_number_buttons(self):
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            btn = ctk.CTkButton(
                self.button_frame, text=str(i), width=80, height=80,
                font=("Arial", 24), command=lambda n=i: self.add_number(n)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)

        btn_0 = ctk.CTkButton(
            self.button_frame, text="0", width=80, height=80,
            font=("Arial", 24), command=lambda: self.add_number(0)
        )
        btn_0.grid(row=3, column=1, padx=5, pady=5)

    def create_special_buttons(self):
        borrar = ctk.CTkButton(
            self.button_frame, text="X", width=80, height=80,
            font=("Arial", 24), fg_color="orange", command=self.delete_last_char
        )
        borrar.grid(row=3, column=0, padx=5, pady=5)

        confirmar = ctk.CTkButton(
            self.button_frame, text=">", width=80, height=80,
            font=("Arial", 24), fg_color="green", command=self.confirm_input
        )
        confirmar.grid(row=3, column=2, padx=5, pady=5)

        borrar_todo = ctk.CTkButton(
            self.button_frame, text="BORRAR TODO", width=260, height=60,
            font=("Arial", 20), fg_color="red", hover_color="#f76666",
            command=self.clear_input
        )
        borrar_todo.grid(row=4, column=0, columnspan=3, pady=(10, 0))

    def on_connect_ui(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("\033[37;45m  UI\033[0m:    Interfaz interactiva conectada al servidor MQTT.")
            client.subscribe([(TOPIC_PANTALLA, 0), (TOPIC_COMANDOS, 0), (TOPIC_CHEQUEO, 0)])
        else:
            print(f"\033[37;41mERROR\033[0m:   Error de conexiÃ³n en la interfaz interactiva: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            if msg.topic == TOPIC_COMANDOS:
                print("\033[37;46mMQTT\033[0m:    Respuesta del servidor MQTT.")
                if data[1:] == SLOCKER:
                    for casillero, datos in espacios.items():
                        if datos['number'] == int(data[0]):
                            self.mostrar_notificacion("Â¡Casillero abierto!")
                            GPIO.output(datos['lock'], GPIO.HIGH)
                            time.sleep(TIEMPO_MUESTREO)
                            GPIO.output(datos['lock'], GPIO.LOW)
            elif msg.topic == TOPIC_CHEQUEO:
                if data[0] == 'CHECAR':
                    if data[2:] == SLOCKER:
                        for casillero, datos in espacios.items():
                            if datos['number'] == int(data[1]):
                                if GPIO.input(datos['sensor']) == GPIO.HIGH:
                                    mensajeEstado = 'ABIERTO'
                                else:
                                    mensajeEstado = 'CERRADO'
                                mensaje = ['RESPUESTA', mensajeEstado, datos['number']] + SLOCKER
                                self.client.publish(TOPIC_CHEQUEO, json.dumps(mensaje), qos=1)

                # Mostrar notificaciÃ³n en pantalla

                # self.mostrar_notificacion("Â¡Comando recibido!")
        except Exception as e:
            print(f"\033[37;41mERROR\033[0m:   Error al procesar el comando de la interfaz interactiva: {e}")

    def on_disconnect(self, client, userdata, rc):
        print(f"\033[37;45m  UI\033[0m:    Interfaz interactiva desconectada del broker (RC: {rc})")
        if rc != 0:
            print("\033[37;45m  UI\033[0m:    Interfaz interactiva intentando reconexiÃ³n...")
            client.reconnect()

    def add_number(self, num):
        if len(self.current_input) < self.max_digits:
            self.current_input += str(num)
            self.update_display()
        else:
            self.display.configure(text="MÃXIMO", text_color="red")
            self.app.after(1000, self.update_display)

    def delete_last_char(self):
        self.current_input = self.current_input[:-1]
        self.update_display()

    def clear_input(self):
        self.current_input = ""
        self.update_display()

    def confirm_input(self):
        if self.current_input:
            if self.current_input == self.exit_code:
                self.app.attributes("-fullscreen", False)
                self.display.configure(text="Modo Ventana", text_color="green")
                self.app.after(2000, self.clear_input)
            else:
                mensaje = {"codigo": self.current_input, "locker": SLOCKER}
                self.client.publish(TOPIC_PANTALLA, json.dumps(mensaje), qos=1)
                print("\033[37;42mRASP\033[0m:    Enviado comando al servidor...")
                self.clear_input()

    def update_display(self):
        self.display.configure(
            text=self.current_input if self.current_input else "0",
            text_color="white"
        )

    def mostrar_notificacion(self, mensaje):
        self.notificacion_label.configure(text=mensaje, text_color="green")
        self.app.after(3000, lambda: self.notificacion_label.configure(text=""))

    def start(self):
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_start()
        self.app.mainloop()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.app.destroy()

# Función principal
def main():
    try:
        # Iniciar monitor de sensor en un hilo separado
        sensor_monitor = SensorMonitor()
        sensor_thread = Thread(target=sensor_monitor.start)
        sensor_thread.daemon = True
        sensor_thread.start()

        # Iniciar interfaz de usuario
        app = CalculatorApp()
        app.start()

    except KeyboardInterrupt:
        print("\n\033[37;42mRASP\033[0m:    Programa terminado por el administrador.")
    finally:
        sensor_monitor.stop()
        GPIO.cleanup()
        print("\033[37;42mRASP\033[0m:    Recursos liberados.")

if __name__ == "__main__":
    main()