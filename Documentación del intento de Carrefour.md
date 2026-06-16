
<h2>Índice.</h2>
<ol>
  <li><strong>Objetivo</strong></li>
  <li><strong>Enfoque inicial</strong></li>
  <li><strong>Problemas detectados</strong></li>
  <li><strong>Intentos de solución</strong>
    <ul>
      <li>4.1. Selenium básico</li>
      <li>4.2. User-Agent</li>
      <li>4.3. Navegador visible</li>
      <li>4.4. Esperas aleatorias</li>
      <li>4.5. Uso de perfil de usuario</li>
      <li>4.6. Simulación de comportamiento humano</li>
    </ul>
  </li>
  <li><strong>Análisis técnico</strong></li>
  <li><strong>Alternativas consideradas</strong></li>
  <li><strong>Decisión final</strong></li>
  <li><strong>Conclusión</strong></li>
</ol>
---
<h2>1. Objetivo</h2>

El objetivo de la práctica consistía en replicar el proceso de scraping realizado sobre Consum en la web de Carrefour con el fin de extraer:

* nombres del producto.
* precio

Todo esto con el fin de comparar el precio de los productos de ambos supermercados y elegir la opción más barata.

<h2>2. Enfoque inicial</h2>

Para la página web del Carrefour se ha intentado utilizar el mismo enfoque que en Consum:

- Librerías:
	- ``request``
	- ``BeautifulSoup``
	- ``Selenium``
- Construcción de URL de búsqueda:
```python
url = "https://www.carrefour.es/?q=" + busqueda.replace(" ", "+")
```

<h2>3. Problemas detectados</h2>

Desde el inicio se ha observado una serie de medidas anti-bots activas:

<h5>Bloqueo de Cloudflare</h5>
- Aparición de página:
	-  ``Attention Required``
- HTML con contenido inútil
- Utilización de Cloudflare Bot Management

<h5>Timeout en Selenium</h5>
Error más común:

``TimeoutException: Message:``

Indicado que los elementos (``article``) nunca cargaba.

<h5>Huella digital de Selenium</h5>
El sistema anti-bots de Cloudflare puede detectar los atributos automatizados de Selenium:

- ``window.navigator.webdrivet``
- Comportamientos establecidos de las librerías de python

También, Cloudflre realiza peticiones de información al cliente con el fin de obtener incongruencias sobre el equipo que está lanzando el buscador y la resolución que está utilizando la página.

<h5>HTML incompleto</h5>
En algunos casos:

```html
<title>Compra Online en Carrefour...</title>
```

Pero:
- Sin productos
- Sin estructura esperada

<h5>Dependencia de interacción manual</h5>
- Necesidad de aceptar cookies
- Sin interacción → no carga contenido

<h5>Bloqueo progresivo</h5>
- Primer intento → funciona parcialmente
- Intentos siguientes → bloqueo total

<h2>4. Intentos de solución.</h2>

<h3>4.1. Selenium básico.</h3>

```python
options.add_argument('--headless')
```

No se han podido obtener datos para el proyecto.

<h3>4.2. User-Agent.</h3>
```python
options.add_argument("user-agent=Mozilla/5.0")
```

A pesar de cambiar el **User-Agent**, el bloqueo persistió debido a que el Fingerprinting de Cloudflare detectaba inconsistencias entre la identidad declarada (Cabecera HTTP) y las capacidades técnicas reales del navegador controlado por Selenium. Cambiar el User-Agent es como ponerse una máscara; el fingerprinting es como analizar el ADN: la máscara no engaña a un análisis de laboratorio.

<h3>4.3. Navegador visible (no headless).</h3>
Eliminado el módulo anterior ``--headless`` que eliminaba la visualización del navegador, para que Cloudflare detecte el bot como "más humano".

Al primer uso tras eliminar esta opción, el acceso es concedido, pero en un segundo lanzamiento, el buscador el bloqueado para los posteriores intentos de acceso.

<h3>4.4. Esperas aleatorias.</h3>
```python
time.sleep(random.uniform(2,5))
```

El tiempo de espera aleatorio, ha sido útil para Consum, pero no ha funcionado en este caso, pues Cloudflare bloquea el acceso desde el principio.

<h3>4.5. Uso de perfil de usuario.</h3>

```python
--user-data-dir
```

Acceso permitido efímeramente. Sin embargo, el sistema de persistencia de cookies de Cloudflare detectó patrones de automatización en sesiones sucesivas, obligando a la regeneración constante del perfil, lo cual invalida la escalabilidad del script.

<h3>4.6. Simulación de comportamiento humano.</h3>
Con el fin de engañar a Cloudflate, he intentado imitar el comportamiento humano, con el fin de que pueda pasar más desapercibido utilizando:
- scroll
- delays

Pero una vez más esto no ha funcionado y Cloudflare ha bloqueado el acceso tras el primer uso como en intentos anteriores.

<h2>5. Análisis técnico.</h2>
Tras la fase de pruebas y la investigación de los logs de respuesta, he podido determinar que el sitio web emplea Cloudflare Bot Management, un sistema de seguridad de nivel empresarial.

<h3>Factores de bloqueo detectados:</h3>
**Análisis de comportamiento**: Identificación de patrones de navegación no humanos (velocidad de clic, precisión de movimiento).

**Contenido dinámico inaccesible**: Los datos no se encuentran en el HTML base, sino que se inyectan tras superar retos de seguridad.

**Dependencia de interacción humana**: Obligatoriedad de resolución de retos (CAPTCHA o Turnstile) mediante periféricos reales.

<h3>Flujo de Intento y Error (Ciclo de detección):</h3>
El proceso de bloqueo sigue una secuencia técnica lógica que impide la ejecución del script:

**Petición inicial**: Selenium solicita acceso a carrefour.es. El servidor intercepta la solicitud antes de entregar el contenido.

**Fingerprinting (Huella digital):** Cloudflare analiza la "huella" del navegador. Se verifican elementos como la resolución, fuentes instaladas y, críticamente, la propiedad navigator.webdriver.

**Desafío (JavaScript Challenge)**: Se lanza un script de JavaScript que debe ejecutarse en segundo plano. Mientras un navegador humano lo resuelve en milisegundos, Selenium es detectado por su latencia o por no procesar correctamente el motor de renderizado.

**Bloqueo**: Al detectar una discrepancia en los pasos anteriores, el servidor deniega el acceso (Error 403) y sirve una página de "Attention Required" con contenido HTML nulo para el scraping.

<h2>6. Alternativas consideradas.</h2>
Se han evaluado opciones más avanzadas para la obtención de resultados y proseguir con el proyecto:

- Proxies
- Rotación de IP
- Evasión de detección

<h2>7. Decisión final.</h2>
Tras lo anteriormente mencionado y tras una consulta con el profesorado, se ha decidido no implementar este tipo de técnicas debido a:

- Exceden el alcance académico
- Pueden vulnerar términos de uso
- No aportan valor al objetivo del proyecto

<h2>8. Conclusión.</h2>
Con todo lo mencionado en este documento, he optado por otra vía para continuar con el proyecto.

Pero aún así he podido aprender sobre las limitaciones reales que existen en el ``scraping``, la importancia de analizar el contexto y la necesidad de tomar decisiones técnicas y éticas.

Este desafío me ha permitido entender que el scraping moderno no es solo extraer etiquetas HTML, sino una constante carrera tecnológica entre la automatización y la ciberseguridad. También me ha servido como caso de estudio sobre la robustez de los sistemas de defensa modernos. He comprendido que el scraping actual es una disciplina en constante evolución donde la gestión de la identidad digital es tan crítica como el código de extracción propiamente dicho.