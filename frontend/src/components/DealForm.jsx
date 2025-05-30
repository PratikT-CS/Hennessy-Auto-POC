// import { useState, useEffect } from "react";
// import Select from "react-select";
// import axios from "axios";

// const dealOptions = [
//   { value: "trade", label: "Trade Pack" },
//   { value: "tag_title", label: "Tag and Title Pack" },
// ];

// const requiredDocsMap = {
//   trade: ["Title", "Bill of Sale", "Power of Attorney"],
//   tag_title: ["Bill of Sale", "MV1 Form", "Driver's License"],
// };

// export default function DealForm() {
//   const [input, setInput] = useState("");
//   const [result, setResult] = useState("");
//   const [dealType, setDealType] = useState(dealOptions[0]);
//   const [documents, setDocuments] = useState({});
//   const [loading, setLoading] = useState(false);

//   const requiredDocs = requiredDocsMap[dealType.value];

//   useEffect(() => {
//     // Reset documents when deal type changes
//     setDocuments({});
//   }, [dealType]);

//   const handleSingleFileUpload = (e, docLabel) => {
//     const file = e.target.files[0];
//     if (!file) return;
//     setDocuments((prev) => ({ ...prev, [docLabel]: file }));
//   };

//   const handleProcess = async (e) => {
//     e.preventDefault();
//     const allDocsUploaded = requiredDocs.every((doc) => documents[doc]);

//     if (!allDocsUploaded) {
//       alert("Please upload all required documents before processing.");
//       return;
//     }

//     const formData = new FormData();
//     formData.append("dealType", dealType.value);
//     formData.append("description", input);

//     requiredDocs.forEach((docLabel) => {
//       formData.append("documents", documents[docLabel]);
//       formData.append("document_names", docLabel);
//     });

//     try {
//       setLoading(true);
//       // const response = await axios.post(
//       //   "https://example.com/api/process-deal",
//       //   formData,
//       //   {
//       //     headers: {
//       //       "Content-Type": "multipart/form-data",
//       //     },
//       //   }
//       // );
//       console.log(formData);
//       setResult(`Success: ${JSON.stringify(response.data)}`);
//     } catch (error) {
//       console.error(error);
//       setResult("Failed to process deal. Please try again.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="flex justify-center items-center h-full w-full">
//       <div className="w-full p-10 rounded-3xl bg-gray-100 md:w-2/3 lg:w-2/4">
//         <h2 className="text-xl font-semibold mb-4 text-center">
//           Upload Documents for Deal Processing
//         </h2>

//         <form onSubmit={handleProcess} className=" space-y-4">
//           <div>
//             <label className="block mb-1 font-medium">Deal Type</label>
//             <Select
//               options={dealOptions}
//               value={dealType}
//               onChange={(type) => setDealType(type)}
//               className="text-sm rounded-lg"
//             />
//           </div>
//           <div className="bg-gray-200 p-5 rounded-lg text-sm">
//             <p className="font-semibold mb-2">Upload Required Documents:</p>
//             <ul className="space-y-2">
//               {requiredDocs.map((doc, i) => (
//                 <li
//                   key={i}
//                   className="flex items-center justify-between space-x-4"
//                 >
//                   <label className="w-40 font-medium">{doc}</label>

//                   {documents[doc] && (
//                     <span className="text-green-600 font-semibold text-xs text-right">
//                       {/* {documents[doc].name} */}
//                       Done
//                     </span>
//                   )}
//                   {/* Hidden file input + Styled label as button */}
//                   <div className="relative">
//                     <input
//                       id={`file-input-${i}`}
//                       type="file"
//                       accept=".pdf,.jpg,.jpeg,.png"
//                       onChange={(e) => handleSingleFileUpload(e, doc)}
//                       className="hidden"
//                     />
//                     <label
//                       htmlFor={`file-input-${i}`}
//                       className="cursor-pointer bg-gray-400 text-white px-4 py-1 rounded text-sm hover:bg-gray-500 transition"
//                     >
//                       {/* Upload File */}
//                       {/* Change File */}
//                       {documents[doc] ? "Change File" : "Upload File"}
//                     </label>
//                   </div>
//                 </li>
//               ))}
//             </ul>
//           </div>

//           {/* <div className="bg-blue-50 border p-4 rounded text-sm">
//             <p className="font-semibold mb-2">Upload Required Documents:</p>
//             <ul className="space-y-2">
//               {requiredDocs.map((doc, i) => (
//                 <li key={i} className="flex items-center space-x-4">
//                   <label className="w-40 font-medium">{doc}</label>
//                   <input
//                     type="file"
//                     placeholder="Upload file"
//                     accept=".pdf,.jpg,.jpeg,.png"
//                     onChange={(e) => handleSingleFileUpload(e, doc)}
//                     className="text-sm"
//                   />
//                   {documents[doc] && (
//                     <span className="text-green-600 font-semibold text-xs">
//                       Uploaded
//                     </span>
//                   )}
//                 </li>
//               ))}
//             </ul>
//           </div> */}

//           <button
//             type="submit"
//             disabled={!requiredDocs.every((doc) => documents[doc]) || loading}
//             className={`px-4 py-2 rounded-lg text-grey w-full mt-4 ${
//               loading
//                 ? "bg-blue-300 cursor-not-allowed"
//                 : "bg-blue-600 hover:bg-blue-700 "
//             }`}
//           >
//             {loading ? "Processing..." : "Upload and Process All Documents"}
//           </button>
//         </form>

//         {result && (
//           <div className="bg-green-100 p-4 rounded-lg shadow mt-5">
//             <h3 className="font-semibold text-green-800">Result</h3>
//             <p>{result}</p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

