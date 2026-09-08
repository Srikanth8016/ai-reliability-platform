"use client";

import { useState, useEffect } from "react";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";
import { getAuthToken } from "@/lib/api";
import { Loader2 } from "lucide-react";

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    // Check local storage on mount
    const token = getAuthToken();
    setIsAuthenticated(!!token);
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  if (isAuthenticated === null) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
      </main>
    );
  }

  return (
    <main className="min-h-screen">
      {isAuthenticated ? (
        <Dashboard onLogoutAction={handleLogout} />
      ) : (
        <Login onLoginAction={handleLogin} />
      )}
    </main>
  );
}
