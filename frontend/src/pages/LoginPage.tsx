import React, { useState } from "react";
import { useAuth } from "../authContext";
import { useNavigate } from "react-router-dom";
import { handleLogin } from "../authApi";

function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const onSubmit = async () => {
    try {
      await handleLogin(email, password);
      login();
      navigate("/");
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <div className="d-flex flex-column align-items-center min-vh-100 justify-content-center">
      <h1>Login</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="form-control mt-3"
        style={{ width: "300px" }}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="form-control mt-3"
        style={{ width: "300px" }}
      />
      <button onClick={onSubmit} className="btn btn-primary mt-3">
        Login
      </button>
      <button
        onClick={() => navigate("/register")}
        className="btn btn-secondary mt-3"
      >
        Register
      </button>
    </div>
  );
}

export default LoginPage;
