## 🚀 Cómo Usar la Aplicación

### Ejecutar la Interfaz Gráfica

Para iniciar la aplicación con la interfaz gráfica Tkinter:

python gui.py

### 🧪 Ejecutar Pruebas

#### Ejecutar cada nivel de pruebas individualmente

**Pruebas Unitarias:**
python -m unittest tests.test_unitarias

**Pruebas de Integración:**
python -m unittest tests.test_integracion


**Pruebas de Sistema:**
python -m unittest tests.test_sistema


**Pruebas de Aceptación:**
python -m unittest tests.test_aceptacion


#### Ejecutar todas las pruebas

Para ejecutar todos los niveles de pruebas en una sola ejecución:

python run_all_tests.py

#### Ejecutar pruebas con mayor verbosidad

Para obtener información detallada de cada prueba:

python -m unittest tests.test_unitarias -v
