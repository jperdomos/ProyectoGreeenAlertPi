
# 🌡️ GreenAlertPi: Sistema embebido de monitoreo ambiental con alertas inteligentes

📚 Proyecto académico  
**Universidad Nacional de Colombia – Sede Manizales**  
Facultad de Ingeniería y Arquitectura  
Asignatura: **Programación en Sistemas Linux Embebidos**  
Periodo: 2025-1

---

👤 Autores

- 🎓 Juan Camilo Perdomo  
  - GitHub: [@jperdomos](https://github.com/jperdomos)  
  - Correo: jperdomos@unal.edu.co
- 🎓 Campos Herney Tulcan  
  - GitHub: [@jperdomos](https://github.com/jperdomos)  
  - Correo: jperdomos@unal.edu.co  

---

## 📘 1. Descripción

**GreenAlertPi** es un sistema embebido desarrollado en Python sobre una Raspberry Pi Zero 2 W, diseñado para monitorear condiciones ambientales (temperatura y humedad) en invernaderos o entornos agrícolas. El sistema integra sensores, salidas físicas (LED y buzzer), una interfaz en terminal (TUI), registros automáticos de eventos y un bot de Telegram para supervisión y control remoto.

El propósito es ofrecer una solución **inteligente, local y de bajo costo**, capaz de alertar en tiempo real cuando se superan umbrales críticos ambientales, sin depender de interfaces gráficas pesadas ni conexión constante a monitores.

---

## 🧱 2. Diagrama general del sistema
![Diagrama del sistema](diagramabloques.png)
---

## 🔌 3. Componentes físicos (hardware)

- 🧠 **Raspberry Pi Zero 2 W**  
- 🌡️ **Sensor DHT11** para temperatura y humedad (GPIO 4)  
- 🚨 **LED rojo** (indicador visual de alerta, GPIO 17)  
- 🔊 **Buzzer activo o pasivo con PWM** (alarma sonora, GPIO 27)  
- 🪛 Conexiones GPIO con resistencias y jumpers  
- 🔌 Alimentación 5V / 2A  

---

## 🧠 4. Funcionalidades principales

| Módulo               | Descripción                                                                 |
|----------------------|------------------------------------------------------------------------------|
| ✅ Lectura sensorial  | Usa `Adafruit_DHT` para leer temperatura y humedad desde el sensor DHT11.   |
| 🚨 Activación de alerta | Si los valores superan los umbrales definidos, se activa un LED y buzzer con PWM. |
| 📊 Registro de eventos | Cada alerta se guarda automáticamente en un archivo CSV con hora, valores y estado. |
| 🖥️ Interfaz TUI       | Interfaz de texto en tiempo real en la terminal, con lectura continua y comandos. |
| 🤖 Bot de Telegram    | Permite consultar estado ambiental y desactivar alerta desde cualquier lugar. |
| 🔧 Systemd             | El sistema se lanza automáticamente al encender la Raspberry.                |

---

## 🧩 5. Estructura del proyecto

```
GreenAlertPi/
├── data/
│   ├── alerta_estado.json
│   ├── alert_log.csv
│   └── alert_state.py
├── src/
│   ├── sensor_reader.py
│   ├── alert_manager.py
│   ├── settings.py
│   └── test_*.py
├── telegram/
│   ├── bot_handler.py
│   ├── config.py
│   └── get_chat_id.py
├── tui/
│   └── interface.py
├── tests/
├── venv/
├── requirements.txt
├── greentui.service
└── README.md
```

---

## ⚙️ 6. Instalación

### 📦 Requisitos

- Raspberry Pi Zero 2 W  
- Raspberry Pi OS Lite actualizado  
- Acceso SSH o terminal  
- Sensor DHT11 conectado al GPIO 4  
- LED y buzzer conectados a GPIO 17 y 27  

### 🧰 Instalación paso a paso

```bash
sudo apt update && sudo apt install python3-pip python3-venv

cd ~/GreenAlertPi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 7. Ejecución

### Modo manual (TUI)

```bash
cd ~/GreenAlertPi
source venv/bin/activate
python3 tui/interface.py
```

### Modo automático con `systemd`

Archivo `/etc/systemd/system/greentui.service`:

```ini
[Unit]
Description=GreenAlertPi - Interfaz TUI de monitoreo
After=multi-user.target

[Service]
User=user
WorkingDirectory=/home/user/GreenAlertPi
ExecStart=/home/user/GreenAlertPi/venv/bin/python3 tui/interface.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable greentui
sudo systemctl start greentui
```

---

## 💬 8. Bot de Telegram

Este bot permite:

- Consultar temperatura y humedad actual
- Desactivar una alerta activa manualmente
- Recibir alerta automática cuando se dispare una condición crítica

### 📌 Requisitos

- Crear un bot con [@BotFather](https://t.me/BotFather)
- Guardar tu `TOKEN` en `telegram/config.py`
- Obtener tu `CHAT_ID` con `telegram/get_chat_id.py`

### 🧪 Ejecución

```bash
source venv/bin/activate
python3 telegram/bot_handler.py
```

---

## 📊 9. Registro de eventos

Cada vez que se activa una alerta, se registra en `data/alert_log.csv`:

| Timestamp           | Temperatura | Humedad | Estado  |
|---------------------|-------------|---------|---------|
| 2025-07-25 06:10:02 | 32.5 °C     | 78 %    | ACTIVA  |
| 2025-07-25 06:12:44 | 30.1 °C     | 81 %    | ACTIVA  |

---

## 🧪 10. Pruebas realizadas

| Módulo                | Verificación                                                                 |
|------------------------|------------------------------------------------------------------------------|
| Sensor DHT11           | Lectura estable y continua de temperatura y humedad                         |
| GPIO salida (LED/Buzz) | Activación PWM y desactivación controlada                                    |
| Archivo JSON estado    | Lectura y escritura correcta del estado en `alerta_estado.json`              |
| CSV eventos            | Registro correcto en `alert_log.csv`                                         |
| Interfaz TUI           | Visualización y control por teclado en tiempo real                           |
| Bot Telegram           | Respuestas correctas a comandos, envío de alertas automáticas                |
| Systemd                | Arranque automático, reinicio en caso de fallo, persistencia                 |

---

## 🎯 11. Comandos útiles

```bash
# Activar entorno virtual
source venv/bin/activate

# Ver interfaz manualmente
python3 tui/interface.py

# Verificar logs del servicio
sudo journalctl -u greentui.service -f

# Ejecutar bot de Telegram
python3 telegram/bot_handler.py
```

---

## 🧭 12. Conclusiones

GreenAlertPi demuestra cómo es posible construir un sistema embebido completo, eficiente y extendible usando Python, Raspberry Pi y sensores simples. Su arquitectura modular y sus múltiples interfaces (TUI, Telegram, registro local) lo hacen ideal para aplicaciones agrícolas y educativas.

---

## ⚖️ Licencia

MIT License – Proyecto de uso académico, libre para modificar y reutilizar con atribución adecuada.

© 2025 Juan Perdomo — Universidad Nacional de Colombia
