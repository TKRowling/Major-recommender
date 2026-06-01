import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/app.css";

function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    sessionStorage.setItem(
      "user",
      JSON.stringify({
        email,
        isLoggedIn: true,
      })
    );

    navigate("/recommendation");
  };

  return (
    <main className="login-page">
      <div className="login-card">
        <h2>Login</h2>
        <p>Sign in to continue using ChomNeanh AI.</p>

        <form onSubmit={handleLogin} className="login-form">
          <input
            type="email"
            placeholder="Email"
            value={email}
            required
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            required
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Login</button>
        </form>
      </div>
    </main>
  );
}

export default LoginPage;