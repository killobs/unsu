"use client";
import { useEffect, useRef, useState } from "react";

function sinMovimiento() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

// Regla común a los dos componentes: el estado "escondido" (opacidad 0, cifra en
// cero) NO se aplica al montar, sino recién en la primera respuesta del
// observador. Así, si el observador nunca contesta —sin JS, sin soporte, o un
// viewport de altura cero— queda a la vista el valor real en vez de un 0 o un
// bloque invisible. En un registro público, mostrar "0 sistemas" es peor que no
// animar.

export function Revelar({ children, retraso = 0, etiqueta: Etiqueta = "div", className = "" }) {
  const ref = useRef(null);
  const [estado, setEstado] = useState("libre"); // libre → sin clase, contenido visible

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (sinMovimiento()) return;

    let cuadro;
    const observador = new IntersectionObserver(
      ([entrada]) => {
        if (!entrada.isIntersecting) {
          setEstado("oculto");
          return;
        }
        // Ya visible en la primera respuesta: se esconde y se suelta al cuadro
        // siguiente, para que la transición tenga desde dónde arrancar.
        setEstado("oculto");
        cuadro = requestAnimationFrame(() => setEstado("visible"));
        observador.disconnect();
      },
      { threshold: 0.12, rootMargin: "0px 0px -50px 0px" },
    );
    observador.observe(el);
    return () => {
      observador.disconnect();
      if (cuadro) cancelAnimationFrame(cuadro);
    };
  }, []);

  const clases = ["revelar", estado === "oculto" && "es-oculto", estado === "visible" && "es-visible", className]
    .filter(Boolean)
    .join(" ");

  return (
    <Etiqueta ref={ref} className={clases} style={retraso ? { transitionDelay: `${retraso}ms` } : undefined}>
      {children}
    </Etiqueta>
  );
}

export function Cifra({ valor, formato, duracion = 1200 }) {
  const ref = useRef(null);
  const [n, setN] = useState(valor); // el HTML estático trae el número real

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (sinMovimiento()) return;

    let cuadro;
    const animar = () => {
      const inicio = performance.now();
      const paso = (ahora) => {
        const p = Math.min(1, (ahora - inicio) / duracion);
        setN(valor * (1 - Math.pow(1 - p, 3))); // easeOutCubic
        if (p < 1) cuadro = requestAnimationFrame(paso);
      };
      cuadro = requestAnimationFrame(paso);
    };

    const observador = new IntersectionObserver(
      ([entrada]) => {
        if (!entrada.isIntersecting) {
          setN(0); // recién aquí: el observador ya demostró que responde
          return;
        }
        setN(0);
        animar();
        observador.disconnect();
      },
      { threshold: 0.35 },
    );
    observador.observe(el);
    return () => {
      observador.disconnect();
      if (cuadro) cancelAnimationFrame(cuadro);
    };
  }, [valor, duracion]);

  return (
    <span ref={ref} className="cifra__numero">
      {formato ? formato(n) : Math.round(n).toLocaleString("es-PE")}
    </span>
  );
}
