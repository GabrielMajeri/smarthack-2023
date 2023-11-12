import type { Metadata } from "next";
import { Rubik } from "next/font/google";

import classNames from "classnames";

import { NavBar } from "@/components/nav-bar";

import "./globals.css";

const rubik = Rubik({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AcquiSmart",
  description: "The intelligent procurement platform.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={classNames(rubik.className, "px-28 pt-10")}>
        <NavBar />
        {children}
      </body>
    </html>
  );
}
