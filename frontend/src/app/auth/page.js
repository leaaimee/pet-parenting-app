"use client";

import { useState } from "react";
import LoginForm from "@/components/LoginForm";
import RegisterForm from "@/components/RegisterForm";
import { Questrial } from "next/font/google";

const questrial = Questrial({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-questrial",
});

export default function AuthPage() {
  const [isLoginMode, setIsLoginMode] = useState(true);

  return (
    <section className={`min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12 ${questrial.variable}`}>
      <div className="max-w-md mx-auto space-y-6">
        <header className="space-y-2 text-center">
          <h1 className="text-4xl font-[var(--font-questrial)] tracking-tight uppercase">
            {isLoginMode ? "Welcome Back" : "Join the Family"}
          </h1>
          <p className="text-[#F4F4F5] text-sm">
            {isLoginMode ? "Log in to manage your pets and profile." : "Register to become part of the family."}
          </p>
        </header>

        <div className="bg-[#cbe7eb] text-[#1B1A1F] border border-white/10 rounded-[32px] shadow-md p-8 transition-colors duration-300">
          {isLoginMode ? <LoginForm /> : <RegisterForm />}
        </div>

        <div className="text-center">
          <button
            className="text-sm underline text-[#F4F4F5] hover:text-white"
            onClick={() => setIsLoginMode(!isLoginMode)}
          >
            {isLoginMode ? "Need an account? Register" : "Already have an account? Log In"}
          </button>
        </div>
      </div>
    </section>
  );
}
