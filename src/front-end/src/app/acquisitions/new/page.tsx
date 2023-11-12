"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

type Acquisition = {
  id: number;
  title: string;
  status: string;
  date: Date;
};

const acquisitions = [
  {
    id: 1,
    title: "Light bulbs for town",
    status: "Approved",
    date: new Date(),
  },
  {
    id: 2,
    title: "Benches in park",
    status: "Approved",
    date: new Date(),
  },
  {
    id: 3,
    title: "Garbage system",
    status: "Waiting for approval",
    date: new Date(),
  },
  {
    id: 4,
    title: "More light bulbs",
    status: "Waiting for approval",
    date: new Date(),
  },
  {
    id: 5,
    title: "Water pipes",
    status: "Waiting for approval",
    date: new Date(),
  },
  {
    id: 6,
    title: "Christmas lights",
    status: "Rejected",
    date: new Date(),
  },
];

export default function NewAcquisition() {
  const [acquisitionRequest, setAcquisitionRequest] = useState("");
  const [debouncedAcquisitionRequest, setDebouncedAcquisitionRequest] =
    useState("");

  const [similarAcquisitions, setSimilarAcquisitions] = useState<
    undefined | Acquisition[]
  >(undefined);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setDebouncedAcquisitionRequest(acquisitionRequest);
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [acquisitionRequest]);

  useEffect(() => {
    setSimilarAcquisitions([]);
    if (debouncedAcquisitionRequest) {
      fetch(
        `${process.env.NEXT_PUBLIC_API_SERVER_HOST}:30500/extract-product/?prompt=${debouncedAcquisitionRequest}`,
        { method: "POST" },
      )
        .then((response) => response.json())
        .catch((err) => console.error(err))
        .then((response) => {
          const items = response["items"];
          const matchingAcquisitions = acquisitions.filter(({ title }) =>
            items.some((item: string) => title.toLowerCase().includes(item)),
          );

          if (matchingAcquisitions.length > 0) {
            setSimilarAcquisitions(matchingAcquisitions);
          }
        });
    }
  }, [debouncedAcquisitionRequest]);

  return (
    <main className="max-w-prose mx-auto text-center">
      <header>
        <h1 className="font-bold text-2xl">Start a new acquisition</h1>
      </header>
      <section className="mt-10">
        <p className="text-xl">What do you want to buy?</p>
        <input
          type="text"
          placeholder="I want to buy new light bulbs..."
          className="mt-4 min-w-[20em] px-4 py-1 border rounded-full text-center"
          value={acquisitionRequest}
          onChange={(e) => setAcquisitionRequest(e.target.value)}
        />
      </section>
      {similarAcquisitions && similarAcquisitions.length > 0 ? (
        <section>
          <p className="mt-5 text-red-500">
            It looks there are already some items similar to this one in the
            acquisitons list:
          </p>
          <ul>
            {similarAcquisitions.map(({ id, title }) => (
              <li key={id} className="mt-3">
                {id}. {title}
              </li>
            ))}
          </ul>
        </section>
      ) : (
        ""
      )}
      {!!debouncedAcquisitionRequest && (
        <>
          <section className="mt-10">
            <p className="text-xl">Why do you need to buy this?</p>
            <input
              type="text"
              placeholder="I want to change bulbs..."
              className="mt-4 min-w-[20em] px-4 py-1 border rounded-full text-center"
            />
          </section>
          <section className="mt-10">
            <p className="text-xl">Price?</p>
            <input
              type="text"
              placeholder="Enter the estimated price of the product/service..."
              className="mt-4 min-w-[20em] px-4 py-1 border rounded-full text-center"
            />
            <p className="mt-8 text-2xl">Don&apos;t know the price?</p>
            <Link
              href="/market-consultations/new"
              className="inline-block mt-4 shadow-[0_25px_30px_-15px_rgba(22,163,74,0.6)] bg-green-600 text-white font-bold px-10 py-3 rounded-lg"
            >
              Consult the market
            </Link>
          </section>
        </>
      )}
    </main>
  );
}
