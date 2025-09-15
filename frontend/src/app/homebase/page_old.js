

import Link from "next/link";
import { Anton, Chivo, Questrial, Jost } from "next/font/google";


// FONT IMPORT
const anton = Anton({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-anton",
});

const chivo = Chivo({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-chivo",
});

const jost = Jost({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-jost",
});


const questrial = Questrial({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-questrial",
});




export default function HomebasePage() {
  return (
    <section
      className={`min-h-screen bg-[#262229] text-[#F4F4F5] px-6 py-12 ${questrial.variable}`}
    >
      <div className="max-w-screen-lg mx-auto space-y-10">

        {/* H1 + Subtitle */}
        <div>
          <h1 className="font-[var(--font-questrial)] text-4xl lg:text-5xl tracking-tight uppercase text-white mb-2">
            Homebase
          </h1>
          <p className="text-white text-lg">
            Sharing care and chaos, all in one place.
          </p>
        </div>


        {/* GRID START */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* HERO TILE */}
          <Link href="/family" className="lg:col-span-2 block w-full">
            <div className="h-[220px] bg-[#e6dff1] hover:bg-[#f2eaff] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-lg hover:shadow-xl transition-colors duration-300">
              <h2 className="text-xl font-semibold mb-2">Your Family</h2>
              <p className="text-sm">All members in one glance</p>
            </div>
          </Link>


          {/* EMPTY SPOT */}
          <div className="hidden lg:block" />

          {/* ACTION TILE GRID */}
          <div className="lg:col-span-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">


            <div className="w-full">
              <Link href="/appointments" className="block w-full">
                <div className="aspect-[9/10] bg-[#cbe7eb] hover:bg-[#d6eff3] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md hover:shadow-lg transition-colors duration-300 flex flex-col justify-between">
                  <h4 className="text-xl font-medium text-lg mb-1">Appointments</h4>
                  <p className="text-[#1B1A1F] text-sm">Next vet: Mon, 14:30</p>
                </div>
              </Link>
            </div>


            <div className="w-full">
              <Link href="/appointments" className="block w-full">
                <div className="aspect-[9/10] bg-[#f2e0e0] hover:bg-[#f9eaea] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md hover:shadow-lg transition-colors duration-300 flex flex-col justify-between">
                  <h4 className="text-xl font-medium text-lg mb-1"> Medical</h4>
                  <p className="text-[#1B1A1F] text-sm">Weight: 4.3 kg</p>
                </div>
              </Link>
            </div>


            <div className="w-full">
              <Link href="/appointments" className="block w-full">
                <div className="aspect-[9/10] bg-[#f3eeea] hover:bg-[#f9f6f3] text-[#1B1A1F] border border-white/10 p-6 rounded-[32px] shadow-md hover:shadow-lg transition-colors duration-300 flex flex-col justify-between">
                  <h4 className="text-xl font-medium text-lg mb-1"> Marketplace</h4>
                  <p className="text-[#1B1A1F] text-sm">Food stock low</p>
                </div>
              </Link>
            </div>



          </div>

        </div>
      </div>
    </section>
  );
}
