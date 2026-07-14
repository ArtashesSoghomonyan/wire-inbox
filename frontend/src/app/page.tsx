"use client";

import Typewriter from "typewriter-effect";

import { useAuth } from "@/context/AuthContext";
import LoadingPage from "@/components/LoadingPage";
import LoginForm from "@/components/LoginForm";
import styles from "./page.module.scss";
import { typewriterStrings } from "@/constants";


export default function Home() {
  const { user, loading, login, logout } = useAuth();

  if (loading) {
    return <LoadingPage />
  }

  if (!!user) {
    return <>
      <h1>Hello {user.username}</h1>
      <input type="button" className="primary-btn" value="logout" onClick={logout} />
    </>
  }

  return <div className={`${styles.center} ${styles.gradient}`}>
    <div className={styles.logo}>Wire Inbox</div>
    <div className={styles.typewriter}>
      <Typewriter options={{
        strings: typewriterStrings,
        autoStart: true,
        loop: true,
        cursor: "|",
      }} />
    </div>
    <div className={styles.container}>
      <LoginForm />
    </div>
  </div>
}
