#FAQ del SysAcad Wrapper#

##Qué es el SysAcad Wrapper?##

Como estudiantes de la UTN FRRO que somos, sabemos lo estética y funcionalmente pobre que es el actual SysAcad.
Entonces, para ver si podíamos hacer algo mejor que eso, decidimos diseñar e implementar algo que nos dé una solución de manera sencilla.
Así, surgió el SysAcad Wrapper, una página que, sin ser una plataforma independiente al SysAcad, nos da más funciones y ofrece una estética mucho más moderna y amigable.
Por supuesto, el uso del SysAcad Wrapper es legal, ya que el Wrapper se comunica con el SysAcad original, de manera que TODO pasa por él.
Vale aclarar que almacenamos el legajo y otros datos en la DB (para la funcionalidad extendida) pero NO almacenamos tu contraseña.

##Por qué usaría el Wrapper y no el SysAcad original?##

La razón principal por la que lo usarías, que de hecho es la razón principal por la que creamos el Wrapper, es que __NO HAY NI UNA LETRA EN COMIC SANS!__
Otras razones son, además de la mejoradísima estética (más allá de la tipografía), la adición de algunas funciones y comodidades que en más de una vez podrían ser útiles,
como la sección de estadísticas.

##Qué tiene el Wrapper que no haya en el SysAcad?##

Uf, hay tantas cosas...
* Estadísticas (que consideramos muy útiles, por eso las nombramos tanto).
* Una muy mejorada visualización del estado académico (hello, colors!), con posibilidad de filtrar materias por su estado (aprobada, regular, cursando, no cursada) y mostrarlas por orden cronológico o alfabético.
* Mejorados los forms de inscripción.
* Podés encontrar a tus compañeros de cada materia y ver su mail, por si tenés que pedirles algo.
* Logros y scoreboard! Esto es complicado de explicar en una oración, así que habrá un apartado dedicado a esto.

##Logros? Scoreboard? Whaaaat?

Sí, logros y scoreboard! Y no es un juego de steam. Lo que pasa es lo siguiente: Cuando uno se mete al SysAcad, es para fijarse si está regular, para ver si subieron la nota de algún final, etc. Acá nosotros pusimos este tema de los logros, para que cada vez que hagas algo meritorio, puedas sonreír al ver que te ganaste un logro! Hay muchísimos logros dando vueltas por ahí. Y bueno, el scoreboard es un ranking según los logros que tenga cada uno.

##Che, pero a mi eso de los logros y el scoreboard me parece una gilada, honestamente...##

Bueno, depende que tan malo te parezca, podés mandar un mail a soporte@sysacadwrapper.com.ar expresando tu completo disgusto, o simplemente no mirarlo y dedicarte a no quererlo en silencio :D. De todas formas podés desactivar tu nombre del scoreboard por lo que nadie te vería ahí.

## Es seguro? ##

Totalmente. La contraseña se almacena así: Sabés lo que es un hash? Es una función que convierte una cadena de caracteres (tu password) en otra cadena de caracteres, sin ser posible el proceso inverso. El Wrapper guarda un hash de tu contraseña, y siempre que quieras iniciar sesión, compara el hash de lo que pongas, con el hash que tiene guardado. Si coincide, you're in :D. 

##La idea me parece bien, pero yo cambiaría algunas cosas...##

Por supuesto que estamos abiertos a todo tipo de sugerencia (y también informe de errores). Para comentarnos tus propuestas de cambio, mandá un mail a soporte@sysacadwrapper.com.ar, donde consideraremos todo lo que digas, y probablemente lo implementemos después de un tiempo.

##Uy, qué bueno! Quiero ayudar!##

Toda ayuda es más que agradecida. El proyecto es de código abierto, por lo que trabajar con nosotros debería ser algo muy fácil. De todas formas, si querés establecer algún tipo de contacto, podés mandar un mail a soporte@sysacadwrapper.com.ar, y podremos discutir :).
