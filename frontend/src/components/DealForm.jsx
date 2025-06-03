import { useState, useEffect, useRef } from "react";
import Select from "react-select";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import { Loader2, CheckCircle2, XCircle } from "lucide-react";
import { Link } from "react-router-dom";

const dealOptions = [
  { value: "trade", label: "Trade Pack" },
  { value: "tag_title", label: "Tag and Title Pack" },
];

const requiredDocsMap = {
  trade: ["Title", "Bill of Sale", "Power of Attorney"],
  tag_title: ["Bill of Sale", "MV1 Form", "POA"],
};

export default function DealForm() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(true);
  const [dealType, setDealType] = useState(dealOptions[0]);
  const [documents, setDocuments] = useState({});
  const [loading, setLoading] = useState(false);
  const [clientId] = useState(uuidv4()); // Generate unique client ID
  const [wsMessage, setWsMessage] = useState(null);
  const wsRef = useRef(null);
  const [docStatus, setDocStatus] = useState({});
  const [bckDealId, setBckDealId] = useState(); // Example deal ID, can be dynamic

  const requiredDocs = requiredDocsMap[dealType.value];

  useEffect(() => {
    setDocuments({});
  }, [dealType]);

  useEffect(() => {
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${clientId}`);
    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (event) => {
      console.log("Message from server:", event.data);
      setWsMessage(JSON.parse(event.data));

      const messageData = JSON.parse(event.data);
      if (messageData.processing_details){
        const transformedStatus = {};
        for (const [fileName, status] of Object.entries(messageData?.processing_details?.documents_details)) {
          transformedStatus[fileName] = {
            s3: status?.upload_to_s3 === true ? "Success" : status?.upload_to_s3 === false ? "Fail" : "Loader",
            bda: status?.bda_invocation === true ? "Success" : status?.bda_invocation === false ? "Fail" : "Loader",
            db: status?.database_update === true ? "Success" : status?.database_update === false ? "Fail" : "Loader",
            validation: status?.validation === true ? "Success" : status?.validation === false ? "Fail" : "Loader"
          };
        setDocStatus(transformedStatus);
        }
      }
    };
    ws.onerror = (err) => console.error("WebSocket error:", err);
    ws.onclose = () => console.log("WebSocket closed");

    wsRef.current = ws;

    return () => ws.close();
  }, [clientId]);

  // useEffect(() => {
  //   console.log("WebSocket message received:", wsMessage);
  // }, [wsMessage]);

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

    requiredDocs.forEach((docLabel) => {
      // formData.append("docLabel", documents[docLabel]);
      formData.append("files", documents[docLabel]);
    });

    try {
      setLoading(true);
      const response = await axios.post(
        `http://127.0.0.1:8000/api/upload/${clientId}/123123`,
        formData
      );
      // setDocStatus(JSON.parse(response?.data?.status))
      console.log(response?.data['status']);
      setBckDealId(111222);
      setResult(`Success: ${response.data}`)
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

  const renderStatusIcon = (status) => {
    switch (status) {
      case "Loader":
        return <Loader2 className="w-5 h-5 text-yellow-500 animate-spin" />;
      case "Success":
        return <CheckCircle2 className="w-5 h-5 text-green-600" />;
      case "Fail":
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return <span className="text-gray-400">-</span>;
    }
  };

  const isProcessingOngoing = () => {
    return Object.values(docStatus).some((status) =>
      Object.values(status).includes("Loader")
    );
  };

  const areAllRequiredDocsUploaded = () => {
    return requiredDocs.every((doc) => documents.hasOwnProperty(doc));
  };

  return (
    <div className="flex justify-center items-center h-full w-full gap-10">
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
                  className="flex items-center justify-between space-x-4 p-2"
                >
                  <label className="font-medium">{doc}</label>
                  <div className="flex items-center space-x-2">

                    {documents[doc] && (
                      <CheckCircle2 className="w-5 h-5 text-green-600" />
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
                        {documents[doc] ? "Change File" : "Select File"}
                      </label>
                  </div>
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
              !areAllRequiredDocsUploaded() || isProcessingOngoing()
                ? "bg-blue-300 cursor-not-allowed"
                : "bg-blue-500 hover:bg-blue-600 cursor-pointer"
            }`}
          >
            {loading ? "Processing..." : "Upload and Process All Documents"}
          </button>
        </form>

        {/* {result && (
          <div className="bg-green-100 p-4 rounded-lg shadow mt-5">
            <h3 className="font-semibold text-green-800">Result</h3>
            <p>{wsMessage?.message}</p>
            <p>{docStatus && "DocStatus"}</p>
          </div>
        )} */}
      </div>
      {Object.keys(docStatus).length > 0 && (
        <div className="w-[50vw] p-10 rounded-3xl bg-gray-100 md:w-2/3 lg:w-2/4">
          <div className="bg-green-100 p-4 rounded-lg shadow mt-5">
              <h3 className="font-semibold text-green-800">Result / Process</h3>
              <p>{wsMessage?.message}</p>
          </div>
          <div className="mt-8">
            <h3 className="font-semibold mb-4 text-center text-gray-800 text-lg">
              📄 Document Processing Status
            </h3>
            <div className="overflow-auto rounded-xl shadow-md border border-gray-200 bg-white">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-50 text-gray-700">
                  <tr>
                    <th className="py-3 px-4 text-left font-semibold border-b">Document</th>
                    <th className="py-3 px-4 text-center font-semibold border-b">Upload to S3</th>
                    <th className="py-3 px-4 text-center font-semibold border-b">BDA Invocation</th>
                    <th className="py-3 px-4 text-center font-semibold border-b">Stored in DB</th>
                    <th className="py-3 px-4 text-center font-semibold border-b">Validation</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(docStatus).map(([file, status], idx) => (
                    <tr key={idx} className="hover:bg-gray-50 transition">
                      <td className="py-2 px-4 font-medium border-b">{file}</td>
                      <td className="py-2 px-4 text-center border-b">{renderStatusIcon(status?.s3)}</td>
                      <td className="py-2 px-4 text-center border-b">{renderStatusIcon(status?.bda)}</td>
                      <td className="py-2 px-4 text-center border-b">{renderStatusIcon(status?.db)}</td>
                      <td className="py-2 px-4 text-center border-b">{renderStatusIcon(status?.validation)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          {bckDealId && (
            <div className="mt-4 text-center">
              <Link
                disabled={!isProcessingOngoing()}
                to={`/deal/${bckDealId}`}
                className="text-blue-600 hover:underline"
              >
                View Deal Details
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
