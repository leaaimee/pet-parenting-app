import { Geist, Geist_Mono } from "next/font/google";
import { Anton } from "next/font/google";
import "./globals.css";



const anton = Anton({
  weight: "400", // Anton is bold by default
  subsets: ["latin"],
  variable: "--font-anton",
});




const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Pet Parenting App",
  description: "Sharing and Caring Concerns for pets and parents",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[#F5F2F0] text-[#2C2C2C]`}
      >

        <main className="p-4">{children}</main>
      </body>
    </html>
  );
}
