import Link from "next/link";
import Image from "next/image";

import logo from "@/assets/images/logo.png";

import LoginButtons from "./login-buttons";

export function NavBar() {
  const navLinks = [
    {
      url: "/about",
      label: "About",
    },
    {
      url: "/features",
      label: "Features",
    },
    {
      url: "/pricing",
      label: "Pricing",
    },
    {
      url: "/testimonials",
      label: "Testimonials",
    },
    {
      url: "/help",
      label: "Help",
    },
  ];

  return (
    <nav className="mb-24 flex flex-row items-center justify-between">
      <Link href="/">
        <Image src={logo} alt="" className="inline-block h-10 w-10" />
        <span className="ml-3 text-xl font-bold">AcquiSmart</span>
      </Link>
      <ul className="flex flex-row items-center">
        {navLinks.map(({ url, label }, index) => (
          <li key={index} className="mr-5">
            <Link href={url} className="text-small">
              {label}
            </Link>
          </li>
        ))}
      </ul>
      <LoginButtons />
    </nav>
  );
}
