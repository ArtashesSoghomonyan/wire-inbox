"use client";

import React, { createContext, useCallback, useContext, useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";

type Theme = "light" | "dark";

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [theme, setThemeState] = useState<Theme>("light");

  // Derive the effective theme:
  // - Logged-in users: use their backend setting
  // - Anonymous users: always light
  const deriveTheme = useCallback((): Theme => {
    if (user?.settings?.theme) {
      return user.settings.theme;
    }
    return "light";
  }, [user]);

  // Sync theme whenever user changes (login/logout) or on mount
  useEffect(() => {
    const effectiveTheme = deriveTheme();
    setThemeState(effectiveTheme);
    document.documentElement.setAttribute("data-theme", effectiveTheme);
  }, [deriveTheme]);

  const setTheme = useCallback((newTheme: Theme) => {
    setThemeState(newTheme);
    document.documentElement.setAttribute("data-theme", newTheme);
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};
