import { useState } from "react";

const mockDeals = {
  Today: ["Deal A"],
  Yesterday: ["Deal B"],
  "Last 7 Days": ["Deal C"],
  "Previous 30 Days": ["Deal D"],
};

export default function DealList() {
  const [selected, setSelected] = useState("");

  return (
    <>
      <div className="mt-6 mb-10">
        <h2 className="text-3xl font-thin text-center mb-4">
          Hennessey Auto IDP
        </h2>
      </div>
      <div className="mb-5">
        <button className="w-full">New Deal</button>
      </div>
      <div>
        <h2 className="text-xl  mb-4">Previously Processed Deals</h2>
        {Object.entries(mockDeals).map(([period, deals]) => (
          <div key={period} className="mb-4">
            <h3 className="text-lg font-semibold capitalize">
              {period.replace(/([A-Z])/g, " $1")}
            </h3>
            <ul className="ml-4 mt-2">
              {deals.map((deal) => (
                <li
                  key={deal}
                  className={`cursor-pointer hover:text-blue-500 ${
                    selected === deal ? "text-blue-700 font-semibold" : ""
                  }`}
                  onClick={() => setSelected(deal)}
                >
                  {deal}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </>
  );
}
