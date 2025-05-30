import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

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


const DealDetailsPage = () => {
  const { dealId } = useParams();
  const [documents, setDocuments] = useState([]);
  const [dealDetails, setDealDetails] = useState(null);
  const [openIndex, setOpenIndex] = useState(null);

  useEffect(() => {
    const fetchDealData = async () => {
      try {
        // const [docRes, dealRes] = await Promise.all([
        //   axios.get(`/api/deals/${dealId}/documents`),
        //   axios.get(`/api/deals/${dealId}/details`)
        // ]);
        setDocuments(sampleData.documents);
        setDealDetails(dealSampleData);
      } catch (err) {
        console.error("Failed to load deal data", err);
      }
    };
    fetchDealData();
  }, [dealId]);

  const toggleAccordion = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Header */}
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Deal Details - <span className="text-indigo-600">{dealId}</span>
      </h1>

      {/* Documents Section */}
      <h2 className="text-xl font-semibold text-gray-700 mb-4">Documents</h2>
      <div className="space-y-4">
        {documents.map((doc, index) => (
          <div
            key={doc.id}
            className="border rounded-xl shadow-md overflow-hidden transition-all"
          >
            <button
              onClick={() => toggleAccordion(index)}
              className="w-full flex justify-between items-center p-4 bg-gray-100 hover:bg-gray-200"
            >
              <span className="font-medium">{doc.name}</span>
              <span>{openIndex === index ? "▲" : "▼"}</span>
            </button>
            {openIndex === index && (
              <div className="p-4 bg-white space-y-4">
                {/* Preview */}
                <div>
                  <p className="font-semibold">Preview:</p>
                  <iframe
                    src={doc.previewUrl}
                    title={doc.name}
                    className="w-full h-64 border rounded-lg"
                  ></iframe>
                </div>
                {/* Extracted Details */}
                <div>
                  <p className="font-semibold">Extracted Data:</p>
                  <pre className="bg-gray-50 p-3 rounded text-sm text-gray-700">
                    {JSON.stringify(doc.extractedData, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Deal Details Section */}
      {dealDetails && (
        <div className="mt-10">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Deal Metadata</h2>
          <div className="bg-white p-4 rounded-xl shadow-sm border space-y-2">
            <div><strong>Buyer:</strong> {dealDetails.buyer}</div>
            <div><strong>Seller:</strong> {dealDetails.seller}</div>
            <div><strong>Vehicle:</strong> {dealDetails.vehicleInfo}</div>
            <div><strong>Status:</strong> {dealDetails.status}</div>
            {/* Add other fields as needed */}
          </div>
        </div>
      )}
    </div>
  );
};

export default DealDetailsPage;
