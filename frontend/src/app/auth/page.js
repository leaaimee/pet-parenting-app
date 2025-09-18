"use client";

import { useState } from "react";
import LoginForm from "@/components/forms/LoginForm";
import RegisterForm from "@/components/forms/RegisterForm";
import { Questrial } from "next/font/google";

// branding

import TitleAniSub from "@/components/title/TitleAniSub";

const questrial = Questrial({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-questrial",
});

export default function AuthPage() {
  const [isLoginMode, setIsLoginMode] = useState(true);

  return (
    <section
      className={`min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12 ${questrial.variable}`}
    >
      <div className="max-w-md mx-auto space-y-6">
        {/* BRAND */}
      <header className="mb-6">
        <TitleAniSub />
      </header>

        {/* CARD */}
<div className="colorscheme-light bg-[#cbe7eb] text-[#1B1A1F] border border-white/10 rounded-[32px] shadow-md p-8 transition-colors duration-300">
  <h2 className="text-xl font-semibold mb-2">
    {isLoginMode ? "Welcome Back" : "Join the Family"}
  </h2>
  <p className="text-sm mb-4 -mt-2">
    {isLoginMode
      ? "Log in to manage your pets and profile."
      : "Register to become part of the family."}
  </p>

  {isLoginMode ? <LoginForm /> : <RegisterForm />}
</div>

        {/* TOGGLE BUTTON */}
        <div className="text-center">
          <button
            className="text-sm underline text-[#F4F4F5] hover:text-white"
            onClick={() => setIsLoginMode(!isLoginMode)}
          >
            {isLoginMode
              ? "Need an account? Register"
              : "Already have an account? Log In"}
          </button>
        </div>
      </div>
    </section>
  );
}
