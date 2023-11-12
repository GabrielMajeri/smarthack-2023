import { RedirectType, redirect } from "next/navigation";

export default function RequestADemo() {
  redirect("/dashboard", RedirectType.replace);
}
