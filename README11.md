# 📊 Automatización de Cierre Contable

> Herramienta Python para automatizar el proceso de cierre contable mensual — sin fórmulas de Excel manuales.

[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/Licencia-MIT-22c55e?style=flat-square)](LICENSE)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![OpenPyXL](https://img.shields.io/badge/OpenPyXL-3.x-217346?style=flat-square)](https://openpyxl.readthedocs.io)

---

## ¿Qué hace?

Automatiza el cierre contable mensual a partir de un CSV exportado desde cualquier sistema contable. Clasifica transacciones por proveedor o palabra clave, detecta duplicados, marca excepciones para revisión manual y genera informes auditables listos para entregar.

**El archivo original nunca se modifica. Sin macros. Sin conocimientos técnicos.**

---

## ✨ Funcionalidades

| Funcionalidad | Descripción |
|---|---|
| 📥 **Importación CSV** | Compatible con cualquier exportación de sistema contable |
| ✅ **Validación de estructura** | Comprueba las columnas requeridas antes de procesar |
| 🏷️ **Clasificación automática** | Por nombre de proveedor y palabras clave en descripción |
| 🔍 **Detección de duplicados** | Identifica y aísla filas repetidas |
| ⚠️ **Marcado de excepciones** | Señala transacciones no clasificadas para revisión manual |
| 🔒 **No destructivo** | El archivo original nunca se toca |
| 📋 **Trazabilidad completa** | Log de cambios por cada clasificación aplicada |

---

## 📤 Archivos generados

Todos los archivos se crean en `data/output/`, con el nombre del archivo de entrada como prefijo.

```
data/output/
├── enero_ajustado.csv       ← filas originales + columnas de clasificación añadidas
├── enero_excepciones.csv    ← filas sin clasificar para revisión manual
├── enero_duplicados.csv     ← filas duplicadas detectadas
├── enero_log_cambios.csv    ← registro de auditoría completo
└── enero_informe.xlsx       ← libro Excel consolidado (todas las hojas)
```

---

## 🚀 Inicio rápido

### 1. Instalar dependencias

```bash
pip install pandas openpyxl pyyaml
```

### 2. Exportar el CSV

El archivo debe incluir estas columnas:

| Columna | Descripción |
|---|---|
| `fecha` | Fecha de la transacción |
| `proveedor` | Nombre del proveedor |
| `descripcion` | Descripción del concepto |
| `importe` | Importe de la transacción |
| `cuenta` | Código de cuenta contable |

### 3. Copiar el archivo a la carpeta de entrada

```
data/input/enero.csv
```

### 4. (Opcional) Editar las reglas de clasificación

Abre los archivos CSV en `data/rules/` y añade tus propias reglas — sin necesidad de programar.

**`proveedores.csv`** — clasificar por nombre de proveedor:

```csv
proveedor_buscar,categoria,centro_costo
iberdrola,Suministros Energía,Central
telefónica,Telecomunicaciones,Sucursal Norte
```

**`categorias.csv`** — clasificar por palabra clave en la descripción:

```csv
palabra_clave,categoria,centro_costo
alquiler,Gastos Fijos,Administración
software,Tecnología,Sistemas
```

### 5. Ejecutar la herramienta

**Windows** — doble clic en `ejecutar.bat`

**Terminal:**

```bash
cd src
python main.py
```

### 6. Revisar los resultados

Todos los archivos generados están en `data/output/`.

---

## 📁 Estructura del proyecto

```
cierre-contable/
├── data/
│   ├── input/          ← coloca aquí tus archivos CSV
│   ├── output/         ← informes y registros generados
│   └── rules/          ← reglas de clasificación editables (CSV)
├── src/
│   └── main.py         ← punto de entrada principal
├── config/             ← configuración de la herramienta
├── ejecutar.bat        ← lanzador Windows (doble clic para ejecutar)
└── instrucciones.txt   ← guía para el usuario final
```

---

## 🛠️ Tecnologías

| Librería | Uso |
|---|---|
| [Python 3.14+](https://python.org) | Lenguaje principal |
| [Pandas](https://pandas.pydata.org) | Procesamiento de datos y manipulación de CSV |
| [OpenPyXL](https://openpyxl.readthedocs.io) | Generación de informes Excel |
| [PyYAML](https://pyyaml.org) | Lectura de archivos de configuración |

---

## 📋 Ejemplos de reglas de clasificación

| Tipo de regla | Condición | Acción |
|---|---|---|
| Coincidencia de proveedor | Proveedor contiene `"iberdrola"` | Categoría → `"Suministros Energía"` |
| Coincidencia de palabra clave | Descripción contiene `"software"` | Categoría → `"Tecnología"` |
| Proveedor desconocido | Sin regla coincidente | Marcado como excepción |
| Columna ausente | Sin columna `"fecha"` en el archivo | El proceso se detiene con error |
| Fila duplicada | Fila idéntica detectada | Guardada en `duplicados.csv` |

---

## 📄 Licencia

Licencia MIT — libre para uso personal y comercial. Consulta [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Alejandro Peralta** — Especialista en Automatización de Procesos

- GitHub: [@alejandro-orbis](https://github.com/alejandro-orbis)
- LinkedIn: [linkedin.com/in/alejandro-orbis](https://linkedin.com/in/alejandro-orbis)
- Email: [alejandro@orbisautomations.com](mailto:alejandro@orbisautomations.com)

---

*Creado para eliminar el trabajo repetitivo del cierre — para que tu equipo se concentre en lo que realmente importa.*
