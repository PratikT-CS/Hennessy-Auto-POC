import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { Loader2, CheckCircle2, XCircle } from "lucide-react";

const sampleData = {
  "documents": [
    {
      "id": "doc123",
      "name": "TITLE.pdf",
      "previewUrl": "https://hennessy-auto-poc.s3.amazonaws.com/input/250001/BOS.pdf?response-content-disposition=inline&AWSAccessKeyId=AKIA6D6JBWOZLMLX3FDA&Signature=6rbFw7k18zbLbTnq9a1DQGFZO%2Bs%3D&Expires=1748609085",
      "extractedData": {
        "owner": "John Doe",
        "plate": "XYZ123",
        "vin": "1HGCM82633A004352"
      }
    },
    {
      "id": "doc111",
      "name": "BOS.pdf",
      "previewUrl": "https://signed-url-from-s3.com/doc123.pdf",
      "extractedData": {
        "owner": "John Doe",
        "plate": "XYZ123",
        "vin": "1HGCM82633A004352"
      }
    },
    {
      "id": "doc222",
      "name": "POA.pdf",
      "previewUrl": "https://signed-url-from-s3.com/doc123.pdf",
      "extractedData": {
        "owner": "John Doe",
        "plate": "XYZ123",
        "vin": "1HGCM82633A004352"
      }
    }
  ]
}

const dealSampleData = {
  "buyer": "Alice Smith",
  "seller": "Bob Johnson",
  "vehicleInfo": "2018 Toyota Corolla",
  "status": "Pending"
}

const dealSampleData2 = {
  "deal": {
    "frontendDealId": "250001",
    "deal_type": "tag_and_title",
    "created_at": "2023-07-01T12:00:00Z"
  },
  "documents": [
    {
      "id": "doc123",
      "doc_type": "title",
      "s3_url": "",
      "extracted_data": {
        "owner": "Alice Smith",
        "plate": "ABC123",
        "vin": "1HGCM82633A004352"
      }
    },
    {
      "id": "doc111",
      "doc_type": "tag",
      "s3_url": "",
      "extracted_data": {
        "owner": "Bob Johnson",
        "plate": "XYZ789",
        "vin": "00000000000000000"
      }
    }
  ],
  "persons": [
    {
      "name": "John Doe",
      "role": "buyer"
    },
    {
      "name": "Jane Doe",
      "role": "seller"
    }
  ],
  "vehicle": {
    "vin": "1HGCM82633A004352",
    "make": "Honda",
    "model": "Civic",
    "year": 2020
  }
}

const sampleDocStatus = {
  "TITLE.pdf": {
    "s3": null, // Uploaded to S3 
    "bda": true, // BDA invoked
    "db": true, // Stored in DB
    "validation": true // Validation passed
  },
  "BOS.pdf": {
    "s3": true,
    "bda": true,
    "db": false, // Not stored in DB
    "validation": false // Validation failed
  },
  "POA.pdf": {
    "s3": true,
    "bda": false, // BDA invocation failed
    "db": true,
    "validation": true
  }
}

