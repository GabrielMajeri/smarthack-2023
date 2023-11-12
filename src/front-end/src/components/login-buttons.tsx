"use client";

import Link from "next/link";

import { usePathname } from "next/navigation";

export default function LoginButtons() {
  const pathname = usePathname();
  const loggedIn = pathname === "/" ? false : true;

  if (loggedIn) {
    return (
      <Link
        href="/profile"
        className="text-violet-500 border border-violet-500 rounded-full px-8 py-2"
      >
        John Doe
      </Link>
    );
  }

  return (
    <ul className="flex flex-row items-center">
      <li>
        <Link href="/sign-in" className="inline-block font-bold px-10 py-3">
          Sign in
        </Link>
      </li>
      <li>
        <Link
          href="/sign-up"
          className="inline-block font-bold text-violet-500 border border-violet-500 rounded-full px-10 py-3"
        >
          Sign up
        </Link>
      </li>
    </ul>
  );
}
