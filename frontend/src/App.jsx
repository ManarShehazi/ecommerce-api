/**
 * Root application component.
 *
 * Manages the global auth state (user + token).
 * - If not logged in → shows AuthForm
 * - If logged in → shows product catalog, credits, and order history
 *
 * Token is persisted in localStorage so the user stays logged in on refresh.
 * On login/register, the token + user info are stored and passed down to children.
 */

import { useState, useEffect, useCallback } from "react";
import AuthForm from "./components/AuthForm";
import ProductList from "./components/ProductList";
import OrderHistory from "./components/OrderHistory";
import { getBalance } from "./api";

/* ── Minimal global styles ─────────────────────────── */
const appStyle = {
  fontFamily: "'Segoe UI', system-ui, sans-serif",
  maxWidth: 800,
  margin: "0 auto",
  padding: "20px",
};

const headerStyle = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  borderBottom: "1px solid #ddd",
  paddingBottom: 12,
  marginBottom: 24,
};

export default function App() {
  // Auth state — restored from localStorage on mount
  const [user, setUser] = useState(null);
  const [credits, setCredits] = useState(0);

  // On mount, check if a session exists in localStorage
  useEffect(() => {
    const token = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
      // Fetch fresh balance from server
      getBalance()
        .then((data) => setCredits(data.credits))
        .catch(() => handleLogout()); // Token expired/invalid → log out
    }
  }, []);

  /** Called by AuthForm after successful login/register */
  const handleAuth = (authData) => {
    localStorage.setItem("token", authData.token);
    localStorage.setItem("user", JSON.stringify(authData.user));
    setUser(authData.user);
    setCredits(authData.user.credits);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    setCredits(0);
  };

  /** Refresh credit balance — called after adding credits or purchasing */
  const refreshCredits = useCallback(async () => {
    try {
      const data = await getBalance();
      setCredits(data.credits);
    } catch {
      // Silently fail — balance will refresh on next action
    }
  }, []);

  // ── Not logged in: show auth form ──
  if (!user) {
    return (
      <div style={appStyle}>
        <h1>🛒 E-Commerce Store</h1>
        <AuthForm onAuth={handleAuth} />
      </div>
    );
  }

  // ── Logged in: show the store ──
  return (
    <div style={appStyle}>
      <header style={headerStyle}>
        <h1>🛒 E-Commerce Store</h1>
        <div>
          <span>
            <strong>{user.username}</strong> — {credits.toFixed(1)} credits
          </span>
          <button onClick={handleLogout} style={{ marginLeft: 12 }}>
            Logout
          </button>
        </div>
      </header>

      <ProductList credits={credits} onBalanceChange={refreshCredits} />
      <OrderHistory />
    </div>
  );
}