import { useState, useEffect, useRef } from "react";
import Select from "react-select";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";

const dealOptions = [
  { value: "trade", label: "Trade Pack" },
  { value: "tag_title", label: "Tag and Title Pack" },
];

const requiredDocsMap = {
  trade: ["Title", "Bill of Sale", "Power of Attorney"],
  tag_title: ["Bill of Sale", "MV1 Form", "Driver's License"],
};

export default function DealForm() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(true);
  const [dealType, setDealType] = useState(dealOptions[0]);
  const [documents, setDocuments] = useState({});
  const [loading, setLoading] = useState(false);
  const [clientId] = useState(uuidv4()); // Generate unique client ID
  const [wsMessage, setWsMessage] = useState("");
  const wsRef = useRef(null);

  const requiredDocs = requiredDocsMap[dealType.value];

  useEffect(() => {
    setDocuments({});
  }, [dealType]);

  useEffect(() => {
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${clientId}`);
    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (event) => {
      console.log("Message from server:", event.data);
      setWsMessage(event.data);
    };
    ws.onerror = (err) => console.error("WebSocket error:", err);
    ws.onclose = () => console.log("WebSocket closed");

    wsRef.current = ws;

    return () => ws.close();
  }, [clientId]);

  const handleSingleFileUpload = (e, docLabel) => {
    const file = e.target.files[0];
    if (!file) return;
    setDocuments((prev) => ({ ...prev, [docLabel]: file }));
  };

  const handleProcess = async (e) => {
    e.preventDefault();
    const allDocsUploaded = requiredDocs.every((doc) => documents[doc]);

    if (!allDocsUploaded) {
      alert("Please upload all required documents before processing.");
      return;
    }

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send("Start processing deal");
    }

    const formData = new FormData();
    // formData.append("dealType", dealType.value);
    // formData.append("description", input);

    // var files = [];
    requiredDocs.forEach((docLabel) => {
      // files.push(documents[docLabel]);
      formData.append("files", documents[docLabel]);
      // formData.append("document_names", docLabel);
    });
    // formData.append("files", files);
    // console.log(formData);

    try {
      setLoading(true);
      const response = await axios.post(
        `http://127.0.0.1:8000/api/upload/:${clientId}/:250001`,
        formData
      );
      setResult(`Success: ${JSON.stringify(response.data)}`);
    } catch (error) {
      console.error(error);
      setResult("Failed to process deal. Please try again.");
    } finally {
      setInput("");
      setDocuments({});
      setDealType(dealOptions[0]);
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center h-full w-full">
      <div className="w-full p-10 rounded-3xl bg-gray-100 md:w-2/3 lg:w-2/4">
        <h2 className="text-xl font-semibold mb-4 text-center">
          Upload Documents for Deal Processing
        </h2>

        <form onSubmit={handleProcess} className=" space-y-4">
          <div>
            <label className="block mb-1 font-medium">Deal Type</label>
            <Select
              options={dealOptions}
              value={dealType}
              onChange={(type) => setDealType(type)}
              className="text-sm rounded-lg"
            />
          </div>
          <div className="bg-gray-200 p-5 rounded-lg text-sm">
            <p className="font-semibold mb-2">Upload Required Documents:</p>
            <ul className="space-y-2">
              {requiredDocs.map((doc, i) => (
                <li
                  key={i}
                  className="flex items-center justify-between space-x-4"
                >
                  <label className="w-40 font-medium">{doc}</label>

                  {documents[doc] && (
                    <span className="text-green-600 font-semibold text-xs text-right">
                      {/* {documents[doc].name} */}
                      Done
                    </span>
                  )}
                  {/* Hidden file input + Styled label as button */}
                  <div className="relative">
                    <input
                      id={`file-input-${i}`}
                      type="file"
                      accept=".pdf,.jpg,.jpeg,.png"
                      onChange={(e) => handleSingleFileUpload(e, doc)}
                      className="hidden"
                    />
                    <label
                      htmlFor={`file-input-${i}`}
                      className="cursor-pointer bg-gray-400 text-white px-4 py-1 rounded text-sm hover:bg-gray-500 transition"
                    >
                      {/* Upload File */}
                      {/* Change File */}
                      {documents[doc] ? "Change File" : "Upload File"}
                    </label>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          {/* <div className="bg-blue-50 border p-4 rounded text-sm">
            <p className="font-semibold mb-2">Upload Required Documents:</p>
            <ul className="space-y-2">
              {requiredDocs.map((doc, i) => (
                <li key={i} className="flex items-center space-x-4">
                  <label className="w-40 font-medium">{doc}</label>
                  <input
                    type="file"
                    placeholder="Upload file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={(e) => handleSingleFileUpload(e, doc)}
                    className="text-sm"
                  />
                  {documents[doc] && (
                    <span className="text-green-600 font-semibold text-xs">
                      Uploaded
                    </span>
                  )}
                </li>
              ))}
            </ul>
          </div> */}

          <button
            type="submit"
            disabled={!requiredDocs.every((doc) => documents[doc]) || loading}
            className={`px-4 py-2 rounded-lg text-grey w-full mt-4 ${
              loading
                ? "bg-blue-300 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 "
            }`}
          >
            {loading ? "Processing..." : "Upload and Process All Documents"}
          </button>
        </form>

        {result && (
          <div className="bg-green-100 p-4 rounded-lg shadow mt-5">
            <h3 className="font-semibold text-green-800">Result</h3>
            <p>{wsMessage}</p>
          </div>
        )}
      </div>
    </div>
  );
}
