export default function OrbeCarga({ texto }) {
  return (
    <div className="orbe-carga" role="status" aria-live="polite">
      <span className="orbe-carga__esfera" aria-hidden="true" />
      <span>{texto}</span>
    </div>
  );
}
