import type { Metadata } from "next";
import "./globals.css";
import LiveChat from "./components/LiveChat";

export const metadata: Metadata = {
  title: "NOVAMART — Shop smarter",
  description: "A modern Bangladesh marketplace for everyday essentials.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="bn"><body>{children}<LiveChat /></body></html>;
}
