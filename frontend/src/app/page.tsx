"use client";

import axios from "axios";
import { useState } from "react";
import Typewriter from "typewriter-effect";

import { useAuth } from "@/context/AuthContext";
import LoadingPage from "@/components/LoadingPage";
import LoginForm from "@/components/LoginForm";
import styles from "./page.module.scss";
import { typewriterStrings } from "@/constants";

export default function Home() {
  const { user, loading, logout, refreshUser } = useAuth();
  const [code, setCode] = useState(["", "", "", "", "", ""]);
  const [verificationError, setVerificationError] = useState("");

  const handleCodeChange = (value: string, index: number) => {
    const nextValue = value.replace(/\D/g, "").slice(0, 1);
    const updatedCode = [...code];
    updatedCode[index] = nextValue;
    setCode(updatedCode);

    if (nextValue && index < code.length - 1) {
      const nextInput = document.querySelector<HTMLInputElement>(`input[data-index="${index + 1}"]`);
      nextInput?.focus();
    }
  };

  const handleCodeKeyDown = (event: React.KeyboardEvent<HTMLInputElement>, index: number) => {
    if (event.key === "Backspace") {
      event.preventDefault();
      const updatedCode = [...code];

      if (updatedCode[index]) {
        updatedCode[index] = "";
      } else if (index > 0) {
        updatedCode[index - 1] = "";
        const previousInput = document.querySelector<HTMLInputElement>(`input[data-index="${index - 1}"]`);
        previousInput?.focus();
      }

      setCode(updatedCode);
    }

    if (event.key === "Enter") {
      event.preventDefault();
      void sendVerificationCode();
    }
  };

  const handleCodePaste = (event: React.ClipboardEvent<HTMLInputElement>) => {
    event.preventDefault();
    const pastedValue = event.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);

    if (!pastedValue) {
      return;
    }

    const updatedCode = Array(6).fill("");
    pastedValue.split("").forEach((digit, index) => {
      updatedCode[index] = digit;
    });

    setCode(updatedCode);

    const nextIndex = Math.min(pastedValue.length, 5);
    const nextInput = document.querySelector<HTMLInputElement>(`input[data-index="${nextIndex}"]`);
    nextInput?.focus();
  };

  const sendVerificationCode = async () => {
    const verificationCode = code.join("");

    if (verificationCode.length !== 6) {
      setVerificationError("Please enter the full 6-digit verification code.");
      return;
    }

    const token = localStorage.getItem("accessToken");

    if (!token) {
      setVerificationError("You are not authenticated.");
      return;
    }

    try {
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/users/verify-account/`,
        { code: verificationCode },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      await refreshUser();
      setVerificationError("");
    } catch (err) {
      console.error("Verification failed", err);
      setVerificationError("The verification code is invalid or expired.");
    }
  };

  if (loading) {
    return <LoadingPage />
  }

  if (!!user && !user.is_verified) {
    return <div className={`${styles.center} ${styles.gradient}`}>
      <div className={styles.logo}>Wire Inbox</div>
      <h2>Your account has been created successfully!</h2>
      <h2>We have sent you an email with verification code</h2>
      <div className={styles.verification}>
        {code.map((digit, index) => (
          <input
            key={index}
            maxLength={1}
            inputMode="numeric"
            autoComplete="one-time-code"
            value={digit}
            data-index={index}
            onChange={(event) => handleCodeChange(event.target.value, index)}
            onKeyDown={(event) => handleCodeKeyDown(event, index)}
            onPaste={handleCodePaste}
          />
        ))}
      </div>
      {verificationError ? <p>{verificationError}</p> : null}
      <button type="button" className="primary-btn" onClick={() => void sendVerificationCode()}>
        Verify account
      </button>
    </div>
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