const DealDetailsPage = () => {
  const { dealId } = useParams();
  const [documents, setDocuments] = useState(dealSampleData2?.documents);
  const [dealDetails, setDealDetails] = useState(dealSampleData2);
  const [openIndex, setOpenIndex] = useState(null);
  const [docStatus, setDocStatus] = useState(sampleDocStatus);

  useEffect(() => {
    const fetchDealData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/deals/${dealId}`);
        const data = response.data;
        console.log(data);

        setDocuments(data?.documents);
        setDealDetails(data);
      } catch (err) {
        console.error("Failed to load deal data", err);
      }
    };
    fetchDealData();
  }, [dealId]);


  const toggleAccordion = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const renderStatusIcon = (status) => {
    switch (status) {
      case "Loader":
        return <Loader2 className="w-full h-5 text-yellow-500 animate-spin" />;
      case "Success":
        return <CheckCircle2 className="w-full h-5 text-green-600" />;
      case "Fail":
        return <XCircle className="w-full h-5 text-red-600" />;
      default:
        return <Loader2 className="w-full h-5 text-yellow-500" />;
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Header */}
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Deal Details - <span className="text-indigo-600">{dealDetails?.deal?.frontendDealId}</span>
      </h1>
      <h3 className="text-xl font-bold text-gray-800 my-2">Deal for : {dealDetails?.deal?.deal_type === "tag_and_title" ? "Tag and Title" : "Trade"}</h3>

      {/* Documents Processing Summary Section */}
      <div className="my-8">
        <h3 className="font-semibold mb-4 text-center text-gray-800 text-lg">
          📄 Document Processing Summary
        </h3>
        <div className="overflow-hidden rounded-xl shadow-md border border-gray-200 bg-white">
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
                  <td className="py-2 px-4 text-cente border-b">{renderStatusIcon(status?.s3)}</td>
                  <td className="py-2 px-4 text-center border-b">{renderStatusIcon(status?.bda)}</td>
                  <td className="py-2 px-4 text-center border-b">{renderStatusIcon(status?.db)}</td>
                  <td className="py-2 px-4 text-center border-b">{renderStatusIcon(status?.validation)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Deal Details Section */}
      {dealDetails && (
        <div className="my-10">
          <div>
            <h2 className="text-xl font-semibold text-gray-700 my-4">Deal Metadata</h2>
            <div className="bg-white p-4 rounded-xl shadow-sm border space-y-2">
              <div><strong>Deal Id:</strong> {dealDetails?.deal?.frontendDealId}</div>
              <div><strong>Deal For:</strong> {dealDetails?.deal?.deal_type === "tag_and_title" ? "Tag and Title" : "Trade"}</div>
            </div>
            <h2 className="text-xl font-semibold text-gray-700 my-4">Vehicle Metadata</h2>
            <div className="bg-white p-4 rounded-xl shadow-sm border space-y-2">
              <div><strong>VIN (Vehicle Identification Number):</strong> {dealDetails?.vehicle?.vin}</div>
              <div><strong>Vehicle Model:</strong> {dealDetails?.vehicle?.model}</div>
              <div><strong>Vehicle Manufacturer:</strong> {dealDetails?.vehicle?.make}</div>
              <div><strong>Vehicle Manufacture Year:</strong> {dealDetails?.vehicle?.year}</div>
            </div>
            <h2 className="text-xl font-semibold text-gray-700 my-4">Persons Metadata</h2>
            <div className="bg-white p-4 rounded-xl shadow-sm border space-y-2">
              <h3 className="text-lg font-semibold">Parties Involved</h3>
              {dealDetails?.persons?.map((person, index) => (
                <div key={index * 12 + 1} className="mb-2">
                  <strong>{person.role.charAt(0).toUpperCase() + person.role.slice(1)}:</strong> {person.name}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Documents Section */}
      <h2 className="text-xl font-semibold text-gray-700 mb-4">Documents</h2>
      <div className="space-y-4">
        {documents?.map((doc, index) => (
          <div
            key={doc?.id}
            className="border rounded-xl shadow-md overflow-hidden transition-all"
          >
            <button
              onClick={() => toggleAccordion(index)}
              className="w-full flex justify-between items-center p-4 bg-gray-100 hover:bg-gray-200"
            >
              <span className="font-medium">{doc?.doc_type}</span>
              <span>{openIndex === index ? "▲" : "▼"}</span>
            </button>
            {openIndex === index && (
              <div className="p-4 bg-white space-y-4">
                {/* Preview */}
                {/* <div>
                  <p className="font-semibold">Preview:</p>
                  <iframe
                    src={doc.previewUrl}
                    title={doc.name}
                    className="w-full h-64 border rounded-lg"
                  ></iframe>
                </div> */}
                {/* Extracted Details */}
                <div>
                  <p className="font-semibold">Extracted Data:</p>
                  <pre className="bg-gray-50 p-3 rounded text-sm text-gray-700">
                    {JSON.stringify(doc?.extracted_data, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DealDetailsPage;
