import { t } from "@/lib/diccionario";

export default function Pie({ locale }) {
  const d = t(locale);
  return (
    <footer className="pie">
      <div className="contenedor">
        <p>{d.piePropia}</p>
        <p>
          {d.pieFuente}
          <a href="https://github.com/killobs/unsu" target="_blank" rel="noreferrer">
            github.com/killobs/unsu
          </a>
        </p>
      </div>
    </footer>
  );
}
