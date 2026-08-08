#  Sistema de Preguntas

##  Integrantes del Grupo
- Mathias Medina - 
- Kenny Blacio - 
- Cristhian Solano - 
#### **Fecha de inicio:** [27/07/2026]
#### - Entrega: [08/08/2026]

##  Descripción del Proyecto

El proyecto comprende el diseño e implementación de un Banco de Preguntas interactivo en Python, orientado al almacenamiento, administración y evaluación dinámica de reactivos.

Capacidades Principales

Gestión multiformato: Carga e importación flexible de datos desde archivos TXT, CSV y JSON, centralizando la persistencia en una base de datos SQLite mediante el patrón DAO (Data Access Object).

Evaluación e informes: Motor de simulación con selección aleatoria de reactivos, validación inmediata de respuestas, calificación automática y generación de reportes exportables a JSON, CSV y TXT.

Análisis de datos: Panel de consulta para visualizar estadísticas detalladas segmentadas por materia y nivel de dificultad.

Arquitectura y Calidad
Desarrollado bajo el paradigma de Programación Orientada a Objetos (POO), el sistema aplica una estricta separación de responsabilidades dividida en módulos independientes (entidades, acceso a datos, lógica de negocio y simulador). Además, incluye una suite de pruebas unitarias que garantiza la fiabilidad y correcto funcionamiento de cada componente.

##  Tecnologías Utilizadas
- Python 3.8+
- SQLite3
- Git



##  Estructura Inicial del Proyecto
![estructura del proyecto]
![entidad y su estructura]
![constructor que sirve]

##  Archivos de Preguntas Generados
- ✅ preguntas.txt (50 preguntas)
- ✅ preguntas.csv (50 preguntas)
- ✅ preguntas.json (50 preguntas)
![archivos cargados]


## 🗄️ Base de Datos SQLite
- ✅ Tabla 'preguntas' creada
- ✅ Conexión exitosa
- ✅ Métodos CRUD implementados

![estructura de la tabla]
![insercio


## 📥 Carga de Datos desde Archivos
- ✅ Carga desde TXT: 50 preguntas cargadas
- ✅ Carga desde CSV: 50 preguntas cargadas
- ✅ Carga desde JSON: 50 preguntas cargadas

![txt]
![csv]
![json]

## 💾 Guardado en Base de Datos
- ✅ 50 preguntas guardadas en SQLite
- ✅ Exportación a TXT desde BD
- ✅ Exportación a CSV desde BD
- ✅ Exportación a JSON desde BD

![cargar a la base de datos]
![archivos exportados]

## 🎮 Simulador de Evaluación
- ✅ Selección aleatoria de preguntas
- ✅ Interacción con usuario
- ✅ Validación de respuestas
- ✅ Cálculo de puntaje

![]


##  Generación de Reportes
-  Reporte TXT generado
-  Reporte CSV generado
-  Reporte JSON generado
![estadisticas.csv]
![reporte.json]
![respuestas.txt]



## Pruebas Finales
-  Pruebas unitarias pasadas
-  Integración completa verificada
-  Manejo de errores implementado



##  Conclusiones

### Resumen del trabajo realizado



Este proyecto abarcó el desarrollo integral de un sistema de evaluaciones interactivo en Python, estructurado bajo una arquitectura de separación de responsabilidades con acceso a bases de datos SQLite (patrón DAO) y exportación de reportes en TXT, CSV y JSON.

Componentes y Funcionalidades Desarrolladas

Módulo central: Gestión de la entidad de preguntas, validación de respuestas en tiempo real, cálculo automático de puntajes y simulador interactivo.

Interfaz y robustez: Menú en consola para navegación fluida, control exhaustivo de excepciones y suite de pruebas unitarias para validar la estabilidad de los módulos.

Lecciones Aprendidas

Arquitectura y buenas prácticas: Consolidación de Programación Orientada a Objetos (POO), persistencia relacional con SQLite y manejo eficiente de archivos.

Calidad de software: Comprensión del valor de las pruebas unitarias, la validación estricta de datos y la organización modular para facilitar el mantenimiento futuro.

Mejoras Futuras

Experiencia de usuario y control: Evolución hacia una interfaz gráfica (GUI) e implementación de un módulo de autenticación con historial de intentos.

Adaptabilidad e IA: Integración de dificultad adaptativa, compatibilidad con nuevos formatos de datos e inteligencia artificial para la generación automática de reactivos y análisis predictivo del rendimiento.