import Link from "next/link";

export default function Home() {
  return (
    <main className="">
      <section className="bg-black text-white min-h-screen flex flex-col pt-[10rem] px-3">
        <header className="text-center">
          <h1 className="text-4xl font-extrabold">AcquiSmart</h1>
          <h2 className="mt-5">
            The last procurement you&apos;ll <br /> have to do manually.
          </h2>
        </header>
        <p className="mt-16 text-justify px-5">
          With AcquiSmart&apos;s digital procurement platform, the acquisition
          of new products and services is as easy as filling out a{" "}
          <span className="text-red-500">Christmas wishlist</span>.
        </p>
        <div className="mt-20 flex flex-col justify-center items-center">
          <Link
            href="/request-a-demo"
            className="inline-block bg-blue-500 text-white font-bold p-3 rounded-sm"
          >
            Request a demo
          </Link>
          <button className="mt-5 text-blue-100 font-bold">
            Find out more
          </button>
        </div>
      </section>
    </main>
  );
}
