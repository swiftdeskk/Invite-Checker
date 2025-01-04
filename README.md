# 🚀 Discord Invite Checker 📋

Este programa permite verificar el estado de las invitaciones de un servidor de Discord utilizando proxies (si se habilitan) y mostrar el estado de cada invitación.

---

## 📦 Instalación

### Requisitos

- **Python 3.6 o superior** 💻
- **Un archivo de configuración `config.yaml`** para definir los parámetros. 📄

### 1. Clona el repositorio

Primero, clona este repositorio a tu máquina local:

```bash
git clone https://github.com/tu_usuario/discord-invite-checker.git
```

### 2. Instala las dependencias

Instala las dependencias necesarias para que el programa funcione correctamente. Asegúrate de tener **pip** instalado.

```bash
cd discord-invite-checker
pip install -r requirements.txt
```

---

## ⚙️ Configuración

Antes de ejecutar el programa, asegúrate de configurar el archivo `config.yaml` con los parámetros correctos. Puedes editar este archivo según tus necesidades.

### **Archivo `config.yaml`** ejemplo:

```yaml
# Configuración de la cantidad mínima de miembros y el uso de proxies
min_members: 1000        # 🧑‍🤝‍🧑 Mínimo de miembros requeridos
proxies_enabled: true    # 🌐 Habilitar el uso de proxies
```

- **min_members**: El número mínimo de miembros que debe tener el servidor para que se considere una invitación válida.
- **proxies_enabled**: Si se habilitan proxies, el programa usará proxies para verificar las invitaciones.

---

## 🏃‍♂️ Uso

### Ejecutar el script

Para usar el programa, simplemente ejecuta el script `main.py`:

```bash
python main.py
```

### Opciones de línea de comandos

Puedes usar algunas opciones al ejecutar el script:

- `--min-members`: Especifica el número mínimo de miembros.
- `--proxies`: Habilita o deshabilita el uso de proxies.
- `--file`: Especifica el archivo de invitaciones a procesar.

### Ejemplo de uso:

```bash
python main.py --min-members 1000 --proxies --file invites.txt
```

Este comando procesará las invitaciones del archivo `invites.txt`, verificando si tienen al menos 1000 miembros y utilizando proxies si están habilitados.

---

## 📝 ¿Qué hace el programa?

El programa realiza lo siguiente:

1. Lee las invitaciones de Discord desde un archivo (por defecto `invites.txt`).
2. Verifica el estado de cada invitación utilizando proxies (si están habilitados).
3. Muestra la información de cada invitación, como el nombre del servidor y la cantidad de miembros.
4. Si el servidor tiene menos miembros de los especificados en `config.yaml`, se ignorará.

---

## 💡 Ejemplo de salida

Cuando ejecutes el programa, obtendrás una salida similar a esta:

```
🔗 Invite -> abc123, Server: My Server, Members: 🧑‍🤝‍🧑 1500
🔗 Invite -> xyz789, Server: Another Server, Members: 🧑‍🤝‍🧑 200
❌ Error: Proxy connection failed
✅ All invites processed.
```

- **🔗**: Muestra la invitación y el nombre del servidor.
- **🧑‍🤝‍🧑**: Indica el número de miembros en el servidor.
- **❌**: Muestra los errores de conexión si algo sale mal.

---

## 🤝 Contribuciones

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio. 🍴
2. Crea una nueva rama (`git checkout -b feature-name`). 🌱
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva característica'`). 🖋️
4. Empuja los cambios (`git push origin feature-name`). 🚀
5. Crea un pull request. 🤲

---
