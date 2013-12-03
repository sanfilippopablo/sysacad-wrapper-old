Coding Style - Naming Conventions
=================================

### Idioma

Los nombres de variables, nombres de bloques, vistas, urls, tags y demás deben escribirse en inglés. Sólo debe usarse el español para palabras exclusivas del problema (materia, legajo, alumno, etc).

**No:**
* `ALLOWED_FILENUMBER`
* `LEGAJOS_PERMITIDOS`

**Sí:**
* `ALLOWED_LEGAJOS`

**No:**
* `PersonalSettingsView`
* `VistaAjustesPersonales`

**Sí:**
* `AjustesPersonalesView`

Puede gustar o no, pero es sólo una convención, para ser consistentes.

### Coding style

`ThisIsAClass`

### Nombres de cosas específicas

Los códigos de estado de materias son:
* Materia aprobada: `aprobada`
* Materia regularizada: `regular`
* Materia en curso: `cursa`
* Materia a la que todavía no se está inscripto: `no_inscripto`
