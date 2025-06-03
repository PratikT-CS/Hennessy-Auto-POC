import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const mockDeals = {
  "Today": ["Deal A"],
  "Yesterday": ["Deal B"],
  "Last 7 Days": ["Deal C"],
  "Previous 30 Days": ["Deal D"],
};

export default function DealList() {
  const [selected, setSelected] = useState("");
  const [deals, setDeals] = useState([]);

  useEffect(() => {
    // Simulate fetching deals from an API
    const fetchDeals = async () => {
      // In a real application, you would replace this with an API call
      const response = await axios.get('http://localhost:8000/api/deals');
      setDeals(response.data);
    };

    fetchDeals();
  }, []);

  return (
    <>
      <div className="mt-6 mb-10">
        <h2 className="text-3xl font-thin text-center mb-4">
          Hennessey Auto IDP
        </h2>
      </div>
      <div className="mb-5 flex justify-center">
        <Link 
          className="bg-gray-200 text-gray-700 hover:bg-gray-300 px-4 py-1 rounded-lg cursor-pointer shadow "
          to="/"
        >
            New Deal
        </Link>
      </div>
      <div>
        <h2 className="text-xl  mb-4">Previously Processed Deals</h2>
        {Object.entries(deals).map(([period, deals]) => (
          <div key={period} className="mb-4">
            <h3 className="text-lg font-semibold capitalize">
              {period?.replace(/([A-Z])/g, " $1")}
            </h3>
            <ul className="ml-4 mt-2">
              {deals?.map((deal) => (
                <li
                  key={deal}
                  className={`cursor-pointer hover:text-blue-500 ${
                    selected === deal ? "text-blue-700 font-semibold" : ""
                  }`}
                  onClick={() => setSelected(deal)}
                >
                  <Link to={`/deal/${deal}`}>{deal}</Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </>
  );
}
