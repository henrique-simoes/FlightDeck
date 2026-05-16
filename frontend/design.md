# Eventinkerer – Identidad de Marca

## Esencia
Eventinkerer es una plataforma moderna y vibrante para descubrir y comprar entradas a conciertos, conferencias, presentaciones y festivales. La marca transmite **energía, cercanía y confianza**, evocando la emoción previa a un evento en vivo.

## Principios visuales
- **Curvas suaves**: radios grandes (1.25rem base, hasta 2xl/3xl en tarjetas y botones) para una sensación amigable y contemporánea.
- **Gradientes sutiles**: violeta → cian como firma visual en logo, CTAs y portadas de eventos.
- **Jerarquía clara**: tipografía bold para títulos, muted para metadatos.
- **Espacio generoso**: respiración entre tarjetas y secciones.

## Paleta (oklch)
| Token | Valor | Uso |
|---|---|---|
| Primary | `oklch(0.58 0.22 295)` – Violeta vibrante | CTAs, logo, acentos principales |
| Accent | `oklch(0.78 0.17 200)` – Cian eléctrico | Highlights, notificaciones, gradientes |
| Background | `oklch(0.985 0.005 280)` – Blanco con leve tinte lila | Fondo general |
| Foreground | `oklch(0.18 0.04 280)` – Casi negro con matiz violeta | Texto principal |
| Muted | `oklch(0.96 0.015 285)` | Fondos secundarios |
| Secondary | `oklch(0.95 0.03 290)` | Chips, badges |

El gradiente firma se construye con `from-primary to-accent` (violeta → cian).

## Tipografía
Sistema sans-serif por defecto del SO. Pesos: 400 (cuerpo), 600 (subtítulos), 700 (títulos).

## Componentes clave
- **Navbar**: sticky, blur translúcido, logo con tile gradiente + nombre con texto en gradiente, avatar con anillo de marca.
- **Filtros**: tarjeta sticky con chips redondeados, checkboxes y slider de precio.
- **Tarjeta de evento**: portada con gradiente único + emoji, badge de categoría flotante, metadatos con iconos, CTA en gradiente.

## Tono
Cercano, entusiasta, claro. Español neutro. Verbos en imperativo en CTAs ("Comprar entradas", "Aplicar filtros").

## Layout del home
- Navbar superior (logo izquierda, usuario logueado derecha).
- Cuerpo en grid 1/3 + 2/3: filtros a la izquierda, lista de eventos a la derecha.
- Responsive: en mobile, los filtros pasan arriba de la lista.
