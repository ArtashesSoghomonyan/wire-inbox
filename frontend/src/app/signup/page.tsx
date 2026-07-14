"use client";

import { useRef, useState } from "react";
import Typewriter from "typewriter-effect";
import { useRouter } from "next/navigation";
import axios from "axios";
import Link from "next/link";

import { useAuth } from "@/context/AuthContext";
import { allowedEmailDomains, forbiddenUsernames, typewriterStrings } from "@/constants";
import LoadingPage from "@/components/LoadingPage";
import mainStyles from "../page.module.scss";
import styles from "./SignUp.module.scss";


type RegistrationData = {
  username: string | null,
  email: string | null,
  password: string | null,
  firstName: string | null,
  lastName: string | null,
}

export default function Home() {
  const { user, loading, login } = useAuth();
  const router = useRouter();

  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [finalError, setFinalError] = useState<boolean>(false);
  const [step, setStep] = useState<number>(1);
  const [formData, setFormData] = useState<RegistrationData>({
    username: "",
    email: "",
    password: "",
    firstName: "",
    lastName: "",
  });
  const [errors, setErrors] = useState<RegistrationData>({
    username: null,
    email: null,
    password: null,
    firstName: null,
    lastName: null,
  });
  const usernameTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const emailTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const validateEmail = (email: string) => {
    setFormData({ ...formData, email: email });

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setErrors({ ...errors, email: "Please enter a valid email." });
      return;
    } else if (!allowedEmailDomains.includes(email.split("@")[1])) {
      setErrors({ ...errors, email: "Sorry this email domain is not supported." });
      return;
    }

    // Cancel the previous pending API call
    if (emailTimeoutRef.current) {
      clearTimeout(emailTimeoutRef.current);
    }

    // Debounce: wait 1 second after the user stops typing before calling the API
    emailTimeoutRef.current = setTimeout(async () => {
      try {
        const response = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/users/check-email/`,
          {
            params: {
              email: email,
            },
          },
        );

        if (!response.data.available) {
          setErrors({
            ...errors,
            email: "This email is not available to use.",
          });
        } else {
          setErrors({ ...errors, email: null });
        }
      } catch {
        setErrors({ ...errors, email: "Could not check email availability." });
      }
    }, 1000);
  };

  const validateUsername = (username: string) => {
    setFormData({ ...formData, username: username });

    if (!(username.length >= 1 && username.length <= 50)) {
      setErrors({
        ...errors,
        username: "Username can have less than 50 characters.",
      });
      return;
    } else if (!/^[a-z_]+$/.test(username)) {
      setErrors({
        ...errors,
        username: "Username can only contain english letters and underscores",
      });
      return;
    } else if (forbiddenUsernames.includes(username)) {
      setErrors({ ...errors, username: "This username is not allowed." });
      return;
    }

    // Cancel the previous pending API call
    if (usernameTimeoutRef.current) {
      clearTimeout(usernameTimeoutRef.current);
    }

    // Debounce: wait 1 second after the user stops typing before calling the API
    usernameTimeoutRef.current = setTimeout(async () => {
      try {
        const response = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/users/check-username/`,
          {
            params: {
              username: username,
            },
          },
        );

        if (!response.data.available) {
          setErrors({ ...errors, username: "This username is already used." });
        } else {
          setErrors({ ...errors, username: null });
        }
      } catch {
        setErrors({
          ...errors,
          username: "Could not check username availability.",
        });
      }
    }, 1000);
  };

  const validatePassword = (password: string) => {
    setFormData({ ...formData, password: password });

    if (password.length < 8) {
      setErrors({
        ...errors,
        password: "Password is too short, it should be at least 8 characters.",
      });
    } else if (/^\d+$/.test(password)) {
      setErrors({
        ...errors,
        password: "Password cannot be entirely numeric.",
      });
    } else if (
      [formData.username, formData.firstName, formData.lastName, formData.email]
        .filter((v): v is string => v !== null && v.length > 0)
        .some((v) => password.toLowerCase().includes(v.toLowerCase()))
    ) {
      setErrors({
        ...errors,
        password: "Password is too similar to your personal information.",
      });
    } else {
      setErrors({ ...errors, password: null });
    }
  };

  const validateFirstName = (firstName: string) => {
    setFormData({ ...formData, firstName: firstName });

    if (!/^\p{L}+$/u.test(firstName)) {
      setErrors({
        ...errors,
        firstName: "First name can only contain letters.",
      });
    } else {
      setErrors({ ...errors, firstName: null });
    }
  };

  const validateLastName = (lastName: string) => {
    setFormData({ ...formData, lastName: lastName });

    if (!/^\p{L}+$/u.test(lastName)) {
      setErrors({ ...errors, lastName: "Last name can only contain letters." });
    } else {
      setErrors({ ...errors, lastName: null });
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/users/register/`,
        {
          email: formData.email,
          username: formData.username,
          first_name: formData.firstName,
          last_name: formData.lastName,
          password: formData.password,
        },
      );

      if (response.status === 201) {
        await login({
          email: formData.email || "",
          password: formData.password || "",
        });
        router.push("/");
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setFinalError(true);
      }
    }
  }

  if (loading) {
    return <LoadingPage />
  }

  if (!!user) {
    router.push("/");
  }

  return <div className={`${mainStyles.center} ${mainStyles.gradient}`}>
    <div className={mainStyles.logo}>Wire Inbox</div>
    <div className={mainStyles.typewriter}>
      <Typewriter options={{
        strings: typewriterStrings,
        autoStart: true,
        loop: true,
        cursor: "|",
      }} />
    </div>
    <div className={mainStyles.container}>
      <form method="POST" onSubmit={handleSubmit} className={styles.form}>
        {finalError && <p className="error-text">Oops something went wrong, please try again later!</p>}
        {step === 1 && (<>
          <h3>Join our community right now!</h3>
          <p>Already have an account? <Link href="/">Sign in</Link></p>
          {errors.email && <p className="error-text">{errors.email}</p>}
          <input
            type="email"
            placeholder="Email"
            onChange={(e) => validateEmail(e.target.value.trim())}
            className={errors.email ? "input error-input" : "input"}
            value={formData.email || ""}
            required
          />
          {errors.username && <p className="error-text">{errors.username}</p>}
          <input
            type="text"
            placeholder="Username"
            onChange={(e) => validateUsername(e.target.value.trim())}
            className={errors.username ? "input error-input" : "input"}
            value={formData.username || ""}
            required
          />
          {errors.password && <p className="error-text">{errors.password}</p>}
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            onChange={(e) => validatePassword(e.target.value.trim())}
            className={errors.password ? "input error-input" : "input"}
            value={formData.password || ""}
            required
          />
          <div className={styles.showPassword}>
            <input
              type="checkbox"
              checked={showPassword}
              onChange={() => setShowPassword(!showPassword)}
            />
            <span>Show password</span>
          </div>
          <input
            type="button"
            className="primary-btn"
            value="Next"
            onClick={() => setStep(2)}
            disabled={
              errors.email !== null ||
              errors.password !== null ||
              errors.username !== null ||
              formData.email === "" ||
              formData.password === "" ||
              formData.username === ""
            }
          />
        </>)}

        {step === 2 && (<>
          {errors.firstName && <p className="error-text">{errors.firstName}</p>}
          <input
            type="text"
            placeholder="First name"
            onChange={(e) => validateFirstName(e.target.value.trim())}
            className={errors.firstName ? "input error-input" : "input"}
            value={formData.firstName || ""}
            required
          />
          {errors.lastName && <p className="error-text">{errors.lastName}</p>}
          <input
            type="text"
            placeholder="Last name"
            onChange={(e) => validateLastName(e.target.value.trim())}
            className={errors.lastName ? "input error-input" : "input"}
            value={formData.lastName || ""}
            required
          />
          <div className="buttons">
            <input
              type="button"
              className="secondary-btn"
              value="Prev"
              onClick={() => setStep(1)}
            />
            <input
              type="submit"
              className="primary-btn"
              value="Submit"
              disabled={
                errors.firstName !== null ||
                errors.lastName !== null ||
                formData.firstName === "" ||
                formData.lastName === ""
              }
            />
          </div>
        </>)}
      </form>
    </div>
  </div>
}
