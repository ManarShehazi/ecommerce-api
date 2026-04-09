/**
 * AuthForm — handles both registration and login.
 *
 * A single form with a toggle between "Register" and "Login" modes.
 * On success, calls props.onAuth(data) with { token, user } so the
 * parent (App) can store the session.
 */

import { useState } from "react";
import { register, login } from "../api";

const formStyle = {
  maxWidth: 360,
  margin: "40px auto",
  padding: 24,
  border: "1px solid #ddd",
  borderRadius: 8,
};

const inputStyle = {
  width: "100%",
  padding: 8,
  marginBottom: 12,
  boxSizing: "border-box",
};

const errorStyle = {
  color: "#d32f2f",
  marginBottom: 12,
  fontSize: 14,
};

export default function AuthForm({ onAuth }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // Call the appropriate API endpoint based on mode
      const data = isLogin
        ? await login(username, password)
        : await register(username, password);
      onAuth(data);
    } catch (err) {
      // Show the server's error message, or a generic fallback
      const message =
        err.response?.data?.detail || "Something went wrong. Please try again.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form style={formStyle} onSubmit={handleSubmit}>
      <h2>{isLogin ? "Login" : "Register"}</h2>

      {error && <p style={errorStyle}>{error}</p>}

      <input
        style={inputStyle}
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        style={inputStyle}
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      <button type="submit" disabled={loading} style={{ width: "100%", padding: 10 }}>
        {loading ? "Please wait..." : isLogin ? "Login" : "Register"}
      </button>

      <p style={{ textAlign: "center", marginTop: 12 }}>
        {isLogin ? "No account? " : "Already have an account? "}
        <button
          type="button"
          onClick={() => {
            setIsLogin(!isLogin);
            setError("");
          }}
          style={{ background: "none", border: "none", color: "#1976d2", cursor: "pointer", textDecoration: "underline" }}
        >
          {isLogin ? "Register" : "Login"}
        </button>
      </p>
    </form>
  );
}
