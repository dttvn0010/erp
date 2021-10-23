import axios from "axios";
import { useRouter } from "next/router";
import { useState } from "react"

export default function Login() {
  const router = useRouter();
  const [err, setErr] = useState('');

  const logIn = (e) => {
    e.preventDefault();
    const data = new FormData(document.getElementById('fmt'));
    axios.post('/api/token', data).then(result => {
      localStorage.setItem('token', result.data.access);
      router.push('/');
    }).catch(_ => {
      setErr('Tên đăng nhập hoặc mật khẩu không đúng')
    })
  }
  return (
    <div className="bg-login">
      <div className="login-form">
        <h3>Đăng nhập</h3>
        <br/>
        <form id="fmt" onSubmit={logIn} method="POST">
          <div className="mb-3">
            <label className="form-label">Tên tài khoản</label>
            <input name="username" type="text" className="form-control" />
          </div>
          <div className="mb-3">
            <label className="form-label">Mật khẩu</label>
            <input name="password" type="password" className="form-control" />
          </div>
          <div className="mb-3" style={{color: "red"}}>
            {err}
          </div>
          <br/>
          <div className="mb-3">
            <button type="submit" className="btn btn-primary btn-block">Đăng nhập</button>
          </div>
          <div className="clearfix">
            <a href="#/" className="float-end">Quên mật khẩu?</a>
          </div>
        </form>
        
        <p className="text-center mt-3">
          <a href="#/">Đăng ký tài khoản</a>
        </p>
      </div>
    </div>
  )
}