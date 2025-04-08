import { Inter} from "next/font/google";
import "./globals.css";
import Header from "@/components/header";
import { ClerkProvider } from "@clerk/nextjs";

const inter=Inter({subsets:["latin"]});

export const metadata = {
  title: "Finalyze",
  description: "Open platform for finance and budget plan",
};

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>

    
    <html lang="en">
      <body
        className={`${inter.className}`}>

        {/*header*/}
        <Header />
        <main className="min-h-screen">
        {children}
        </main>
        {/*footer*/}
        <footer className="bg-blue-50">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>Finance and Budget Planning Platform</p>
        </div>
        </footer>
      </body>
    </html>
    </ClerkProvider>
  );
}
