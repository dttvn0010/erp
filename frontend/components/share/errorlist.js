export default function ErrorList({errors}) {
  if(!errors) return <></>;
  return (
    <ul className="errorlist">
      {errors.map((err, i) =>
        <li key={i}>{err}</li>
      )}
    </ul>
  )
}