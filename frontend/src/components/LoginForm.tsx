"use client";

import { useState } from "react";
import Link from "next/link";

import { useAuth } from "@/context/AuthContext";
import styles from "./LoginForm.module.scss";

export default function LoginForm() {
  const { user, loading, login } = useAuth();
  const [isError, setIsError] = useState<boolean>(false);
  const [emailInput, setEmailInput] = useState<string>("");
  const [passwordInput, setPasswordInput] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      await login({ email: emailInput, password: passwordInput });
    } catch {
      setIsError(true);
    }
  }

  return <form method="POST" onSubmit={handleSubmit} className={styles.loginForm}>
    <p>Don't have an account? <Link href="/signup">Sign up</Link></p>
    <input type="button" value="Continue with Google" className="soft-btn" />
    <p className={styles.or}>or</p>
    {isError && <p className="error-text">Wrong credentials</p>}
    <input
      type="email"
      placeholder="Email"
      className="input"
      value={emailInput}
      onChange={e => setEmailInput(e.target.value)}
    />
    <input
      type="password"
      placeholder="Password"
      value={passwordInput}
      className="input"
      onChange={e => setPasswordInput(e.target.value)}
    />
    <input
      type="submit"
      value="Log In"
      className="primary-btn"
      disabled={!(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput) && passwordInput.length >= 8)}
    />
    <a href="#">Forgot Password?</a>
  </form>
}
