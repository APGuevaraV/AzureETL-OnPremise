# 🚀 Proyecto ETL en Azure con Arquitectura Medallón (Bronze → Silver → Golden)

Este proyecto implementa un flujo completo de ingestión, transformación y consumo de datos utilizando servicios de Azure. La solución sigue la arquitectura **Medallón** (Bronze → Silver → Golden) y permite mover datos desde un entorno On-Premise hasta un dashboard final en Power BI.

---

## 🧩 Arquitectura General

La arquitectura utilizada es la siguiente:

![Arquitectura del proyecto](/architecture/architecture.png)  


---

## 📥 1. Ingesta de Datos — On-Premise → ADLS Bronze

### 🔹 Fuente de datos
- Base de datos **AdventureWorks 2019**
- SQL Server instalado de manera **On-Premise** (local)

### 🔹 Proceso de ingesta
Usando **Azure Data Factory (ADF)** se configuró una *pipeline* para:

1. Conectarse al SQL Server On-Premise
2. Extraer todas las tablas de la BD
3. Guardarlas en **Azure Data Lake Storage Gen2 (ADLS)**  
4. Formato de almacenamiento: **Parquet**
5. Capa de destino: **Bronze**

---

## 🧼 2. Transformación — Bronze → Silver (Databricks)

En **Azure Databricks** se desarrolló un notebook dedicado al procesamiento inicial de los datos.

### 📘 Notebook 1: Limpieza y estandarización (Bronze → Silver)

Acciones realizadas:
- Lectura de cada tabla Parquet desde Bronze
- Limpieza de nulos y tipificación correcta
- Normalización básica
- Escritura tabla por tabla en:
  - **ADLS Silver**
  - Formato **Delta Lake**

Este notebook se integró como un **paso dentro de la pipeline de ADF**.

---

## 🔄 3. Transformación — Silver → Golden (Databricks)

### 📙 Notebook 2: Curación final y mejoras semánticas (Silver → Golden)

Acciones realizadas:
- Lectura de tablas Delta desde Silver
- Transformación de nombres de columnas:
  - De formato **PascalCase**
  - A formato **snake_case** con guion bajo (`example_column`)
- Validaciones finales
- Escritura en:
  - **ADLS Golden**
  - Formato **Delta Lake**

Este notebook también se agregó como un **paso dentro de la pipeline de ADF**.

---

## 📊 4. Modelado y Exposición de Datos — Synapse Analytics

Desde **Azure Synapse Analytics**:

### 🔹 Lectura desde ADLS Golden
- Se configuró una External Data Source hacia ADLS Golden.
- Se generaron vistas externas tipo *serverless* para cada tabla Delta.

### 🔹 Automatización con Stored Procedure
Mediante un **Stored Procedure**, se generó dinámicamente una vista por cada tabla Delta encontrada en Golden.

Este Stored Procedure fue ejecutado a través de un paso adicional en la pipeline.

---

## 📈 5. Consumo — Power BI

Finalmente, **Power BI** se conecta a las vistas generadas en Synapse para construir visualizaciones y dashboards interactivos.

---

## 🔐 6. Seguridad y Gobernanza

El proyecto implementa prácticas de seguridad y administración:

### ✔ Azure Active Directory
- Controla identidades y permisos del workspace
- Manejo de roles y acceso por servicio

### ✔ Azure Key Vault
- Almacena:
  - Keys
  - Secrets
  - Tokens
- Consumido por:
  - ADF
  - Synapse
  - Databricks

### ✔ External Locations en Databricks
- Administración segura de permisos de lectura y escritura hacia ADLS
- Minimiza la exposición de credenciales

---

## 📂 Estructura sugerida del repositorio

```txt
 📦 proyecto-etl-azure
├── architecture/
│ └── arquitectura-medallon.png
├── synapse/
│ ├── pipelines/
│ ├── sql/
│ └── notebooks/
├── databricks/
│ ├── bronze_to_silver.ipynb
│ └── silver_to_gold.ipynb
├── adf/
│ └── pipelines/
├── powerbi/
│ └── dashboard.pbix
└── README.md
 ```


---

## 🧠 Conclusión

Este proyecto muestra un flujo ETL profesional usando Azure, desde extracción On-Premise hasta la capa de visualización, incorporando buenas prácticas de:

- Arquitectura de datos (Medallón)
- Transformación con Spark
- Orquestación con ADF
- Modelado con Synapse
- Gobernanza con Key Vault y AAD

