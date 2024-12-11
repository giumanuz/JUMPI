import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../webApi";
import { useAuth } from "../authContext";

function RegisterPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!username || !email || !password) {
      setError("All fields are required!");
      return;
    }

    try {
      await registerUser(username, email, password);
      login();
      navigate("/");
    } catch (err) {
      setError((err as Error).message || "Registration failed.");
    }
  };

  return (
    <div className="d-flex flex-column align-items-center min-vh-100 justify-content-center">
      <h1>Register</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="form-control mt-3"
        style={{ width: "300px" }}
      />
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
        Register
      </button>
      <button onClick={() => navigate("/login")} className="btn btn-secondary mt-3">
        Already have an account? Login
      </button>
    </div>
  );
}

export default RegisterPage;
