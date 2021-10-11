export default function Card({title, body}) {
  return (
    <div className="content p-3">
      <div className="card shadow mb-4">
        <div className="card-header py-3">
          <h6 className="m-0 font-weight-bold text-primary">{title}</h6>
        </div>
        <div className="card-body">
          {body}
        </div>
      </div>
    </div>
  )
}