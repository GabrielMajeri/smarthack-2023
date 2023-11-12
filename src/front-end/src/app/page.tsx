import Link from "next/link";
import Image from "next/image";

import searchingImage from "@/assets/images/undraw/searching.svg";
import sketchingImage from "@/assets/images/undraw/sketching.svg";

export default function Home() {
  return (
    <main className="max-w-screen-lg mx-auto">
      <section className="flex flex-row flex-wrap gap-12">
        <header className="flex-[2]">
          <h1 className="text-4xl font-medium">
            Handle procurements easily <br /> with{" "}
            <span className="font-bold">AcquiSmart</span>.
          </h1>
          <p className="mt-4 max-w-xl">
            With <span className="font-semibold">AcquiSmart</span>&apos;s
            digital procurement platform, the acquisition of new products and
            services is as easy as filling out a{" "}
            <span className="text-red-500 font-semibold">
              Christmas wishlist
            </span>
            .
          </p>
          <Link
            href="/request-a-demo"
            className="inline-block mt-20 shadow-[0_25px_30px_-15px_rgba(139,92,246,0.6)] bg-violet-500 text-white font-bold px-10 py-3 rounded-lg"
          >
            Get started
          </Link>
        </header>
        <div className="flex-[1]">
          <Image src={searchingImage} alt="" />
        </div>
      </section>
      <section className="mt-12 flex flex-row flex-wrap gap-12">
        <div className="flex-[1]">
          <Image src={sketchingImage} alt="" />
        </div>
        <div className="flex-[2]">
          <h2 className="text-3xl font-medium">Smart procurement strategy</h2>
          <p className="mt-4">
            Our <span className="text-blue-700">AI-driven</span> tool optimizes
            procurement strategy for institutions. By leveraging advanced
            technology, we streamline processes, ensure transparency, and
            identify cost-effective suppliers. With tailored insights, we
            empower smarter, more impactful procurement decisions.
          </p>
        </div>
      </section>
    </main>
  );
}
