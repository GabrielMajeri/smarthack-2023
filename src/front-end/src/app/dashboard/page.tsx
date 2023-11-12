"use client";

import Link from "next/link";

import { Chart } from "react-google-charts";

function TotalBudgetWidget() {
  const data = [
    ["Acquisition", "Cost"],
    ["Energy", 15],
    ["Utilities", 7],
    ["Employee Benefits", 2],
    ["Raw Materials", 2],
    ["Building Repairs", 7],
  ];

  const options = {
    pieHole: 0.5,
    is3D: false,
    legend: "none",
  };

  return (
    <section>
      <h2 className="font-bold text-2xl text-center">Total budget</h2>
      <h3 className="mt-2 font-normal text-lg text-center text-gray-400">
        FY2023
      </h3>
      <Chart
        chartType="PieChart"
        width="100%"
        height="400px"
        data={data}
        options={options}
      />
    </section>
  );
}

function SpentBudgetWidget() {
  const data = [
    ["Acquisition", "Cost"],
    ["Energy", 4],
    ["Utilities", 1],
    ["Employee Benefits", 6],
    ["Raw Materials", 5],
  ];

  const options = {
    pieHole: 0.5,
    is3D: false,
    legend: "none",
  };

  return (
    <section>
      <h2 className="font-bold text-2xl text-center">Spent budget</h2>
      <h3 className="mt-2 font-normal text-lg text-center text-gray-400">
        FY2023
      </h3>
      <Chart
        chartType="PieChart"
        width="100%"
        height="400px"
        data={data}
        options={options}
      />
    </section>
  );
}

function AcquisitionsPlan() {
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
      status: "Waiting approval",
      date: new Date(),
    },
    {
      id: 4,
      title: "More light bulbs",
      status: "Waiting approval",
      date: new Date(),
    },
    {
      id: 5,
      title: "Water pipes",
      status: "Waiting approval",
      date: new Date(),
    },
    {
      id: 6,
      title: "Christmas lights",
      status: "Rejected",
      date: new Date(),
    },
  ];

  return (
    <>
      <div className="py-5 text-center">
        <input placeholder="Search..." className="outline-none p-3" />
      </div>
      <table className="w-full">
        <thead className="bg-neutral-100">
          <tr>
            <th scope="col" className="width-[50%]">
              Title
            </th>
            <th scope="col">Status</th>
            <th scope="col">Date</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          {acquisitions.map((acquisition) => (
            <tr key={acquisition.id} className="p-3">
              <td className="px-1 py-3">{acquisition.title}</td>
              <td className="flex justify-center items-center">
                <span
                  className={
                    acquisition.status === "Approved"
                      ? "text-sm font-bold bg-green-100 text-green-500 rounded-sm px-2 py-1"
                      : acquisition.status === "Waiting approval"
                      ? "text-sm font-bold bg-yellow-100 text-yellow-500 rounded-sm px-2 py-1 mx-2 my-1"
                      : acquisition.status === "Rejected"
                      ? "text-sm font-bold bg-red-100 text-red-500 round-sm px-2 py-1"
                      : "text-sm font-bold"
                  }
                >
                  {acquisition.status.toUpperCase()}
                </span>
              </td>
              <td>{acquisition.date.toLocaleDateString("en-UK")}</td>
              <td></td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex flex-row flex-wrap gap-4 items-center justify-center">
        <Link
          href="/acquisitions/"
          className="inline-block mt-20 shadow-[0_25px_30px_-15px_rgba(139,92,246,0.6)] bg-violet-500 text-white font-bold px-10 py-3 rounded-lg"
        >
          View all
        </Link>
        <Link
          href="/acquisitions/add"
          className="inline-block mt-20 shadow-[0_25px_30px_-15px_rgba(22,163,74,0.6)] bg-green-600 text-white font-bold px-10 py-3 rounded-lg"
        >
          Add new
        </Link>
      </div>
    </>
  );
}

function SpendingWidget() {
  const data = [
    ["Quarter", "Planned", "Spent"],
    ["Q1 2023", 1000, 900],
    ["Q2 2023", 1200, 750],
    ["Q3 2023", 950, 825],
    ["Q4 2023", 1100, 400],
  ];

  const options = {
    curveType: "function",
    legend: { position: "bottom" },
    hAxis: {
      title: "Quarter",
    },
    vAxis: {
      title: "Million €",
    },
  };

  return (
    <section>
      <h2 className="font-bold text-2xl text-center">Spending</h2>
      <Chart
        chartType="LineChart"
        width="100%"
        height="400px"
        data={data}
        options={options}
      />
    </section>
  );
}

export default function Dashboard() {
  return (
    <div className="flex flex-row flex-wrap gap-8">
      <section className="flex-[1]">
        <TotalBudgetWidget />
        <SpentBudgetWidget />
      </section>
      <section className="flex-[2]">
        <header>
          <h1 className="font-bold text-2xl">Acquisitions plan for 2024</h1>
        </header>
        <AcquisitionsPlan />
      </section>

      <section className="flex-[1]">
        <SpendingWidget />
      </section>
    </div>
  );
}
